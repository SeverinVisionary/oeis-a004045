#!/usr/bin/env python3
"""Independent verification of the elementary lower bound, for EVEN n,
    K(n,1,2) >= ceil(3*2^(n+1)/(3n+2)).

Written from the statement of the argument, not from its author's code.

  g(x) = c(x) - 2 >= 0,  E = sum_x g(x) = (n+1)M - 2^(n+1)
  Step 1: |B(u) cap B(v)| = 2 if d(u,v) in {1,2}, else 0   (u != v)
  Step 2: x in C  ==>  sum_{y in B(x)} c(y) = (n+1) + 2*N2(x) is ODD for n even,
          hence >= 2(n+1)+1, hence sum_{y in B(x)} g(y) >= 1.
  Step 3: S = {g >= 1}, s = |S| <= E.  I = #{(x,y): x in C, y in B(x) cap S}
          M <= I = sum_{y in S} c(y) = E + 2s <= 3E.
  Step 4: M <= 3((n+1)M - 2^(n+1))  ==>  M >= 3*2^(n+1)/(3n+2).
"""
import itertools, random, sys
from math import ceil
from fractions import Fraction

def ball(v, n):
    return [v] + [v ^ (1 << i) for i in range(n)]

# ---- Step 1: intersection numbers, checked exhaustively for n = 4, 6, 8 ----
def check_step1(n):
    N = 1 << n
    for u in range(N):
        Bu = set(ball(u, n))
        for v in range(u + 1, N):
            d = bin(u ^ v).count('1')
            k = len(Bu & set(ball(v, n)))
            want = 2 if d in (1, 2) else 0
            if k != want:
                return "FAIL n=%d u=%d v=%d d=%d got %d want %d" % (n, u, v, d, k, want)
    return "ok"

# ---- Steps 2-4 on actual double coverings ----
def cov(C, n):
    N = 1 << n
    c = [0] * N
    for u in C:
        for y in ball(u, n):
            c[y] += 1
    return c

def check_code(C, n):
    """Return None if every claim holds on this double covering, else a failure string."""
    N, S_ = 1 << n, set(C)
    c = cov(C, n)
    if min(c) < 2:
        return None                      # not a double covering; skip
    M = len(S_)
    g = [ci - 2 for ci in c]
    E = sum(g)
    if E != (n + 1) * M - 2 * N:
        return "E identity failed"
    for x in S_:                          # Step 2
        tot = sum(c[y] for y in ball(x, n))
        N2 = sum(1 for u in S_ if 1 <= bin(u ^ x).count('1') <= 2)
        if tot != (n + 1) + 2 * N2:
            return "Step2 ball-sum identity failed at %d" % x
        if n % 2 == 0 and tot % 2 == 0:
            return "Step2 parity failed at %d" % x
        if sum(g[y] for y in ball(x, n)) < 1:
            return "Step2 conclusion failed at %d" % x
    Sset = [y for y in range(N) if g[y] >= 1]  # Step 3
    s = len(Sset)
    I = sum(1 for x in S_ for y in ball(x, n) if g[y] >= 1)
    if not (s <= E):                   return "s <= E failed"
    if not (M <= I):                   return "M <= I failed"
    if I != sum(c[y] for y in Sset):   return "I double-count failed"
    if sum(c[y] for y in Sset) != E + 2 * s: return "E+2s failed"
    if not (M <= 3 * E):               return "M <= 3E failed"
    if M < bound(n):                   return "BOUND VIOLATED: M=%d < %d" % (M, bound(n))
    return None

def bound(n):
    return ceil(Fraction(3 * (1 << (n + 1)), 3 * n + 2))

def random_cover(n, seed):
    """Greedy-then-repair random double covering."""
    rng = random.Random(seed)
    N = 1 << n
    C = set(rng.sample(range(N), N // 3))
    while True:
        c = cov(C, n)
        bad = [x for x in range(N) if c[x] < 2]
        if not bad: return sorted(C)
        x = rng.choice(bad)
        C.add(rng.choice([y for y in ball(x, n) if y not in C]))

print("=== Step 1 (intersection numbers), exhaustive ===")
for n in (4, 6, 8):
    print("  n=%d: %s" % (n, check_step1(n)))

print("\n=== bound values vs published K(n,1,2) ===")
# The bound is valid ONLY for even n: Step 2 needs |B| = n+1 odd, so that a sum
# of nine terms each >= 2 which is forced odd must be >= 19.  For odd n the ball
# sum is even and no round-up occurs.  Printing the formula at odd n as well is
# the discriminating test: it must VIOLATE the known values there, and it does
# (n=3 gives 5 > K=4; n=7 gives 34 > K=32).  If it happened to hold at odd n we
# would have to suspect the parity step of being unnecessary -- i.e. of being
# mis-stated.
known = {2: 3, 3: 4, 4: 8, 5: 12, 6: 20, 7: 32, 8: "59..64"}
odd_violations = []
for n in range(2, 9):
    b, k = bound(n), known.get(n)
    if n % 2:
        viol = isinstance(k, int) and b > k
        odd_violations.append(viol)
        print("  n=%d: N/A (odd n: no parity round-up) -- formula %d vs K=%d%s"
              % (n, b, k, "  <-- exceeds the true value, as it may" if viol else "  (coincides)"))
    else:
        print("  n=%d: bound >= %2d   known %s%s"
              % (n, b, k, "  <-- EXACT" if k == b else ""))

assert any(odd_violations), ("control failed: the formula never exceeds a known "
    "odd-n value, so this run does not witness that the parity step is load-bearing")
print("  -> the parity step is load-bearing: at n=3 and n=7 the formula exceeds the")
print("     true K(n,1,2), so it is NOT a valid bound without |B| odd.")

print("\n=== exhaustive: ALL double coverings of F_2^4 up to size 9 ===")
n, N, cnt, fails = 4, 16, 0, 0
for k in range(bound(4), 10):
    for C in itertools.combinations(range(N), k):
        c = cov(C, n)
        if min(c) < 2: continue
        cnt += 1
        r = check_code(list(C), n)
        if r: fails += 1; print("   ", r)
print("  %d double coverings checked, %d failures" % (cnt, fails))

print("\n=== random double coverings, n=4 and n=6 ===")
for n in (4, 6):
    f = 0
    for seed in range(300):
        r = check_code(random_cover(n, seed), n)
        if r: f += 1; print("   n=%d %s" % (n, r))
    print("  n=%d: 300 covers, %d failures" % (n, f))
sys.exit(1 if fails else 0)
