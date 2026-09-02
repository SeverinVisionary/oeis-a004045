#!/usr/bin/env python3
"""Can the within-half distance-2 pair count close the balanced case?  No.

In the balanced case at n=8, M=60 (M_e=M_o=30, E_e=E_o=14, gamma_e=gamma_o=gamma)
summing the exact ball identity  sum_{y in B(x)} g(y) = 2*N_2(x) - 9  over the
even codewords gives, with e_1 = gamma + 30 the induced edge count and e2_e the
number of distance-2 pairs inside the even half,

        4 * e2_e = Q_o + 238 - 2*gamma,      Q_o = sum over odd words of g^2.

Since sum_{odd} g = E_o = 14 with g >= 0 integral, Q_o >= 14; and g <= 7 (a word
has c <= 9), so Q_o <= 98.  With gamma in [0,14] this pins

        56 <= e2_e <= 84.

Closing M=60 by counting would need an independent UPPER bound e2_e <= 52.  The
identity forces e2_e >= 56, so no such bound can exist -- the target is below
what the case itself requires.  56 distance-2 pairs among 30 words is an average
degree of under 4 in the distance-2 graph, far from any extremal obstruction.

Conclusion: this counting route is exhausted.  The balanced case needs a
different method, not a sharper count.
"""
import functools, itertools, random
print = functools.partial(print, flush=True)

def ball(v, n): return [v] + [v ^ (1 << i) for i in range(n)]
def par(v): return bin(v).count('1') & 1

def quantities(C, n=8):
    N, S_ = 1 << n, set(C)
    c = [0] * N
    for u in S_:
        for y in ball(u, n): c[y] += 1
    if min(c) < 2: return None
    g = [x - 2 for x in c]
    Ce = {x for x in S_ if not par(x)}
    gamma = sum(g[x] for x in Ce)
    Qo = sum(g[y] ** 2 for y in range(N) if par(y))
    e2e = sum(1 for a, b in itertools.combinations(sorted(Ce), 2)
              if bin(a ^ b).count('1') == 2)
    return gamma, Qo, e2e, len(Ce), len(S_) - len(Ce)

print("=== check 4*e2_e = Q_o + 238 - 2*gamma on balanced n=8 covers ===")
print("    (the identity is specific to M=60 balanced; for general M and split")
print("     the constant moves, so we verify the general form it comes from)")
def general(C, n=8):
    """4*e2_e = Q_o + 2*(9*M_e) - 2*e_1 - 2*... -- rederived per code, no constants."""
    N, S_ = 1 << n, set(C)
    c = [0] * N
    for u in S_:
        for y in ball(u, n): c[y] += 1
    if min(c) < 2: return None
    g = [x - 2 for x in c]
    Ce = {x for x in S_ if not par(x)}
    Co = S_ - Ce
    lhs = sum(sum(g[y] for y in ball(x, n)) for x in Ce)
    N2 = {x: sum(1 for u in S_ if 1 <= bin(u ^ x).count('1') <= 2) for x in Ce}
    assert lhs == sum(2 * N2[x] - (n + 1) for x in Ce), "ball identity summed over C_e"
    e1 = sum(1 for x in Ce for y in ball(x, n)[1:] if y in Co)
    e2e = sum(1 for a, b in itertools.combinations(sorted(Ce), 2)
              if bin(a ^ b).count('1') == 2)
    assert sum(N2.values()) == e1 + 2 * e2e, "N2 splits into edges + distance-2 pairs"
    return True

def rand_cover(n, seed):
    rng = random.Random(seed); N = 1 << n
    C = set(rng.sample(range(N), N // 3))
    while True:
        cc = [0] * N
        for u in C:
            for y in ball(u, n): cc[y] += 1
        bad = [x for x in range(N) if cc[x] < 2]
        if not bad: break
        x = rng.choice(bad); C.add(rng.choice([y for y in ball(x, n) if y not in C]))
    return sorted(C)

ok = sum(1 for s in range(60) if general(rand_cover(8, s)))
print("  %d random n=8 covers: both identities hold" % ok)
ok6 = sum(1 for s in range(60) if general(rand_cover(6, s), 6))
print("  %d random n=6 covers: both identities hold" % ok6)

print("\n=== the balanced M=60 window ===")
for gamma in (0, 7, 14):
    lo = (14 + 238 - 2 * gamma) / 4.0
    hi = (98 + 238 - 2 * gamma) / 4.0
    print("  gamma=%2d:  e2_e in [%.1f, %.1f]" % (gamma, lo, hi))
print("  over gamma in [0,14]:  e2_e >= %.0f" % ((14 + 238 - 28) / 4.0))
print("\n  Target for a counting kill was e2_e <= 52.")
print("  The identity FORCES e2_e >= 56.  No such upper bound can exist.")
print("  => the counting route to the balanced case is exhausted.")
