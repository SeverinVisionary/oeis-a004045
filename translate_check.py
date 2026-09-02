#!/usr/bin/env python3
"""Is there a balanced double covering whose odd half is a TRANSLATE of its even half?

Ansatz: C = C_e u (C_e + v), with C_e a set of even-weight words and v of odd
weight (so C_e + v is odd and |C_o| = |C_e|).  The whole code is then determined
by C_e, giving a 2^(n-1)-variable feasibility problem per v.

Reduction: coordinate permutations map the family to itself and send v to any
vector of the same weight; translation by an EVEN word w sends C_e -> C_e + w
and fixes v.  So v matters only up to WEIGHT, leaving one instance per odd
weight.

Control: the same ansatz at n=6, M=20 must be FEASIBLE for some v -- K(6,1,2)=20
is achieved -- otherwise the model is wrong and the n=8 answer means nothing.
"""
import functools, sys, time
print = functools.partial(print, flush=True)
import numpy as np, highspy

def run(n, M, v, tl=600.0):
    N = 1 << n
    ev = [x for x in range(N) if bin(x).count('1') % 2 == 0]   # the free set
    pos = {x: i for i, x in enumerate(ev)}
    h = highspy.Highs(); h.setOptionValue("output_flag", False)
    h.setOptionValue("time_limit", tl)
    K = len(ev)
    h.addVars(K, np.zeros(K), np.ones(K))
    h.changeColsIntegrality(K, np.arange(K, dtype=np.int32),
                            np.array([highspy.HighsVarType.kInteger] * K))
    inf = highspy.kHighsInf
    # word u is in C iff (u even and u in C_e) or (u odd and u+v in C_e)
    def var_of(u):
        return pos[u] if bin(u).count('1') % 2 == 0 else pos[u ^ v]
    for x in range(N):                       # coverage: |B(x) cap C| >= 2
        coef = {}
        for u in [x] + [x ^ (1 << i) for i in range(n)]:
            coef[var_of(u)] = coef.get(var_of(u), 0) + 1
        idx = np.array(list(coef), dtype=np.int32)
        val = np.array([float(c) for c in coef.values()])
        h.addRow(2.0, inf, len(idx), idx, val)
    h.addRow(float(M // 2), float(M // 2), K, np.arange(K, dtype=np.int32), np.ones(K))
    t = time.time(); h.run(); el = time.time() - t
    return h.modelStatusToString(h.getModelStatus()), el

def check(n, M):
    N = 1 << n
    print("=== n=%d, M=%d, translate ansatz (one instance per odd weight) ===" % (n, M))
    any_feas = False
    for w in range(1, n, 2):
        v = (1 << w) - 1                       # representative of weight w
        st, el = run(n, M, v)
        print("   wt(v)=%d: %-14s %5.1fs" % (w, st, el))
        if "nfeasible" not in st and "imit" not in st: any_feas = True
    return any_feas

feas6 = check(6, 20)
if not feas6:
    sys.exit("CONTROL FAILED: no translate-type 20-word cover at n=6; model is void")
print("   control PASSES: a translate-type cover exists at n=6, M=20.\n")

feas8 = check(8, 60)
print()
print("RESULT: at n=8, M=60 the translate ansatz is %s"
      % ("FEASIBLE -- claim refuted" if feas8 else "INFEASIBLE for every odd weight"))
