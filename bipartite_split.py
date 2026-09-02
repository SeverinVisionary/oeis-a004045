#!/usr/bin/env python3
"""The weight-parity split, and the case it kills by hand.

For even n, split F_2^n into the even- and odd-weight halves (2^(n-1) each).
Every neighbour of an even word is odd, so summing coverage over the even half

    sum_{x even} c(x) = M_e + n*M_o  >=  2 * 2^(n-1) = 2^n,          (R_e)
    sum_{x odd}  c(x) = M_o + n*M_e  >=  2^n.                        (R_o)

Both are nonnegative combinations of the original covering rows, so each is
certifiable in one step.  Define the per-half excesses
    E_e = M_e + n*M_o - 2^n,   E_o = M_o + n*M_e - 2^n.

KILLED CASE.  Suppose E_o = 0.  Then every odd word has c = 2 exactly, so the
over-covered set S is entirely even.  An even codeword's ball is itself plus n
odd words, none over-covered, so Step 2 of the excess theorem (ball-excess >= 1)
forces g(x) >= 1 for every x in C_e: C_e is a subset of S.  If additionally
|C_e| = E_e then S = C_e with g == 1, i.e. coverage is exactly 3 on C_e and
exactly 2 everywhere else.  Now count C_e-C_o edges twice:
    x in C_e: c(x) = 1 + deg_o(x) = 3  =>  deg_o(x) = 2  =>  F = 2*M_e
    y in C_o: c(y) = 1 + deg_e(y) = 2  =>  deg_e(y) = 1  =>  F =   M_o
so the case dies whenever 2*M_e != M_o.

STRONGER FORM.  The chain above needs only C_e contained in S and |S| <= E_e,
which already gives  M_e <= E_e.  So E_o = 0 kills the case OUTRIGHT whenever
M_e > E_e, and when M_e = E_e it kills unless 2*M_e = M_o.  The outright form is
what closes n=6, M=19: both surviving splits there have a zero-excess half with
M_e = 9 > 5 = E_e, so K(6,1,2) >= 20 -- the exact value -- with no search.
"""
import itertools
from math import ceil
from fractions import Fraction

def cases(n, M):
    """(M_e, M_o, E_e, E_o, verdict) for every split allowed by rows R_e, R_o."""
    out = []
    for Me in range(M + 1):
        Mo = M - Me
        Ee = Me + n * Mo - (1 << n)
        Eo = Mo + n * Me - (1 << n)
        if Ee < 0 or Eo < 0:
            continue                      # violates R_e or R_o outright
        v = "OPEN"
        if Eo == 0:
            if Me > Ee:                     v = "KILLED (E_o=0: M_e=%d > E_e=%d)" % (Me, Ee)
            elif Me == Ee and 2 * Me != Mo: v = "KILLED (E_o=0: %d edges != %d)" % (2 * Me, Mo)
        if Ee == 0:
            if Mo > Eo:                     v = "KILLED (E_e=0: M_o=%d > E_o=%d)" % (Mo, Eo)
            elif Mo == Eo and 2 * Mo != Me: v = "KILLED (E_e=0: %d edges != %d)" % (2 * Mo, Me)
        out.append((Me, Mo, Ee, Eo, v))
    return out

def report(n, M):
    cs = cases(n, M)
    if not cs:
        print("  n=%d M=%d: NO split survives rows R_e,R_o -- M is refuted outright" % (n, M))
        return True
    print("  n=%d M=%d:" % (n, M))
    for Me, Mo, Ee, Eo, v in cs:
        print("     (M_e,M_o)=(%2d,%2d)  E_e=%3d E_o=%3d   %s" % (Me, Mo, Ee, Eo, v))
    allkilled = all(c[4] != "OPEN" for c in cs)
    print("     => %s" % ("ALL CASES KILLED: no such code exists" if allkilled
                          else "%d case(s) remain open" % sum(c[4] == "OPEN" for c in cs)))
    return allkilled

print("=== n=4: the counting bound gives only M >= 7, but K(4,1,2) = 8. ===")
k4 = report(4, 7)

print("\n=== n=6: counting bound already gives 20; the split must also kill M=19 ===")
k6 = report(6, 19)
assert k6, "split failed to kill n=6 M=19, but K(6,1,2)=20 is known -- method is too weak"

print("\n=== n=8: the live frontier, and the rungs above it ===")
report(8, 60)
for M in (61, 62, 63):
    report(8, M)

# ---- exhaustive ground truth at n=4 -------------------------------------
def ball(v, n): return [v] + [v ^ (1 << i) for i in range(n)]
def is_cover(C, n):
    c = [0] * (1 << n)
    for u in C:
        for y in ball(u, n): c[y] += 1
    return min(c) >= 2

print("\n=== exhaustive ground truth: double coverings of F_2^4 of size 7 ===")
found = sum(1 for C in itertools.combinations(range(16), 7) if is_cover(C, 4))
print("  brute force: %d found (C(16,7) = 11440 candidates)" % found)
assert found == 0, "a 7-word double covering of F_2^4 exists; the split argument is WRONG"
assert k4, "split failed to kill n=4 M=7, yet none exists -- argument is incomplete, not unsound"
print("  agrees with the split argument: K(4,1,2) >= 8, proved with no search.")
