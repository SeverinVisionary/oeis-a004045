#!/usr/bin/env python3
"""Debug-only sanity check: parse a generic OPB file and solve it with
scipy.optimize.milp (HiGHS). NOT part of the certificate chain -- this is a
quick independent gut-check on the encoder's structure before spending
RoundingSat/VeriPB time, nothing here is ever quoted as a certificate.
"""
import argparse
import re
import sys

import numpy as np
from scipy.optimize import LinearConstraint, milp, Bounds
from scipy.sparse import csr_matrix

TERM_RE = re.compile(r"([+-]?\d+)\s*x(\d+)")


def parse_opb(path):
    nvars = 0
    rows = []  # (coeffs dict, rhs)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("*"):
                if line.startswith("*") and "#variable=" in line:
                    m = re.search(r"#variable=\s*(\d+)", line)
                    if m:
                        nvars = int(m.group(1))
                continue
            if ">=" not in line:
                continue
            lhs, rhs = line.split(">=")
            rhs = int(rhs.replace(";", "").strip())
            coeffs = {}
            for coef, var in TERM_RE.findall(lhs):
                coeffs[int(var) - 1] = int(coef)
            rows.append((coeffs, rhs))
    return nvars, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("opb")
    a = ap.parse_args()
    nvars, rows = parse_opb(a.opb)
    data, ri, ci = [], [], []
    lb = []
    for r, (coeffs, rhs) in enumerate(rows):
        for v, c in coeffs.items():
            data.append(c)
            ri.append(r)
            ci.append(v)
        lb.append(rhs)
    A = csr_matrix((data, (ri, ci)), shape=(len(rows), nvars))
    lb = np.array(lb, dtype=float)
    ub = np.full(len(rows), np.inf)
    constraints = LinearConstraint(A, lb, ub)
    bounds = Bounds(0, 1)
    integrality = np.ones(nvars)
    c = np.zeros(nvars)
    res = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    print("status:", res.status, res.message)
    print("success:", res.success)


if __name__ == "__main__":
    sys.exit(main())
