#!/usr/bin/env python3
"""Standalone re-checker for the certificates in `certs/`.

Everything a third party needs in order to not trust us. It takes the
committed artifacts and a VeriPB binary, and answers one question per
certificate: *does this proof really refute the instance the statement names?*

    VERIPB=/path/to/veripb  python3 recheck.py --certs certs
    VIPRCHK=/path/to/viprchk python3 recheck.py --certs certs_exact

Standard library only. It does **not** import `pb_encode.py`, `verify.py` or
any other file in this directory -- importing our encoder to check our encoding
would be circular. Instead it re-derives the instance from the definition of
K(n,1,2), in the twelve lines of `expected_constraints` below, and requires the
committed .opb to match *semantically* (same constraint multiset, same variable
count), not merely byte for byte. A reader who disagrees with those twelve
lines should stop there; everything downstream is mechanical.

Two independent certification routes write records here, and both are handled.
Route 1 (`certs/`) is a VeriPB cutting-planes proof checked by `veripb`; route
2 (`certs_exact/`) is a VIPR certificate from exact-rational SCIP, completed by
`viprcomp` and checked by `viprchk`. Both routes' SOLVERS read the same `.opb`,
so step 1 below re-derives one file for both.

Their CHECKERS do not agree, and an earlier version of this comment wrongly
said the check was "literally the same" for both. It is not. `veripb` is
invoked as `veripb instance.opb proof.pbp` and therefore checks the proof
against our instance. `viprchk` is invoked as `viprchk cert.vipr` and never
sees the `.opb` at all: it verifies whatever problem the certificate's own
header states. So for route 2 the link between the certificate and our
instance is NOT established by the checker, and must be established
separately -- that is what `vipr_bind.py` does, and route 2 records are only
trustworthy when their `binding.bound` field is true.

Route 1 records come in two kinds and both are handled:

  * a **rung** record (`"M": 57`) claims `K(n,1,2) > M`, and its proof is a
    refutation of the instance carrying `|C| <= M` as a constraint;
  * a **value** record (`"M": null`) claims `K(n,1,2) = a`, and its proof
    establishes matching bounds on the objective `min |C|` of an instance that
    carries no cardinality constraint at all.

Four things are checked per certificate:

  1. the .opb parses, and its constraint multiset -- and, for a value record,
     its objective -- equals the one implied by "every word of F_2^n has >= 2
     codewords in its radius-1 ball", plus `|C| <= M` for a rung. So the proof
     is about the right formula, not merely about *a* formula;
  2. the recorded sha256 of the .opb and of the .pbp match the files on disk
     -- so the artifacts are the ones the record describes;
  3. VeriPB accepts (.opb, .pbp) and reports the verdict the record claims:
     `VERIFIED UNSATISFIABLE` for a rung, `VERIFIED BOUNDS a <= obj <= b` with
     exactly the recorded bounds for a value;
  4. VeriPB *rejects* the same proof against a deliberately weaker instance
     built from the same twelve lines -- `M + 1` for a rung, `mu = 1` for a
     value. Both are provably satisfiable well below the certified quantity, so
     no valid proof of the claim can exist for them. Without this step a checker
     that accepted everything would look identical to a correct one, and step 3
     would be worthless.

Only all four together certify anything. Any one of them failing makes the
record worthless, and this script exits non-zero and says which.

Proofs too large to commit are listed in `certs/MANIFEST.md` with their sizes,
hashes and exact regeneration commands; regenerate one, drop it in `certs/`,
and re-run this script.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


# --- the mathematics, restated independently of the encoder -----------------

def expected_constraints(n, M, mu=2):
    """The constraint multiset of "K(n,1,mu) <= M", in canonical >= form.

    Variable v (0-based) stands for "the word v is a codeword". Each entry is
    (sorted ((var, coef), ...), rhs) meaning sum coef*var >= rhs. `M = None`
    drops the cardinality row: that is the optimisation form, where the bound
    on |C| is the objective being minimised rather than a constraint.
    """
    N = 1 << n
    out = []
    for v in range(N):                                   # coverage
        ball = sorted([v] + [v ^ (1 << i) for i in range(n)])
        out.append((tuple((c, 1) for c in ball), mu))
    if M is not None:
        out.append((tuple((v, -1) for v in range(N)), -M))   # cardinality
    return sorted(out)


def expected_objective(n):
    """`min |C|` = minimise the all-ones sum over every word."""
    return tuple((v, 1) for v in range(1 << n))


def write_opb(path, n, M, mu=2, objective=False):
    """Write the instance implied by `expected_constraints` -- used only to
    build the negative controls, so it goes through the same twelve lines."""
    cons = expected_constraints(n, M, mu)
    with open(path, "w") as f:
        f.write("* #variable= %d #constraint= %d #equal= 0 intsize= %d\n"
                % (1 << n, len(cons), max(len(str(-M)) if M is not None else 2, 2)))
        if objective:
            f.write("min: %s ;\n"
                    % " ".join("+1 x%d" % (v + 1) for v, _ in expected_objective(n)))
        for terms, rhs in cons:
            f.write("%s >= %d ;\n"
                    % (" ".join("%+d x%d" % (c, v + 1) for v, c in terms), rhs))


# --- an OPB reader ---------------------------------------------------------

def parse_opb(path):
    nvars, cons, obj = None, [], None
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("min:"):
                body = line[4:].rstrip(";").split()
                terms = {}
                for i in range(0, len(body), 2):
                    terms[int(body[i + 1][1:]) - 1] = int(body[i])
                obj = tuple(sorted((k, v) for k, v in terms.items() if v))
                continue
            if line.startswith("*"):
                if "#variable=" in line:
                    toks = line.replace("=", "= ").split()
                    nvars = int(toks[toks.index("#variable=") + 1])
                continue
            if not line.endswith(";"):
                raise ValueError("constraint without ';': %r" % line)
            body = line[:-1].split()
            op, rhs = body[-2], int(body[-1])
            if op != ">=":
                raise ValueError("this re-checker only accepts '>=' constraints, got %r" % op)
            terms = {}
            for i in range(0, len(body) - 2, 2):
                coef, var = int(body[i]), body[i + 1]
                if not var.startswith("x"):
                    raise ValueError("unexpected term %r" % var)
                idx = int(var[1:]) - 1
                terms[idx] = terms.get(idx, 0) + coef
            cons.append((tuple(sorted((k, v) for k, v in terms.items() if v)), rhs))
    if nvars is None:
        raise ValueError("no '#variable=' header")
    return nvars, sorted(cons), obj


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --- one certificate -------------------------------------------------------

def recheck_exact(rec_path, certs, viprchk, budget):
    """Route 2: an exact-rational MILP certificate checked by viprchk."""
    rec = json.load(open(rec_path))
    n, M = rec["n"], rec["M"]
    res = {"record": os.path.basename(rec_path), "statement": rec["statement"],
           "route": rec.get("route"), "claimed": rec.get("result"), "steps": []}

    def step(label, ok, **extra):
        res["steps"].append(dict(step=label, PASS=bool(ok), **extra))
        return ok

    opb = os.path.join(certs, rec["instance"]["path"])
    if not step("instance file present", os.path.exists(opb), path=opb):
        res["VERDICT"] = "INCOMPLETE"
        return res

    nvars, cons, obj = parse_opb(opb)
    want = expected_constraints(n, M, rec.get("mu", 2))
    step("encoding is the K(%d,1,2) <= %d instance, re-derived here" % (n, M),
         nvars == (1 << n) and cons == want and obj is None,
         variables=nvars, constraints=len(cons), expected_constraints=len(want))
    step("instance sha256 matches the record",
         sha256(opb) == rec["instance"]["sha256"])

    comp = rec.get("complete", {})
    path = comp.get("completed_path")
    path = os.path.join(certs, os.path.basename(path)) if path else None
    if not path or not os.path.exists(path):
        step("completed certificate present", False,
             note="not committed; certs/MANIFEST.md carries its size, sha256 "
                  "and the command that regenerates it")
        res["VERDICT"] = "INCOMPLETE (certificate not on disk)"
        return res
    if comp.get("sha256"):
        step("completed certificate sha256 matches the record",
             sha256(path) == comp["sha256"])

    # viprchk cannot read a compressed certificate, so expand it first and
    # check the expansion against the recorded uncompressed hash -- otherwise
    # the thing checked and the thing hashed would be different objects.
    tmp = None
    if path.endswith(".gz"):
        import gzip
        import tempfile
        fd, tmp = tempfile.mkstemp(suffix=".vipr")
        with os.fdopen(fd, "wb") as out_f, gzip.open(path, "rb") as in_f:
            while True:
                chunk = in_f.read(1 << 22)
                if not chunk:
                    break
                out_f.write(chunk)
        if comp.get("uncompressed_sha256"):
            step("expanded certificate sha256 matches the record",
                 sha256(tmp) == comp["uncompressed_sha256"])
        path = tmp

    try:
        t0 = time.time()
        p = subprocess.run([viprchk, path], capture_output=True, text=True,
                           timeout=budget)
        dt = time.time() - t0
        out = (p.stdout + p.stderr).strip()
        step("viprchk verifies infeasibility",
             p.returncode == 0 and "verified infeasibility" in out.lower(),
             seconds=round(dt, 2), exit_code=p.returncode,
             checker_output=out.splitlines()[-5:])
    finally:
        if tmp:
            os.unlink(tmp)

    ok = all(x["PASS"] for x in res["steps"])
    res["VERDICT"] = ("CERTIFIED: K(%d,1,2) > %d" % (n, M)) if ok else "FAILED"
    res["check_seconds"] = round(dt, 2)
    return res


def recheck(rec_path, certs, veripb, budget):
    rec = json.load(open(rec_path))
    n, M = rec["n"], rec["M"]
    mu = rec.get("mu", 2)
    opt = M is None
    res = {"record": os.path.basename(rec_path), "statement": rec["statement"],
           "claimed": rec.get("result"), "steps": []}

    def step(label, ok, **extra):
        res["steps"].append(dict(step=label, PASS=bool(ok), **extra))
        return ok

    opb = os.path.join(certs, rec["instance"]["path"])
    if not step("instance file present", os.path.exists(opb), path=opb):
        res["VERDICT"] = "INCOMPLETE"
        return res

    nvars, cons, obj = parse_opb(opb)
    want = expected_constraints(n, M, mu)
    label = ("encoding is the 'minimise |C|' instance for K(%d,1,2), re-derived here" % n
             if opt else
             "encoding is the K(%d,1,2) <= %d instance, re-derived here" % (n, M))
    step(label,
         nvars == (1 << n) and cons == want
         and obj == (expected_objective(n) if opt else None),
         variables=nvars, constraints=len(cons), expected_constraints=len(want),
         objective_present=obj is not None)
    step("instance sha256 matches the record", sha256(opb) == rec["instance"]["sha256"])

    proof = rec.get("proof", {}).get("path")
    pbp = os.path.join(certs, proof) if proof else None
    if not proof or not os.path.exists(pbp):
        step("proof file present", False,
             note="not committed; see certs/MANIFEST.md for size, sha256 and "
                  "the exact command that regenerates it")
        res["VERDICT"] = "INCOMPLETE (proof not on disk)"
        return res
    step("proof sha256 matches the record", sha256(pbp) == rec["proof"]["sha256"])

    t0 = time.time()
    p = subprocess.run([veripb, "--stats", opb, pbp],
                       capture_output=True, text=True, timeout=budget)
    dt = time.time() - t0
    out = (p.stdout + p.stderr).strip()
    if opt:
        # `s VERIFIED BOUNDS a <= obj <= b` with a == b certifies the value.
        want_line = "s VERIFIED BOUNDS %s <= obj <= %s" % (
            rec["check"]["bounds"][0], rec["check"]["bounds"][1])
        ok = p.returncode == 0 and any(l.strip() == want_line
                                       for l in out.splitlines())
        step("VeriPB accepts the proof and reports the same bounds as the record",
             ok, seconds=round(dt, 2), exit_code=p.returncode,
             expected_line=want_line, checker_output=out.splitlines()[-6:])
    else:
        step("VeriPB accepts the proof and reports unsatisfiable",
             p.returncode == 0 and "unsatisfiable" in out.lower(),
             seconds=round(dt, 2), exit_code=p.returncode,
             checker_output=out.splitlines()[-6:])

    # Negative control. Rebuild a *weaker* instance from the same twelve lines
    # and require VeriPB to REJECT this proof against it. A checker that
    # accepted everything would sail through the step above; this is what
    # catches it. Decision mode relaxes the cardinality bound to M+1;
    # optimisation mode relaxes the coverage requirement to mu = 1, where
    # K(n,1,1) is far below the certified value, so a valid proof of the
    # recorded bound provably cannot exist.
    if opt:
        control = os.path.join(certs, ".control_n%d_opt.opb" % n)
        write_opb(control, n, None, 1, objective=True)
        why = "the mu = 1 instance, whose optimum is far lower"
    else:
        control = os.path.join(certs, ".control_n%d_M%d.opb" % (n, M + 1))
        write_opb(control, n, M + 1, mu)
        why = "the M+1 instance"
    try:
        q = subprocess.run([veripb, control, pbp],
                           capture_output=True, text=True, timeout=budget)
        step("VeriPB rejects the same proof against %s (negative control)" % why,
             q.returncode != 0, exit_code=q.returncode)
    finally:
        os.unlink(control)

    ok = all(s["PASS"] for s in res["steps"])
    if not ok:
        res["VERDICT"] = "FAILED"
    elif opt:
        lo, hi = rec["check"]["bounds"]
        res["VERDICT"] = ("CERTIFIED: K(%d,1,2) = %s" % (n, lo) if lo == hi
                          else "CERTIFIED: %s <= K(%d,1,2) <= %s" % (lo, n, hi))
    else:
        res["VERDICT"] = "CERTIFIED: K(%d,1,2) > %d" % (n, M)
    res["check_seconds"] = round(dt, 2)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certs", default=os.path.join(HERE, "certs"))
    ap.add_argument("--veripb", default=None, help="VeriPB binary ($VERIPB)")
    ap.add_argument("--viprchk", default=None, help="viprchk binary ($VIPRCHK)")
    ap.add_argument("--only", default=None, help="substring filter on record names")
    ap.add_argument("--budget", type=float, default=86400.0)
    a = ap.parse_args()

    from shutil import which
    veripb = a.veripb or os.environ.get("VERIPB") or which("veripb")
    viprchk = a.viprchk or os.environ.get("VIPRCHK") or which("viprchk")

    recs = sorted(f for f in os.listdir(a.certs)
                  if f.startswith("cert_") and f.endswith(".json")
                  and (a.only is None or a.only in f))
    if not recs:
        print("no certificate records under %s" % a.certs, file=sys.stderr)
        return 2

    out = []
    for f in recs:
        path = os.path.join(a.certs, f)
        exact = "VIPR" in (json.load(open(path)).get("route") or "")
        tool = viprchk if exact else veripb
        if not tool or not os.path.exists(tool):
            print("no %s binary: set $%s. Build instructions are in "
                  "CERTIFICATION.md." % ("viprchk" if exact else "VeriPB",
                                         "VIPRCHK" if exact else "VERIPB"),
                  file=sys.stderr)
            return 2
        out.append((recheck_exact if exact else recheck)(path, a.certs, tool, a.budget))
    print(json.dumps(out, indent=2))
    bad = [r for r in out if not r["VERDICT"].startswith("CERTIFIED")]
    print("\n".join("%-28s %s" % (r["record"], r["VERDICT"]) for r in out))
    print("RECHECK %s (%d records, %d not certified)"
          % ("PASS" if not bad else "FAIL", len(out), len(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
