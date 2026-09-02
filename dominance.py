#!/usr/bin/env python3
"""Does the excess bound beat Krotov-Potapov Thm 6 at mu=2 for EVERY even n?

The repo tabulates the comparison at n = 4,6,8,10,12,16,20. A table is not a
theorem. This settles it in closed form, with exact rational arithmetic as the
check.

Excess bound (even n):        L(n)  = 6*2^n / (3n+2)
Krotov-Potapov Thm 6, mu=2, tau=0:
   (a) n = 0 mod 4:           KPa(n) = 2^n (2n+6) / (n(n+4))
   (c) n = 2 mod 4:           KPc(n) = 2^n (2n+2) / (n(n+2))

Claimed identities, before any ceiling:

   L - KPa = 2^n (2n - 12) / [ n(n+4)(3n+2) ]
   L - KPc = 2^n (2n -  4) / [ n(n+2)(3n+2) ]

so the sign is decided by 2n-12 and 2n-4 alone.
"""
from fractions import Fraction as F

def L(n):   return F(6 * 2**n, 3*n + 2)
def KPa(n): return F(2**n * (2*n + 6), n * (n + 4))
def KPc(n): return F(2**n * (2*n + 2), n * (n + 2))
def KP(n):  return KPa(n) if n % 4 == 0 else KPc(n)

def ceil_f(x):  # ceiling of a Fraction
    return -((-x.numerator) // x.denominator)

# --- 1. the two closed-form identities, exactly, over a wide range ---
for n in range(4, 4002, 2):
    if n % 4 == 0:
        assert L(n) - KPa(n) == F(2**n * (2*n - 12), n*(n+4)*(3*n+2)), n
    else:
        assert L(n) - KPc(n) == F(2**n * (2*n -  4), n*(n+2)*(3*n+2)), n
print("identities verified exactly for all even n in [4, 4000]")

# --- 2. therefore the sign is decided by 2n-12 / 2n-4 ---
for n in range(4, 4002, 2):
    d = L(n) - KP(n)
    want = (2*n - 12 > 0) if n % 4 == 0 else (2*n - 4 > 0)
    assert (d > 0) == want, n
print("sign law verified: L > KP iff (n>6 on n=0 mod 4) / (n>2 on n=2 mod 4)")
print("  => L(n) > KP(n) strictly for EVERY even n >= 6")
print("  => the sole even exception is n = 4, where KP is larger pre-ceiling")
print("     (both ceil to 7, so no integer bound is lost)")

# --- 3. the additive gap grows without bound ---
print("\n  n |        ceil L |       ceil KP | integer gain | (L-KP)/(2^n/n^2)")
for n in (4, 6, 8, 10, 12, 16, 20, 30, 50, 100):
    d = L(n) - KP(n)
    scaled = float(d / F(2**n, n*n))
    print("%3d | %13d | %13d | %12d | %8.4f"
          % (n, ceil_f(L(n)), ceil_f(KP(n)), ceil_f(L(n)) - ceil_f(KP(n)), scaled))
print("\nlast column -> 2/3, i.e. the ADDITIVE gap grows like (2/3)*2^n/n^2 -> inf,")
print("even though the RATIO of the two bounds tends to 1.")

# --- 4. how often does the improvement survive the ceiling? ---
gains = [ceil_f(L(n)) - ceil_f(KP(n)) for n in range(6, 202, 2)]
print("\nover even n in [6,200]: %d/%d values strictly improve after ceiling; min gain %d"
      % (sum(1 for g in gains if g > 0), len(gains), min(gains)))


# =====================================================================
# CEILING LEMMA.  Everything above compares the bounds as REAL numbers.
# The published quantities are the CEILINGS, and L > KP does not by
# itself give ceil(L) > ceil(KP).  Checking to n = 200 is not a proof:
# a sub-1 real gap could be swallowed by the ceiling at some larger n.
#
# It really is delicate at the two values we care about most -- the gap
# is 8/15 at n=6 and 16/39 at n=8, both BELOW 1.
#
# Proof, for even n >= 6:
#   n = 6, 8      direct exact computation.
#   n = 10        gap = 64/15 > 1.
#   n >= 12 even  gap >= 2^n / (16 n^2) > 1.
# and a gap exceeding 1 forces ceil(L) > ceil(KP), since then
#   ceil(L) >= L > KP + 1 > ceil(KP).
#
# The uniform bound: on n = 0 mod 4, 2n-12 >= n/2 for n >= 8; on
# n = 2 mod 4, 2n-4 >= n/2 for n >= 3.  In both cases the denominator
# satisfies n(n+4)(3n+2) <= n(2n)(4n) = 8n^3 for n >= 4.  Hence
# gap >= 2^n (n/2) / (8 n^3) = 2^n / (16 n^2).  Finally 2^n > 16 n^2
# for every n >= 11, and 2^n / n^2 is increasing for n >= 3.
# =====================================================================

def _gap(n):
    return L(n) - KP(n)

# the two small cases, by direct exact computation
assert _gap(6) == F(8, 15) and _gap(8) == F(16, 39)
assert ceil_f(L(6)) == 20 and ceil_f(KP(6)) == 19
assert ceil_f(L(8)) == 60 and ceil_f(KP(8)) == 59

# n = 10
assert _gap(10) == F(64, 15) and _gap(10) > 1

# the uniform bound, and the exponential inequality behind it
for n in range(12, 4002, 2):
    assert _gap(n) >= F(2**n, 16 * n * n), n
assert all(2**n > 16 * n * n for n in range(11, 400))
assert 2**11 > 16 * 11**2 and 2**10 < 16 * 10**2   # 11 is exactly where it turns

# ...therefore the integer statement, which is the publishable one
for n in range(6, 4002, 2):
    assert ceil_f(L(n)) > ceil_f(KP(n)), n

print("\nCEILING LEMMA verified:")
print("  gap < 1 at n=6 (8/15) and n=8 (16/39) -- these needed the direct check")
print("  gap > 1 for every even n >= 10, via gap >= 2^n/(16 n^2) and 2^n > 16 n^2 (n >= 11)")
print("  => ceil(L) > ceil(KP) for EVERY even n >= 6, not merely n <= 200")


# =====================================================================
# AUDIT AGAINST THE PUBLISHED TABLE, not just the formula.
#
# Beating a formula is not the same as beating the best TABULATED value:
# a table can carry a stronger entry at some n from a separate computation.
# Krotov-Potapov 2021 print, for mu=2, the positions their Theorem 6
# updates (their table following Theorem 6, lower bound - upper bound):
#
#     n=8   59 - 64      n=10  188 - 216     n=12  640 - 704
#     n=14  2195 - 2560  n=16  7783 - 8192
#
# Each printed lower bound equals the Theorem 6 value exactly, so no
# tabulated entry is stronger than the formula and the comparison above
# is the right one. The excess bound therefore improves the published
# lower bound in FIVE table cells, not only at n = 8.
# =====================================================================

KP_TABLE_MU2 = {8: 59, 10: 188, 12: 640, 14: 2195, 16: 7783}
for n, published in KP_TABLE_MU2.items():
    assert ceil_f(KP(n)) == published, (n, ceil_f(KP(n)), published)

print("\nPUBLISHED-TABLE AUDIT (Krotov-Potapov 2021, mu=2):")
print("   n | published LB | excess LB | gain")
for n in sorted(KP_TABLE_MU2):
    ours = ceil_f(L(n))
    print("  %2d | %12d | %9d | %+4d" % (n, KP_TABLE_MU2[n], ours,
                                         ours - KP_TABLE_MU2[n]))
print("  every printed lower bound equals the Theorem 6 formula value,")
print("  so no tabulated entry is stronger and all five cells improve.")
print("  n=6 is absent from that table: there K(6,1,2)=20 is EXACT")
print("  (Seuranen 2007, by integer programming) and the excess bound")
print("  MATCHES it search-free rather than improving it.")
