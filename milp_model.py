#!/usr/bin/env python3
"""MILP search model for K(n,1,2), independent of sat_model.py.

    python3 milp_model.py --mode opt --budget 3600     # optimise, track dual bound
    python3 milp_model.py --mode 63  --budget 3600     # feasibility at |C| <= 63

min sum_c x_c  s.t.  sum_{c in B(v)} x_c >= 2  for all v,  x binary.
The LP relaxation is 2*2^n/(n+1) exactly (uniform x_c = 2/(n+1) is optimal), so
the root gap is large and every unit of dual bound comes from cuts.

Requires: highspy.
"""
import argparse
import json
import time

import highspy
import numpy as np


def run(n, mode, budget, threads=1):
    N = 1 << n
    inf = highspy.kHighsInf
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", threads)
    h.setOptionValue("time_limit", budget)
    h.addVars(N, np.zeros(N), np.ones(N))
    # "opt" and "lp" minimise |C|; a numeric mode is pure feasibility.
    cost = np.ones(N) if mode in ("opt", "lp") else np.zeros(N)
    h.changeColsCost(N, np.arange(N, dtype=np.int32), cost)
    if mode != "lp":
        h.changeColsIntegrality(
            N, np.arange(N, dtype=np.int32),
            np.array([highspy.HighsVarType.kInteger] * N))
    for v in range(N):
        idx = np.array([v] + [v ^ (1 << i) for i in range(n)], dtype=np.int32)
        h.addRow(2.0, inf, len(idx), idx, np.ones(len(idx)))
    if mode not in ("opt", "lp"):
        h.addRow(-inf, float(mode), N, np.arange(N, dtype=np.int32), np.ones(N))
    t0 = time.time()
    h.run()
    dt = time.time() - t0
    info = h.getInfo()
    out = {
        "n": n, "mode": mode,
        "status": h.modelStatusToString(h.getModelStatus()),
        "objective": h.getObjectiveValue(),
        "dual_bound": getattr(info, "mip_dual_bound", None),
        "nodes": getattr(info, "mip_node_count", None),
        "seconds": round(dt, 1),
    }
    code = None
    if mode != "lp":
        y = np.array(h.getSolution().col_value)
        if y.size and y.sum() > 0:
            code = sorted(int(j) for j in range(N) if y[j] > 0.5)
    return out, code


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--mode", default="opt", help="opt | lp | an integer bound on |C|")
    ap.add_argument("--budget", type=float, default=600.0)
    ap.add_argument("-o", default=None)
    a = ap.parse_args()
    out, code = run(a.n, a.mode, a.budget)
    print(json.dumps(out))
    if code and a.o:
        json.dump(code, open(a.o, "w"))
        print("wrote", a.o, "size", len(code))
