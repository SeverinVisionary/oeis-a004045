#!/usr/bin/env python3
"""Why the excess bound needs n EVEN: an explicit optimal counterexample at n=3.

Surfaced by an adversarial review (gpt-5.6-terra, 2026-09-01) and verified here
rather than taken on report.

    C = {000, 001, 110, 111}  in  F_2^3

is a double covering with c(x) = 2 for EVERY x, hence g == 0 and E = 0.  Step 2
of the excess theorem asserts that every codeword has an over-covered word in
its ball; here there are none anywhere, so the conclusion is plainly false.

The mechanism is exactly the parity: at odd n the ball has EVEN size n+1, so the
ball sum (n+1) + 2*N_2(x) is even and never rounds up past 2(n+1).

This example is sharp in two ways.  It is PERFECT -- every coverage is exactly
2, the extreme case -- and it is OPTIMAL, since |C| = 4 = K(3,1,2).  So the
even-n hypothesis is not an artifact of a bad small case; it fails at the best
possible code.
"""
C = [0b000, 0b001, 0b110, 0b111]
def ball(v, n=3): return [v] + [v ^ (1 << i) for i in range(n)]

c = {x: sum(1 for w in ball(x) if w in C) for x in range(8)}
assert all(v == 2 for v in c.values()), "not a perfect double covering"
assert len(C) == 4, "K(3,1,2) = 4, so this must have 4 words"

g = {x: c[x] - 2 for x in range(8)}
assert sum(g.values()) == 0, "E must be 0"
for x in C:
    assert sum(g[y] for y in ball(x)) == 0, "Step 2 must FAIL here"

x = 0
tot = sum(c[y] for y in ball(x))
N2 = sum(1 for u in C if 1 <= bin(u ^ x).count('1') <= 2)
assert tot == 4 + 2 * N2 and tot % 2 == 0, "ball sum must be even at odd n"

print("C = {000, 001, 110, 111} in F_2^3")
print("  c(x) = 2 for all x, so g == 0 and E = 0")
print("  Step 2 demands ball-excess >= 1 at each codeword; it is 0 -- FAILS")
print("  ball sum at 000 = %d = (n+1) + 2*N_2 = 4 + 2*%d, EVEN: no round-up" % (tot, N2))
print("  |C| = 4 = K(3,1,2): perfect AND optimal, so the failure is not degenerate")
print("\nThe even-n hypothesis is necessary.")
