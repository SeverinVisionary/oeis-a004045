#!/usr/bin/env python3
"""Do the Step-2 cuts shrink the search, and hence the proof?

Cut, one per word x (n EVEN):   W(x) + (n/2)*x_x >= n+1,
                                W(x) = sum_{1<=d(y,x)<=2} x_y.

Validity, from the ball identity:
  x not in C: sum_{y in B(x)} c(y) = 2*#{c' in C : d(c',x)<=2} = 2*W(x); each of
              the n+1 terms is >= 2, so 2W >= 2(n+1), i.e. W >= n+1.
  x in C:     the same sum is (n+1) + 2*N_2(x), forced ODD (n even) and
              >= 2(n+1), hence >= 2(n+1)+1, so W(x) = N_2(x) >= (n+2)/2.
Both branches give W(x) + (n/2)*x_x >= n+1, since (n+2)/2 + n/2 = n+1.

The constants are n-DEPENDENT.  Hard-coding the n=8 values (4 and 9) makes the
cut invalid at n=6, where it wrongly refutes the achievable M=20 -- which is
exactly what the control below is for.

It is CUTTING-PLANES derivable from the original rows in two steps -- add the 9
ball rows of B(x) (giving 9*x_x + 2W >= 18), subtract x_x <= 1, divide by 2 --
so a VeriPB proof may use it while remaining a proof about the unaugmented OPB.
Node count is the proxy for proof size that we can measure cheaply.
"""
import functools, time
print = functools.partial(print, flush=True)
import numpy as np, highspy

def solve(n, M, cuts, tl=5400.0):
    N = 1 << n; inf = highspy.kHighsInf
    h = highspy.Highs(); h.setOptionValue("output_flag", False)
    h.setOptionValue("time_limit", tl)
    h.addVars(N, np.zeros(N), np.ones(N))
    h.changeColsIntegrality(N, np.arange(N, dtype=np.int32),
                            np.array([highspy.HighsVarType.kInteger] * N))
    for v in range(N):
        idx = np.array(sorted([v] + [v ^ (1 << i) for i in range(n)]), dtype=np.int32)
        h.addRow(2.0, inf, len(idx), idx, np.ones(len(idx)))
    h.addRow(-inf, float(M), N, np.arange(N, dtype=np.int32), np.ones(N))
    if cuts:
        for x in range(N):
            w = sorted({x ^ (1 << i) for i in range(n)} |
                       {x ^ (1 << i) ^ (1 << j) for i in range(n) for j in range(n) if i != j})
            coef = {y: 1.0 for y in w}; coef[x] = coef.get(x, 0.0) + n / 2.0
            idx = np.array(list(coef), dtype=np.int32)
            h.addRow(float(n + 1), inf, len(idx), idx, np.array(list(coef.values())))
    t = time.time(); h.run(); el = time.time() - t
    return h.modelStatusToString(h.getModelStatus()), el, h.getInfo().mip_node_count

print("=== control: n=6, M=20 with cuts must stay FEASIBLE ===")
s, el, nd = solve(6, 20, True)
print("   %-12s %5.1fs nodes=%s" % (s, el, nd))
assert "nfeasible" not in s, "CONTROL FAILED: cuts kill an achievable size -- they are invalid"
print("   control passes.\n")

for M in (58, 59, 60):
    for cuts in (False, True):
        s, el, nd = solve(8, M, cuts)
        print("  n=8 M=%d cuts=%-5s  %-12s %7.1fs  nodes=%s" % (M, cuts, s, el, nd))
