#!/usr/bin/env python3
"""M = 60 is impossible, hence K(8,1,2) >= 61.  INDEPENDENT VERIFICATION.

STATUS: the argument was proposed by an automated brainstorm leg and is
reconstructed and checked here from the mathematical statements alone. It has
NOT been reviewed by a human and NOT been through the review panel. It is not
in the claim ladder until it has. The dual multipliers quoted in the original
proposal do NOT verify (their combination leaves positive coefficients on
a_6, a_7, a_8); the LP value is instead certified here by an exact rational
solve of the active system.

The chain, for a double covering C of Q_n with |C| = M, c(y) = |B(y) cap C|,
g = c - 2, E = sum g = (n+1)M - 2^(n+1), S = {g >= 1}, s = |S|, Q = sum g^2,
and a_d = #{(x,z) in C^2 : d(x,z) = d} the ORDERED distance distribution:

 1. Every codeword has an over-covered word in its ball (the excess theorem),
    so  M <= sum_{y in S} c(y) = E + 2s,  giving s >= ceil((M-E)/2) = 16.
 2. Delsarte:  sum_d a_d K_k(d) >= 0  for all k -- valid for ANY subset of the
    cube, packing or covering.  Plus  sum_d a_d = M^2,  a_0 = M,  and the
    antipode row: every antipode of a NON-codeword is still doubly covered, so
        (n+1)M - (a_{n-1} + a_n) = sum_{u notin C} c(ubar) >= 2(2^n - M).
    Minimising a_1 + a_2 over these gives EXACTLY 347 (exact rational LP), and
    a_1 + a_2 is even, so a_1 + a_2 >= 348.
 3. Second moment:  sum_v c(v)^2 = (n+1)M + 2(a_1+a_2)  and also  = 4*2^n + 4E + Q,
    so  Q >= 100.
 4. Write g = 1 + h on S.  Then sum h = E - s and Q = 56 - s + sum h^2, so
    sum h^2 >= 44 + s.  With h <= 5 (i.e. NO word has c = 9) the maximum of
    sum h^2 is 5(E-s), and 44 + s > 5(28-s) for s >= 17.  At s = 16 the two
    sides are both 60, and equality needs every h in {0,5} with sum h = 12 --
    impossible, 5 does not divide 12.  So some y* has c(y*) = 9: B(y*) subset C.
 5. Translate y* to 0.  Then m_0 = 1, m_1 = n, sum_i m_i = M, the layer counts
        sum_{wt(v)=i} c(v) = m_i + (n+1-i)m_{i-1} + (i+1)m_{i+1} >= 2C(n,i),
    AND the layer capacities  0 <= m_i <= C(n,i).  The capacities are essential
    and were omitted in the first write-up: without m_8 <= 1 the continuous
    system has a fractional feasible point and "the LP is infeasible" is FALSE
    as stated.  With them there is a short exact certificate (LAYER_W below),
    and no LP solver is needed.  Contradiction at n=8, M=60.

MONOTONICITY (supplied by a review leg; the write-up had omitted it). Refuting
M = 60 refutes every M <= 60: coverage is monotone, so a double covering of size
k < 60 can be extended to one of size 60 by adding any 60 - k words not already
in C (possible since 60 < 256). Hence K(8,1,2) >= 61.

DISCRIMINATING TEST: the chain must kill only things that are actually
impossible.  It kills (4,7), (6,19), (8,59), (8,60) and leaves (4,8), (6,20),
(6,21), (8,61..64) open -- and K(4,1,2)=8, K(6,1,2)=20 are achievable.
"""
from fractions import Fraction as F
from math import comb, ceil
import itertools as it

def Kr(n, k, d):
    return sum((-1)**j * comb(d, j) * comb(n - d, k - j) for j in range(k + 1))

def antipode_cap(n, M):
    return (n + 1) * M - 2 * (2**n - M)

# ---------- step 2: exact dual certificate for min(a_1 + a_2) ----------
# The bound is certified by an explicit nonnegative combination, checked here in
# exact rationals, so no LP solver is trusted:
#
#   (1/16)(B_1 + B_2 + B_{n-1} + B_n) + 1*(antipode row) + (3/16)(sum_d a_d = M^2)
#
# collapses at n=8, M=60 to   3 a_0 + a_1 + a_2 - 527 >= 0,  i.e. a_1+a_2 >= 347.
def a12_certificate(n, M, y, ya, z):
    """Return the lower bound on a_1+a_2 proved by these multipliers, or None
    if they do not constitute a valid certificate."""
    coef = []
    for d in range(n + 1):
        c = sum(y.get(k, F(0)) * Kr(n, k, d) for k in range(1, n + 1)) + z
        if d >= n - 1: c -= ya
        coef.append(c)
    if any(v < 0 for v in y.values()) or ya < 0: return None
    if coef[1] != coef[2] or coef[1] <= 0: return None
    if any(coef[d] > 0 for d in range(3, n + 1)): return None   # dropped terms
    const = ya * antipode_cap(n, M) - z * M * M
    return (-const - coef[0] * M) / coef[1]

CERT = {8: (dict.fromkeys([1, 2, 7, 8], F(1, 16)), F(1), F(3, 16))}

def min_a1a2(n, M):
    if n in CERT:
        v = a12_certificate(n, M, *CERT[n])
        if v is not None: return v
    from scipy.optimize import linprog          # fallback for control cases
    nd = n + 1; c = [0]*nd; c[1] = 1; c[2] = 1
    A, b = [], []
    for k in range(1, n + 1):
        A.append([-Kr(n, k, d) for d in range(nd)]); b.append(0)
    r = [0]*nd; r[n-1] = 1; r[n] = 1; A.append(r); b.append(antipode_cap(n, M))
    res = linprog(c, A_ub=A, b_ub=b, A_eq=[[1]*nd], b_eq=[M*M],
                  bounds=[(M, M)] + [(0, None)]*(nd-1), method="highs")
    return F(res.fun).limit_denominator(10**6) if res.success else None

# ---------- step 5: solver-free Farkas certificate ----------
# Weight the layer inequalities by w and compare demand with supply. With
# w = (0,0,0,8,8,2,2,17,17) at n=8 the coefficient of m_j collapses to
# 0,0,48,48,48,48,48,48,153, so the 9 words of the full ball contribute NOTHING
# and the remaining M-9 contribute at most 48 each (153 for the unique weight-8
# word), against a demand of sum_i w_i 2C(8,i) = 2658. Hand-checkable; no LP.
LAYER_W = {8: [0, 0, 0, 8, 8, 2, 2, 17, 17]}

def layer_certificate(n, M):
    """True if the weighted layer count is contradictory (so no such code with
    a full ball exists). Returns (killed, demand, max_supply)."""
    w = LAYER_W.get(n)
    if w is None: return None, None, None
    demand = sum(w[i] * 2 * comb(n, i) for i in range(n + 1))
    coef = []
    for j in range(n + 1):
        c = w[j]
        if j + 1 <= n: c += (n - j) * w[j + 1]
        if j - 1 >= 0: c += j * w[j - 1]
        coef.append(c)
    assert coef[0] == 0 and coef[1] == 0, "ball words must contribute nothing"
    others = M - (n + 1)                      # codewords outside the full ball
    top = max(coef[2:n])                      # best non-antipodal contribution
    # capacity m_n <= C(n,n) = 1: at most ONE codeword can sit in the top layer,
    # which is exactly the constraint the first write-up omitted.
    assert comb(n, n) == 1
    supply = max(0, others - 1) * top + coef[n]
    return supply < demand, demand, supply

# ---------- step 5 cross-check: layer LP by integer enumeration ----------
def layer_feasible_int(n, M):
    rng = [range(0, comb(n, i) + 1) for i in range(2, n + 1)]
    for tail in it.product(*rng):
        m = [1, n] + list(tail)
        if sum(m) != M: continue
        ok = True
        for i in range(n + 1):
            cov = m[i] + ((n + 1 - i) * m[i - 1] if i >= 1 else 0) \
                       + ((i + 1) * m[i + 1] if i < n else 0)
            if cov < 2 * comb(n, i): ok = False; break
        if ok: return True, m
    return False, None

def full_ball_forced(n, M):
    # Step 1 rests on sum_{y in B(x)} c(y) = (n+1) + 2 N_2(x) being ODD, which
    # needs n+1 odd, i.e. n EVEN. At odd n it is false and the chain would
    # falsely kill achievable codes -- (3,4), (7,32), (7,33) all "fire" without
    # this guard. Found by an adversarial review leg; the original
    # discriminating test only covered even n and never exercised it.
    if n % 2 == 1:
        return False, "n odd: step 1's parity argument does not apply"
    N = 2**n; E = (n + 1) * M - 2 * N
    if E < 0: return True, "sphere bound"
    a12 = min_a1a2(n, M)
    if a12 is None: return True, "distance LP infeasible"
    a12 = 2 * ceil(a12 / 2)                      # a_1+a_2 is even
    Q = (n + 1) * M + 2 * a12 - 4 * N - 4 * E
    hmax = n - 2                                 # g <= n-1, h = g-1 <= n-2
    for s in range(max(0, ceil((M - E) / 2)), E + 1):
        H = E - s
        need = Q - 2 * E + s
        cap = (hmax - 1) * H
        if need > cap: continue                  # ball forced at this s
        if need == cap and H % (hmax - 1) != 0: continue
        return False, "s=%d survives (need %s <= cap %s)" % (s, need, cap)
    return True, "forced for every s (a1+a2>=%d, Q>=%s)" % (a12, Q)


if __name__ == "__main__":
    print("step 2 -- exact rational LP, min(a_1+a_2):")
    for n, M in [(8, 59), (8, 60), (8, 61), (8, 64), (6, 20)]:
        print("   n=%d M=%2d : %s" % (n, M, min_a1a2(n, M)))
    assert min_a1a2(8, 60) == 347, "the load-bearing LP value changed"
    assert a12_certificate(8, 60, *CERT[8]) == 347, "dual certificate broken"

    print("\nfull chain -- does it force a full ball, and is the layer LP then dead?")
    verdicts = {}
    CASES = [(4, 7), (4, 8), (6, 19), (6, 20), (6, 21),
             (8, 59), (8, 60), (8, 61), (8, 64),
             (3, 4), (5, 12), (7, 32), (7, 33)]          # odd n: must never fire
    for n, M in CASES:
        forced, why = full_ball_forced(n, M)
        if forced:
            if n in LAYER_W:
                killed, dem, sup = layer_certificate(n, M)
                why += "  [layer cert: supply %d vs demand %d]" % (sup, dem)
            else:
                feas, _ = layer_feasible_int(n, M)
                killed = not feas
        else:
            killed = False
        verdicts[(n, M)] = killed
        print("   n=%d M=%2d : forced=%-5s %-46s => %s"
              % (n, M, forced, why, "KILLED" if killed else "open"))

    # discriminating test: never kill an achievable code
    for achievable in [(4, 8), (6, 20), (6, 21), (8, 61), (8, 64),
                       (3, 4), (5, 12), (7, 32), (7, 33)]:
        assert not verdicts[achievable], "FALSE KILL at %s -- argument is wrong" % (achievable,)
    for impossible in [(4, 7), (6, 19), (8, 59), (8, 60)]:
        assert verdicts[impossible], "failed to kill %s" % (impossible,)
    k, d, sp = layer_certificate(8, 60)
    assert k and d == 2658 and sp == 2553, "layer certificate changed"
    print("\nstep 5 hand certificate at n=8, M=60: supply %d < demand %d" % (sp, d))
    print("discriminating test PASSED: kills exactly the impossible cases,")
    print("and never fires at odd n, where step 1's parity argument is invalid.")
    print("=> M=60 is refuted, hence K(8,1,2) >= 61  (UNREVIEWED, see docstring)")
