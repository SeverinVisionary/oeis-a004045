#!/usr/bin/env python3
"""Why HHKL 1993's own excess bound cannot produce our mu=2 result.

This is the load-bearing novelty argument, and unlike a failed literature
search it is CHECKABLE. Read from the primary text (Hamalainen, Honkala,
Kaikkonen, Litsyn, "Bounds for binary multiple covering codes", Des. Codes
Cryptogr. 3 (1993) 251-275), not from a summary.

Their Theorem 6, p.259:

    K(n,r,mu) >= ( mu(n+1-k) + eps ) 2^n / ( (n+1-k)V(n,r) + eps V(n,r-1) )

with, from their Lemma 1,
    eps := (r+1) * ceil( mu(n+1)/(r+1) ) - mu(n+1)
and, from their Lemma 3, k the smallest integer with mu+1 <= C(k,r).

eps is their parity/round-up term -- the entire gain over the sphere bound.
At r = 1 it is (n+1)mu rounded up to the next even number, minus (n+1)mu:

    eps = 0  <=>  mu(n+1) is even.

For EVEN n, n+1 is odd, so eps = 0 exactly when mu is EVEN. When eps = 0 the
whole bound collapses algebraically to the sphere-covering bound mu*2^n/V(n,r).

That is why their Corollary 2 (p.259) is stated only for "mu <= n odd and n
even": their method has nothing to say at even mu. Our argument uses a
DIFFERENT parity -- the ball sum at a CODEWORD,
    sum_{y in B(x)} c(y) = (n+1) + 2*N_2(x),
odd whenever n is even, for EVERY mu -- and so fires precisely where theirs
vanishes.
"""
from math import comb, ceil
from fractions import Fraction as F


def V(n, r):
    return sum(comb(n, i) for i in range(r + 1))


def eps(n, r, mu):
    return (r + 1) * ceil(mu * (n + 1) / (r + 1)) - mu * (n + 1)


def hhkl_thm6(n, r, mu):
    e = eps(n, r, mu)
    k = next(j for j in range(1, 500) if mu + 1 <= comb(j, r))
    return F((mu * (n + 1 - k) + e) * 2**n, (n + 1 - k) * V(n, r) + e * V(n, r - 1))


def sphere(n, r, mu):
    return F(mu * 2**n, V(n, r))


def ours(n):
    return F(6 * 2**n, 3 * n + 2)


def ceil_f(x):
    return -((-x.numerator) // x.denominator)


# --- 1. eps vanishes exactly at even mu, for even n, r=1 ---
for n in range(4, 40, 2):
    for mu in range(1, 12):
        assert (eps(n, 1, mu) == 0) == (mu % 2 == 0), (n, mu)
print("eps(n,1,mu) = 0  <=>  mu even, for every even n tested: OK")

# --- 2. and then Theorem 6 IS the sphere bound, identically ---
# (restricted to mu < n, where k = mu+1 < n+1 keeps the denominator positive;
#  HHKL's own Corollary 2 carries the same mu <= n hypothesis)
for n in range(4, 40, 2):
    for mu in range(2, n, 2):
        assert hhkl_thm6(n, 1, mu) == sphere(n, 1, mu), (n, mu)
print("at even mu, HHKL Thm 6 == sphere bound exactly (not merely close): OK")

# --- 3. so at mu=2 their machinery cannot reach our values ---
print("\n  n | HHKL Thm6 | sphere | HHKL published LB | ours | ")
HHKL_TABLE_MU2 = {6: 19, 8: 58, 10: 187, 12: 631, 14: 2186, 16: 7711}
for n in sorted(HHKL_TABLE_MU2):
    t6 = hhkl_thm6(n, 1, 2)
    assert t6 == sphere(n, 1, 2)
    assert ceil_f(t6) <= HHKL_TABLE_MU2[n]
    print("  %2d | %9d | %6d | %17d | %4d |"
          % (n, ceil_f(t6), ceil_f(sphere(n, 1, 2)), HHKL_TABLE_MU2[n], ceil_f(ours(n))))
print("""
  HHKL Table 5 Part I marks lower bounds by method: 'c' = their Theorem 6.
  NO mu=2 entry carries 'c'. n=6 and n=10 are unmarked (= sphere bound);
  n=8's 58 is marked 'a' = their inequalities (1) and (2), the weight-split
  refinement of the sphere bound, NOT the excess bound. Consistent with the
  collapse proved above.""")

# --- 4. their Corollary 2 is explicitly odd-mu, and does not apply at mu=2 ---
def hhkl_cor2(n, mu):
    """K(n,1,mu) >= (mu(n-mu)+1)2^n / ((n-mu)(n+1)+1), stated for mu odd, n even."""
    return F((mu * (n - mu) + 1) * 2**n, (n - mu) * (n + 1) + 1)

for n in (6, 8, 10, 12):
    for mu in (1, 3, 5):
        assert hhkl_cor2(n, mu) > sphere(n, 1, mu), (n, mu)
print("Corollary 2 beats the sphere bound at odd mu (its stated hypothesis): OK")
print("It is not stated for, and its derivation does not cover, even mu.")
