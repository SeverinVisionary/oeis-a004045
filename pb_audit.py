#!/usr/bin/env python3
"""Encoding-faithfulness audit for pb_encode.py.

The weakest link in any certification pipeline is the encoding: an impeccable
refutation of the wrong formula proves nothing. This script attacks that link
from two independent directions and refuses to pass unless both hold.

    python3 pb_audit.py                  # every instance the certificates use
    python3 pb_audit.py --n 8 --M 60     # one decision instance
    python3 pb_audit.py --n 8 --opt      # the optimisation instance

Direction 1 -- structural, against the model that produced the readings
----------------------------------------------------------------------
`milp_model.py` is *executed*, not re-implemented, with `highspy.Highs`
replaced by a recording proxy that forwards nothing and solves nothing but
captures every `addVars` / `changeColsIntegrality` / `addRow` call the model
makes.  The rows HiGHS would actually have received are then put in a
canonical form (`sum a_i x_i >= b`, coefficients sorted by variable) and
compared as a multiset against a *fresh parse* of the .opb file.  The OPB
parser here shares no code with `pb_encode.py`: it reads the file back as
text, exactly as a third party's solver would.

Passing this means the PB instance and the MILP instance have the same
feasible set by construction, not by inspection.

Direction 2 -- behavioural, against the standalone verifier
-----------------------------------------------------------
Known-good and deliberately-broken codes are evaluated against the parsed OPB
constraints:

  * the published 64-word incumbent satisfies every constraint of the n = 8,
    M = 64 instance -- so the encoding is not accidentally unsatisfiable;
  * the same incumbent violates the M = 57..60 instances on the cardinality
    row only, and satisfies the optimisation instance outright -- so the
    cardinality row is present, bites, and is absent exactly where it should
    be;
  * an incumbent with one codeword deleted violates coverage rows, and the
    number of violated coverage rows equals the deficient-word count that
    `verify.py` -- a separate program sharing no code with either the encoder
    or the models -- reports for the same code;
  * an incumbent with one codeword relocated likewise fails, and agrees with
    `verify.py` on how badly.

A pipeline that cannot fail on a broken code is not testing anything, so the
negative cases are as load-bearing as the positive one.

Requires: highspy (direction 1 only). `--skip-milp` runs direction 2 alone.
"""
import argparse
import json
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------------
# An OPB reader that shares no code with the encoder.
# --------------------------------------------------------------------------

def parse_opb(path):
    """Read an OPB file as text. Returns (nvars, [(coefs, rhs)]) in >= form.

    `coefs` is a dict {0-based variable index: integer coefficient}. Every
    constraint is normalised to `sum coefs >= rhs`. An objective line, if
    present, is returned separately and is not a constraint.
    """
    nvars = None
    cons = []
    obj = None
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("min:"):
                body = line[4:].rstrip(";").split()
                obj = {}
                for i in range(0, len(body), 2):
                    obj[int(body[i + 1][1:]) - 1] = int(body[i])
                continue
            if line.startswith("*"):
                if "#variable=" in line:
                    toks = line.replace("=", "= ").split()
                    for i, t in enumerate(toks):
                        if t == "#variable=":
                            nvars = int(toks[i + 1])
                continue
            if not line.endswith(";"):
                raise ValueError("OPB constraint without terminating ';': %r" % line)
            body = line[:-1].split()
            if body[-2] not in (">=", "="):
                raise ValueError("unsupported relational operator in %r" % line)
            op, rhs = body[-2], int(body[-1])
            terms, i = {}, 0
            while i < len(body) - 2:
                coef = int(body[i])
                var = body[i + 1]
                if not var.startswith("x"):
                    raise ValueError("non-literal term %r (negated literals ~x "
                                     "are legal OPB but this encoder emits none)" % var)
                idx = int(var[1:]) - 1
                terms[idx] = terms.get(idx, 0) + coef
                i += 2
            if op == "=":
                cons.append((terms, rhs))
                cons.append(({k: -v for k, v in terms.items()}, -rhs))
            else:
                cons.append((terms, rhs))
    if nvars is None:
        raise ValueError("no '#variable=' header in %s" % path)
    for terms, _ in cons:
        for idx in terms:
            if not (0 <= idx < nvars):
                raise ValueError("variable index out of declared range")
    return nvars, cons, obj


def canon(terms, rhs):
    """Hashable canonical form of `sum terms >= rhs`, zero coefficients dropped."""
    return (tuple(sorted((k, v) for k, v in terms.items() if v != 0)), rhs)


def evaluate(cons, assignment):
    """Return the list of indices of constraints violated by `assignment`."""
    bad = []
    for j, (terms, rhs) in enumerate(cons):
        if sum(c * assignment[v] for v, c in terms.items()) < rhs:
            bad.append(j)
    return bad


# --------------------------------------------------------------------------
# Direction 1: record what milp_model.py actually builds.
# --------------------------------------------------------------------------

class _RecordingHighs:
    """Stands in for highspy.Highs: records the model, never solves it."""

    def __init__(self):
        self.rows = []
        self.ncols = None
        self.col_lower = None
        self.col_upper = None
        self.integrality = None
        self.cost = None
        self.options = {}

    def setOptionValue(self, k, v):
        self.options[k] = v

    def addVars(self, n, lower, upper):
        self.ncols = int(n)
        self.col_lower = list(lower)
        self.col_upper = list(upper)

    def changeColsCost(self, n, idx, cost):
        self.cost = dict(zip([int(i) for i in idx], [float(c) for c in cost]))

    def changeColsIntegrality(self, n, idx, kinds):
        self.integrality = dict(zip([int(i) for i in idx], list(kinds)))

    def addRow(self, lower, upper, nnz, idx, vals):
        terms = {}
        for i, v in zip(idx, vals):
            terms[int(i)] = terms.get(int(i), 0) + int(round(float(v)))
        self.rows.append((float(lower), float(upper), terms))

    # The model is never solved; these keep milp_model.run() from crashing.
    def run(self):
        return None

    def getInfo(self):
        return type("Info", (), {"mip_dual_bound": None, "mip_node_count": None})()

    def getModelStatus(self):
        return "recorded"

    def modelStatusToString(self, s):
        return "recorded"

    def getObjectiveValue(self):
        return 0.0

    def getSolution(self):
        return type("Sol", (), {"col_value": []})()


def milp_rows(n, M):
    """Canonical `>=` rows of the model milp_model.py builds.

    `M = None` audits the optimisation form against `milp_model.py --mode opt`,
    which sets a cost of 1 on every column and adds no cardinality row -- the
    exact counterpart of `pb_encode.py --opt`.
    """
    import highspy
    sys.path.insert(0, HERE)
    import milp_model

    real = milp_model.highspy
    rec = {}

    class _Shim:
        kHighsInf = real.kHighsInf
        HighsVarType = real.HighsVarType

        @staticmethod
        def Highs():
            rec["h"] = _RecordingHighs()
            return rec["h"]

    milp_model.highspy = _Shim
    try:
        milp_model.run(n, "opt" if M is None else str(M), budget=1.0)
    finally:
        milp_model.highspy = real

    h = rec["h"]
    inf = real.kHighsInf
    out = []
    for lo, hi, terms in h.rows:
        if hi >= inf:
            out.append(canon(terms, int(round(lo))))
        elif lo <= -inf:
            out.append(canon({k: -v for k, v in terms.items()}, int(round(-hi))))
        else:
            out.append(canon(terms, int(round(lo))))
            out.append(canon({k: -v for k, v in terms.items()}, int(round(-hi))))
    integral = (h.integrality is not None
                and all(str(v).endswith("kInteger") or v == real.HighsVarType.kInteger
                        for v in h.integrality.values()))
    domain = {
        "ncols": h.ncols,
        "lower_all_0": all(x == 0.0 for x in h.col_lower),
        "upper_all_1": all(x == 1.0 for x in h.col_upper),
        "all_integer": bool(integral),
        "objective_all_zero": all(c == 0.0 for c in (h.cost or {}).values()),
        "objective_all_one": all(c == 1.0 for c in (h.cost or {}).values()),
    }
    return out, domain


# --------------------------------------------------------------------------
# Direction 2: known-good and broken codes.
# --------------------------------------------------------------------------

def verify_py(code, n, mu=2):
    """Run the standalone verify.py on a code and return its JSON report."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(sorted(code), f)
        path = f.name
    try:
        p = subprocess.run(
            [sys.executable, os.path.join(HERE, "verify.py"), path,
             "-n", str(n), "--mu", str(mu)],
            capture_output=True, text=True)
        body = p.stdout.rsplit("}", 1)[0] + "}"
        # NB: the verdict is the whole last line. "INVALID".endswith("VALID")
        # is true, so a suffix test here would silently pass broken codes.
        verdict = p.stdout.strip().splitlines()[-1].strip()
        if verdict not in ("VALID", "INVALID"):
            raise ValueError("unexpected verify.py verdict %r" % verdict)
        return json.loads(body), verdict == "VALID"
    finally:
        os.unlink(path)


def assignment_of(code, nvars):
    a = [0] * nvars
    for c in code:
        a[c] = 1
    return a


def behavioural(n, cons, nvars, code, label, expect_ok, rng):
    """Evaluate `code` against the OPB and cross-check with verify.py."""
    bad = evaluate(cons, assignment_of(code, nvars))
    # the cardinality row is the last constraint emitted by pb_encode.py
    card_idx = nvars if len(cons) > nvars else -1
    coverage_violated = [j for j in bad if j != card_idx]
    card_violated = card_idx in bad
    report, ok = verify_py(code, n)
    agree = report["deficient_words"] == len(coverage_violated)
    # verify.py knows nothing about M, so it must agree with the OPB exactly on
    # coverage: valid iff no coverage row is violated.
    agree = agree and (ok == (not coverage_violated))
    passed = (not bad) == expect_ok and agree
    return {
        "case": label,
        "size": len(code),
        "opb_satisfied": not bad,
        "coverage_rows_violated": len(coverage_violated),
        "cardinality_row_violated": card_violated,
        "verify_py_deficient_words": report["deficient_words"],
        "verify_py_valid": ok,
        "agrees_with_verify_py": agree,
        "expected_satisfied": expect_ok,
        "PASS": passed,
    }


# --------------------------------------------------------------------------

def audit_instance(n, M, skip_milp, rng):
    sys.path.insert(0, HERE)
    import pb_encode
    import verify

    with tempfile.NamedTemporaryFile("w", suffix=".opb", delete=False) as f:
        opb = f.name
    meta = pb_encode.write_opb(opb, n, M, mu=2)
    try:
        nvars, cons, obj = parse_opb(opb)
        nrows = (1 << n) + (0 if M is None else 1)
        res = {"n": n, "M": M, "opb": {k: meta[k] for k in
                                       ("variables", "constraints", "bytes", "sha256")},
               "parsed_variables": nvars, "parsed_constraints": len(cons),
               "checks": []}

        want_obj = ({v: 1 for v in range(1 << n)} if M is None else None)
        shape_ok = (nvars == (1 << n) and len(cons) == nrows and obj == want_obj)
        res["checks"].append({"check": "declared shape == parsed shape, and the "
                                       "objective is present iff this is the "
                                       "optimisation form",
                              "PASS": bool(shape_ok)})

        if not skip_milp:
            rows, domain = milp_rows(n, M)
            mine = sorted(canon(t, r) for t, r in cons)
            theirs = sorted(rows)
            same = mine == theirs
            res["milp_domain"] = domain
            res["checks"].append({
                "check": "OPB rows == rows milp_model.py feeds HiGHS (as multisets)",
                "opb_rows": len(mine), "milp_rows": len(theirs),
                "PASS": bool(same),
                "first_difference": None if same else str(
                    next((a, b) for a, b in zip(mine + [None] * len(theirs),
                                                theirs + [None] * len(mine)) if a != b)),
            })
            res["checks"].append({
                "check": "milp_model variable domain is binary and the objective "
                         "matches the OPB form",
                "PASS": bool(domain["ncols"] == (1 << n) and domain["lower_all_0"]
                             and domain["upper_all_1"] and domain["all_integer"]
                             and domain["objective_all_one" if M is None
                                        else "objective_all_zero"]),
            })

        if n == 8:
            good = verify.incumbent_64()
            cases = [(good, "published 64-word incumbent", M is None or M >= 64)]
            broken = sorted(set(good) - {good[7]})
            cases.append((broken, "incumbent minus one codeword", False))
            moved = sorted(set(good) - {good[7]})
            spare = next(v for v in range(1 << n) if v not in set(good))
            cases.append((sorted(set(moved) | {spare}), "one codeword relocated", False))
            for code, label, expect in cases:
                fits = M is None or len(code) <= M
                res["checks"].append(behavioural(n, cons, nvars, code, label,
                                                 expect and fits, rng))
        return res
    finally:
        os.unlink(opb)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--M", type=int, default=None)
    ap.add_argument("--opt", action="store_true",
                    help="audit the optimisation form for --n instead of a rung")
    ap.add_argument("--skip-milp", action="store_true")
    a = ap.parse_args()
    rng = random.Random(20260828)

    if a.n is not None and (a.M is not None or a.opt):
        pairs = [(a.n, None if a.opt else a.M)]
    else:
        pairs = [(6, 19), (6, 20), (6, None), (7, 31), (7, 32), (7, None),
                 (8, 57), (8, 58), (8, 59), (8, 60), (8, 64), (8, None)]

    out = [audit_instance(n, M, a.skip_milp, rng) for n, M in pairs]
    print(json.dumps(out, indent=2))
    failed = [c for r in out for c in r["checks"] if not c["PASS"]]
    print("AUDIT %s (%d checks, %d failed)"
          % ("PASS" if not failed else "FAIL",
             sum(len(r["checks"]) for r in out), len(failed)))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
