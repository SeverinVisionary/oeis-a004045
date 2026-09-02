#!/usr/bin/env python3
"""Does the weight-split reduction make the M=60 refutation cheaper?

Baseline: the plain decision instance "is there a double covering of F_2^8 with
at most M codewords?" -- exactly pb_encode.py's formulation (2^n binary vars,
one ball row >= 2 per word, one cardinality row <= M).

Reduced: the same, plus M_e = 30 and M_o = 30 as EQUALITIES.  Those are not free
-- they are licensed by the elementary argument, which kills the other four
splits at M=60.  So this measures the residual case only.

Control: the same reduction at n=6, M=20, split (10,10), which MUST be FEASIBLE
(K(6,1,2)=20 is achieved).  If the control comes back infeasible the encoding is
wrong and every other number here is void.
"""
import sys, time
import numpy as np, highspy

def build(n, M, split=None, tl=1800.0):
    N = 1 << n
    inf = highspy.kHighsInf
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("time_limit", tl)
    h.addVars(N, np.zeros(N), np.ones(N))
    h.changeColsIntegrality(N, np.arange(N, dtype=np.int32),
                            np.array([highspy.HighsVarType.kInteger] * N))
    for v in range(N):                                   # coverage
        idx = np.array(sorted([v] + [v ^ (1 << i) for i in range(n)]), dtype=np.int32)
        h.addRow(2.0, inf, len(idx), idx, np.ones(len(idx)))
    h.addRow(-inf, float(M), N, np.arange(N, dtype=np.int32), np.ones(N))   # |C| <= M
    if split is not None:
        Me, Mo = split
        ev = np.array([v for v in range(N) if bin(v).count('1') % 2 == 0], dtype=np.int32)
        od = np.array([v for v in range(N) if bin(v).count('1') % 2 == 1], dtype=np.int32)
        h.addRow(float(Me), float(Me), len(ev), ev, np.ones(len(ev)))
        h.addRow(float(Mo), float(Mo), len(od), od, np.ones(len(od)))
    t = time.time(); h.run(); el = time.time() - t
    st = h.getModelStatus()
    return h.modelStatusToString(st), el, h.getInfo().mip_node_count

print("=== CONTROL FIRST: n=6, M=20, split (10,10) must be FEASIBLE ===")
s, el, nd = build(6, 20, (10, 10))
print("  status=%-14s %6.1fs  nodes=%s" % (s, el, nd))
if "nfeasible" in s:
    sys.exit("CONTROL FAILED: encoding calls an achievable size infeasible; results void")
print("  control passes.\n")

print("=== n=8, M=60 ===")
for label, split in (("baseline (no split)", None), ("reduced to (30,30)", (30, 30))):
    s, el, nd = build(8, 60, split)
    print("  %-22s status=%-14s %7.1fs  nodes=%s" % (label, s, el, nd))
