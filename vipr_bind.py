#!/usr/bin/env python3
"""Bind a VIPR certificate to the .opb instance it is supposed to be about.

viprchk is invoked as `viprchk cert.vipr` -- it never sees the .opb. So it
proves infeasibility of whatever problem the certificate's own header states,
which is only the claim we want if that header really is our instance. This
script closes that gap: it parses both files and checks they describe the
same integer program.

Checks performed:
  * every OPB variable appears in the VIPR VAR section, and the VIPR name
    encodes which OPB variable it is (SCIP writes "t_x<k>" for OPB "x<k>");
    an unparseable name is a hard failure, never an assumption
  * the VIPR INT section marks every variable integer (not an LP relaxation)
  * the VIPR bound constraints are exactly 0 <= x_i <= 1 for every variable
  * the multiset of non-bound VIPR constraints equals the multiset of OPB
    constraints, after normalising both to ">=" form
  * the VIPR RTP line claims infeasibility

    python3 vipr_bind.py instance.opb certificate.vipr
"""
import argparse
import re
import sys
from collections import Counter


def parse_opb(path):
    """Return (nvars, [(rhs, {var1based: coef}) ...]) with every row in >= form."""
    nvars = None
    rows = []
    for line in open(path):
        s = line.strip()
        if not s:
            continue
        if s.startswith("*"):
            m = re.search(r"#variable=\s*(\d+)", s)
            if m:
                nvars = int(m.group(1))
            continue
        if s.startswith("min:") or s.startswith("max:"):
            continue  # objective; infeasibility does not depend on it
        assert s.endswith(";"), "unterminated OPB line: %s" % s
        toks = s[:-1].split()
        sense, rhs = toks[-2], int(toks[-1])
        assert sense in (">=", "="), "unsupported OPB sense %r" % sense
        terms = {}
        for coef, var in zip(toks[0:-2:2], toks[1:-2:2]):
            assert var.startswith("x"), var
            terms[int(var[1:])] = terms.get(int(var[1:]), 0) + int(coef)
        rows.append((rhs, terms))
        if sense == "=":
            rows.append((-rhs, {k: -v for k, v in terms.items()}))
    return nvars, rows


def parse_vipr(path):
    """Return (varnames, int_indices, constraints, rtp).

    constraints is a list of (name, sense, rhs, {index0based: coef}).
    """
    toks = []
    with open(path) as f:
        for line in f:
            toks.extend(line.split())
    i = 0

    def take():
        nonlocal i
        v = toks[i]
        i += 1
        return v

    assert take() == "VER"
    take()
    assert take() == "VAR", "expected VAR section"
    nvar = int(take())
    names = [take() for _ in range(nvar)]
    assert take() == "INT", "expected INT section"
    nint = int(take())
    ints = [int(take()) for _ in range(nint)]
    assert take() == "OBJ"
    take()  # min/max
    nobj = int(take())
    for _ in range(nobj):
        take(); take()
    assert take() == "CON", "expected CON section"
    ncon = int(take())
    take()  # number of bound constraints (informational)
    cons = []
    for _ in range(ncon):
        name = take()
        sense = take()
        rhs = int(take())
        nt = int(take())
        terms = {}
        for _ in range(nt):
            idx = int(take())
            coef = int(take())
            terms[idx] = terms.get(idx, 0) + coef
        cons.append((name, sense, rhs, terms))
    assert take() == "RTP", "expected RTP section"
    rtp = take()
    return names, ints, cons, rtp


def to_ge(sense, rhs, terms):
    """Normalise one constraint to >= form; returns a hashable canonical key."""
    if sense == "L":
        rhs, terms = -rhs, {k: -v for k, v in terms.items()}
    elif sense != "G":
        raise AssertionError("unsupported VIPR sense %r (E must be split)" % sense)
    return (rhs, tuple(sorted((k, v) for k, v in terms.items() if v != 0)))


def check(opb_path, vipr_path):
    """Return a list of problems; empty means the certificate is bound to the OPB."""
    nvars, opb_rows = parse_opb(opb_path)
    names, ints, cons, rtp = parse_vipr(vipr_path)
    problems = []

    if rtp != "infeas":
        problems.append("VIPR RTP is %r, not 'infeas' -- this certificate does not "
                        "claim infeasibility" % rtp)

    idx_to_opb = {}
    for i, nm in enumerate(names):
        m = re.fullmatch(r"t?_?x(\d+)", nm)
        if not m:
            problems.append("VIPR variable %d is named %r; cannot bind it to an OPB "
                            "variable" % (i, nm))
            continue
        idx_to_opb[i] = int(m.group(1))
    if nvars is not None and len(names) != nvars:
        problems.append("OPB declares %d variables, VIPR has %d" % (nvars, len(names)))
    if len(set(idx_to_opb.values())) != len(idx_to_opb):
        problems.append("two VIPR variables map to the same OPB variable")
    if len(ints) != len(names):
        problems.append("VIPR marks %d of %d variables integer -- the certificate is "
                        "about a relaxation" % (len(ints), len(names)))
    if problems:
        return problems

    bounds, real = [], []
    for name, sense, rhs, terms in cons:
        (bounds if len(terms) == 1 and abs(next(iter(terms.values()))) == 1
         and rhs in (0, 1, -1) and name.startswith("B") else real).append(
            (name, sense, rhs, terms))

    seen_lo, seen_hi = set(), set()
    for name, sense, rhs, terms in bounds:
        (idx, _), = terms.items()
        key = to_ge(sense, rhs, terms)
        if key == (0, ((idx, 1),)):
            seen_lo.add(idx)
        elif key == (-1, ((idx, -1),)):
            seen_hi.add(idx)
        else:
            problems.append("bound %s on variable %d is not 0<=x<=1" % (name, idx))
    missing = set(range(len(names))) - seen_lo
    if missing:
        problems.append("%d variables have no lower bound 0 in the certificate"
                        % len(missing))
    missing = set(range(len(names))) - seen_hi
    if missing:
        problems.append("%d variables have no upper bound 1 in the certificate"
                        % len(missing))

    want = Counter(to_ge("G", rhs, terms) for rhs, terms in opb_rows)
    got = Counter()
    for name, sense, rhs, terms in real:
        mapped = {idx_to_opb[i]: c for i, c in terms.items()}
        got[to_ge(sense, rhs, mapped)] += 1

    only_opb = want - got
    only_vipr = got - want
    if only_opb:
        problems.append("%d OPB constraint(s) absent from the certificate, e.g. %r"
                        % (sum(only_opb.values()), next(iter(only_opb))))
    if only_vipr:
        problems.append("%d certificate constraint(s) not in the OPB, e.g. %r"
                        % (sum(only_vipr.values()), next(iter(only_vipr))))
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("opb")
    ap.add_argument("vipr")
    a = ap.parse_args()
    problems = check(a.opb, a.vipr)
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("BOUND: %s <-> %s" % (a.opb, a.vipr))
    return 0


if __name__ == "__main__":
    sys.exit(main())
