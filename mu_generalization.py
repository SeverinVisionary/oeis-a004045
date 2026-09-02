"""Verify the even-mu generalization of the excess bound.

Claim (professor leg, 2026-09-01): for even n, even mu, distinct codewords,
    K(n,1,mu) >= ceil( mu(mu+1) 2^n / ((mu+1)(n+1) - 1) ).
At mu=2 this must reduce to 3*2^(n+1)/(3n+2).
"""
from itertools import combinations
from math import ceil

def formula(n, mu):
    return -(-mu * (mu + 1) * 2**n // ((mu + 1) * (n + 1) - 1))

def mu2_formula(n):
    return -(-3 * 2**(n + 1) // (3 * n + 2))

# 1. algebraic reduction at mu=2
for n in range(2, 22, 2):
    a, b = formula(n, 2), mu2_formula(n)
    assert a == b, ("mu=2 reduction FAILS at n=%d: %d vs %d" % (n, a, b))
print("mu=2 reduction to the known formula: OK for n=2..20 even")

# 2. brute-force exact K(n,1,mu) for tiny n, compare to the bound
def ball(x, n):
    return [x] + [x ^ (1 << i) for i in range(n)]

def exact_K(n, mu, cap):
    pts = range(2**n)
    balls = {y: ball(y, n) for y in pts}
    for M in range(1, cap + 1):
        for C in combinations(pts, M):
            S = set(C)
            if all(sum(1 for z in balls[y] if z in S) >= mu for y in pts):
                return M
    return None

print("\n n  mu | bound  exact   verdict")
for n in (2, 4):
    for mu in (2, 4):
        cap = {2: 8, 4: 16}[n]
        lo = formula(n, mu)
        ex = exact_K(n, mu, cap)
        if ex is None:
            print(" %d  %d  | %4d    >%2d   (exact above search cap)" % (n, mu, lo, cap))
            continue
        ok = "VALID" + (" (tight)" if lo == ex else " (slack %d)" % (ex - lo))
        assert lo <= ex, "BOUND VIOLATED at n=%d mu=%d: %d > %d" % (n, mu, lo, ex)
        print(" %d  %d  | %4d   %4d   %s" % (n, mu, lo, ex, ok))

# 3. the parity step must be what does the work: odd mu should be able to violate
print("\n odd-mu control (formula applied where the parity step is invalid):")
for n in (2, 4):
    for mu in (1, 3):
        lo = formula(n, mu)
        ex = exact_K(n, mu, 16)
        flag = "  <-- exceeds exact" if (ex is not None and lo > ex) else ""
        print("  n=%d mu=%d: formula=%d exact=%s%s" % (n, mu, lo, ex, flag))
