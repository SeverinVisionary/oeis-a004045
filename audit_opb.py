#!/usr/bin/env python3
"""Third, from-scratch audit of the orbit-ILP .opb instances.

The certificates in certs_symmetry/ prove that a given .opb file is
infeasible. That is only worth something if the .opb file is the integer
program we claim it is. This script rebuilds every coverage row and the
cardinality row directly from the group action; it does NOT import
symcert_encode.py, the program that wrote the files.

Residual shared assumption, stated plainly: the variable-to-orbit map comes
from symcert_reps.orbits(perm, t), so this audit and the encoder agree on the
representative (perm, t) of each conjugacy class. That representative is
separately validated inside symcert_reps.validated_classes() (element order by
brute force, signed cycle type read back, orbit-stabilizer divisibility), and
any two representatives of one class give isomorphic ILPs by conjugation, so
the choice cannot change feasibility.

    python3 audit_opb.py [--dir certs_symmetry] [--ub 63]
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import symcert_reps as R  # noqa: E402

N = 8


def ball(v):
    """Closed radius-1 ball of v in Q_8: v itself plus its 8 neighbours."""
    return [v] + [v ^ (1 << i) for i in range(N)]


def parse_opb(path):
    """Return (coverage_rows, cardinality_row); rows are (terms, rhs) in >= form."""
    rows, card = [], None
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("*"):
            continue
        assert line.endswith(";"), line
        toks = line[:-1].split()
        rhs = int(toks[-1])
        assert toks[-2] == ">=", line
        terms = {}
        for coeff, var in zip(toks[0:-2:2], toks[1:-2:2]):
            terms[int(var[1:])] = int(coeff)
        if all(c < 0 for c in terms.values()):
            assert card is None, "two cardinality rows in %s" % path
            card = (terms, rhs)
        else:
            rows.append((terms, rhs))
    return rows, card


def audit_class(entry, opb_path, ub, mu=2):
    """Return a list of problems; empty means the instance is exactly right."""
    orbs = entry["orbits"]
    idx = {}
    for i, orbit in enumerate(orbs):
        for word in orbit:
            idx[word] = i + 1
    rows, card = parse_opb(opb_path)
    problems = []
    if len(rows) != 1 << N:
        problems.append("expected %d coverage rows, found %d" % (1 << N, len(rows)))
    for v in range(min(1 << N, len(rows))):
        expected = {}
        for u in ball(v):
            expected[idx[u]] = expected.get(idx[u], 0) + 1
        if (expected, mu) != rows[v]:
            problems.append("coverage row for vertex %d differs" % v)
    expected_card = ({i + 1: -len(o) for i, o in enumerate(orbs)}, -ub)
    if card != expected_card:
        problems.append("cardinality row differs")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(HERE, "certs_symmetry"))
    ap.add_argument("--ub", type=int, default=63)
    a = ap.parse_args()

    classes = {c["label"]: c for c in R.validated_classes()}
    checked, failed, skipped = 0, 0, 0
    for label in sorted(classes):
        path = os.path.join(a.dir, "inst_%s_ub%d.opb" % (label, a.ub))
        if not os.path.exists(path):
            skipped += 1
            continue
        problems = audit_class(classes[label], path, a.ub)
        checked += 1
        if problems:
            failed += 1
            print("%-16s FAIL" % label)
            for p in problems[:5]:
                print("    %s" % p)
            if len(problems) > 5:
                print("    ... and %d more" % (len(problems) - 5))
        else:
            print("%-16s OK  (%d orbits)" % (label, classes[label]["n_orbits"]))
    print("=== audited %d instances, %d failed, %d absent ==="
          % (checked, failed, skipped))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
