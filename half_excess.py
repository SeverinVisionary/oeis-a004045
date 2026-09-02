#!/usr/bin/env python3
"""The half-excess inequality  2*M_e - M_o <= 2*E_o + r_o <= 3*E_o  (n even).

Independent re-derivation and check.  Notation as in EXCESS_THEOREM.md; the odd
half plays the role of the "cheap" side.

  deg_C(x) = g(x) + 1 for every codeword x, and all codeword-neighbours of an
  even codeword are odd, so counting C_e-C_o edges from each side
        gamma_e + M_e = gamma_o + M_o.                                    (1)
  Let the HEAVY odd words be w_1..w_r, the odd words with m_i = g(w_i) >= 1, so
  sum m_i = E_o and r <= E_o.  With k_i = deg_{C_e}(w_i) = m_i + 2 - [w_i in C],
        sum k_i = E_o + 2r - s,   s = #heavy odd words that are codewords.  (2)
  For x in C_e write S(x) = sum_{y in B(x)} g(y) = g(x) + L(x), where L(x) is
  the m-mass on x's heavy neighbours.  S(x) is ODD (established).  So if L(x) is
  even then g(x) is odd, hence >= 1.  Summing the identity
  sum_{x in C_e} S(x) = gamma_e + sum_i m_i k_i against that,
        #{x in C_e : L(x) even} <= gamma_e.                               (3)
  Every x with L(x) odd has a heavy neighbour, so #{L odd} <= sum k_i.    (4)
  (3)+(4): M_e <= gamma_e + sum k_i.  Substitute (1) and (2), and use
  gamma_o - s = sum over heavy odd CODEWORDS of (m_i - 1) <= E_o - r:
        2*M_e - M_o <= 2*E_o + r <= 3*E_o.
"""
import itertools, random

def ball(v, n): return [v] + [v ^ (1 << i) for i in range(n)]
def par(v): return bin(v).count('1') & 1

def audit(C, n):
    """Recompute every quantity from the code and check the chain end to end."""
    N, S_ = 1 << n, set(C)
    c = [0] * N
    for u in S_:
        for y in ball(u, n): c[y] += 1
    if min(c) < 2: return None
    g = [ci - 2 for ci in c]
    Ce = {x for x in S_ if not par(x)}; Co = S_ - Ce
    Me, Mo = len(Ce), len(Co)
    Ee = sum(g[x] for x in range(N) if not par(x))
    Eo = sum(g[y] for y in range(N) if par(y))
    assert Ee == Me + n * Mo - (1 << (n - 1)) * 2, "E_e identity"
    assert Eo == Mo + n * Me - (1 << (n - 1)) * 2, "E_o identity"
    ge = sum(g[x] for x in Ce); go = sum(g[y] for y in Co)
    assert ge + Me == go + Mo, "edge count (1)"
    heavy = [y for y in range(N) if par(y) and g[y] >= 1]
    r = len(heavy); s = sum(1 for y in heavy if y in S_)
    k = {w: sum(1 for x in ball(w, n)[1:] if x in Ce) for w in heavy}
    assert sum(k.values()) == Eo + 2 * r - s, "heavy degrees (2)"
    Leven = 0
    for x in Ce:
        L = sum(g[y] for y in ball(x, n)[1:])
        assert (g[x] + L) % 2 == 1, "S(x) parity"
        if L % 2 == 0: Leven += 1
    assert Leven <= ge, "(3)"
    assert Me - Leven <= sum(k.values()), "(4)"
    assert go - s <= Eo - r, "gamma_o - s <= E_o - r"
    assert 2 * Me - Mo <= 2 * Eo + r, "MAIN sharp form"
    assert 2 * Me - Mo <= 3 * Eo, "MAIN loose form"
    assert 2 * Mo - Me <= 3 * Ee, "MAIN mirrored"
    return (Me, Mo, Ee, Eo)

print("=== n=4: EVERY double covering of F_2^4 (all 2^16 subsets) ===")
tot = 0
for k in range(17):
    for C in itertools.combinations(range(16), k):
        if audit(list(C), 4) is not None: tot += 1
print("  %d double coverings, 0 assertion failures" % tot)

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
    for u in sorted(C, key=lambda _: rng.random()):      # thin back toward minimality
        D = C - {u}
        cc = [0] * N
        for v in D:
            for y in ball(v, n): cc[y] += 1
        if min(cc) >= 2: C = D
    return sorted(C)

for n in (6, 8):
    for seed in range(150 if n == 6 else 80):
        assert audit(rand_cover(n, seed), n) is not None
    print("=== n=%d: %d random minimal double coverings, 0 failures ===" % (n, 150 if n == 6 else 80))

print("\n=== what the inequality does to the M=60 case list at n=8 ===")
for Me in range(28, 33):
    Mo = 60 - Me
    Ee = Me + 8 * Mo - 256; Eo = Mo + 8 * Me - 256
    d1, d2 = 2 * Me - Mo - 3 * Eo, 2 * Mo - Me - 3 * Ee
    v = "KILLED" if (d1 > 0 or d2 > 0) else "survives"
    print("  (%2d,%2d) E=(%2d,%2d): 2M_e-M_o-3E_o=%+4d  2M_o-M_e-3E_e=%+4d  %s"
          % (Me, Mo, Ee, Eo, d1, d2, v))
print("\n=== control: the published 64-word code must NOT be killed ===")
import json, os
p = os.path.join(os.path.dirname(__file__) or '.', 'code64.json')
if os.path.exists(p):
    d = json.load(open(p)); C = d['code'] if isinstance(d, dict) else d
    print("  audit(64-word code) =", audit([int(w) for w in C], 8))
else:
    print("  code64.json not present here; skipped")

print("\n=== the full ladder at n=8: which M are refuted outright? ===")
print("    (a split survives only if BOTH mirrored forms hold)")
for M in range(55, 66):
    surv = []
    for Me in range(M + 1):
        Mo = M - Me
        Ee = Me + 8 * Mo - 256; Eo = Mo + 8 * Me - 256
        if Ee < 0 or Eo < 0: continue                      # row R_e or R_o violated
        if 2 * Me - Mo <= 3 * Eo and 2 * Mo - Me <= 3 * Ee:
            surv.append((Me, Mo))
    print("  M=%2d: %s" % (M, "REFUTED (no split survives)" if not surv
                           else "%d split(s) survive: %s" % (len(surv), surv)))
print("\n  => K(8,1,2) >= 60 with no solver, matching the certified refutation of M=59.")
print("     At M=60 only the balanced split (30,30) survives; killing it gives K >= 61.")

print("\n=== same ladder at n=6, where K(6,1,2)=20 is known ===")
for M in range(17, 22):
    surv = []
    for Me in range(M + 1):
        Mo = M - Me
        Ee = Me + 6 * Mo - 64; Eo = Mo + 6 * Me - 64
        if Ee < 0 or Eo < 0: continue
        if 2 * Me - Mo <= 3 * Eo and 2 * Mo - Me <= 3 * Ee: surv.append((Me, Mo))
    print("  M=%2d: %s" % (M, "REFUTED" if not surv else "%d survive: %s" % (len(surv), surv)))
print("  => reproduces K(6,1,2) >= 20, the exact value.")
