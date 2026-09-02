#!/usr/bin/env python3
"""Third, independent model: SCIP feasibility for K(n,1,2) <= M.

Deliberately a separate code base from milp_model.py (HiGHS) and sat_model.py
(CaDiCaL). Every infeasibility reading in the pilot was taken twice, once here
and once in HiGHS, because a single floating-point branch-and-bound status is
not a verdict.

    python3 scip_model.py --M 59 --budget 3600 --n 8

Requires: pyscipopt. Witnesses must still go through verify.py.
"""
import argparse
import json
import time

from pyscipopt import Model


def run(n, M, budget):
    N = 1 << n
    m = Model()
    m.hideOutput()
    m.setParam("limits/time", budget)
    x = [m.addVar(vtype="B", name="x%d" % v) for v in range(N)]
    for v in range(N):
        b = [v] + [v ^ (1 << i) for i in range(n)]
        m.addCons(sum(x[c] for c in b) >= 2)
    m.addCons(sum(x) <= M)
    t0 = time.time()
    m.optimize()
    out = {"solver": "SCIP", "n": n, "M": M, "status": m.getStatus(),
           "seconds": round(time.time() - t0, 1), "nodes": m.getNNodes()}
    code = None
    if m.getNSols() > 0:
        s = m.getBestSol()
        code = sorted(v for v in range(N) if m.getSolVal(s, x[v]) > 0.5)
    return out, code


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--budget", type=float, default=3600.0)
    ap.add_argument("-o", default=None)
    a = ap.parse_args()
    out, code = run(a.n, a.M, a.budget)
    print(json.dumps(out))
    if code and a.o:
        json.dump(code, open(a.o, "w"))
        print("wrote", a.o, "size", len(code))
