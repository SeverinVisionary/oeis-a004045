#!/usr/bin/env python3
"""Prime-order automorphism sweep for K(n,1,2) -- the whole symmetry theorem.

Why prime order is enough, and why 746 classes were never needed:

    If a code C has a nontrivial automorphism group, some non-identity g fixes
    C, and some power of g has PRIME order and also fixes C. So ruling out
    invariance under prime-order automorphisms rules out every nontrivial
    automorphism group. Conjugate elements give isomorphic orbit-ILPs, so one
    representative per conjugacy class suffices.

For Aut(Q_8) = F_2^8 : S_8 (the hyperoctahedral group B_8) the classes are
indexed by signed cycle types, i.e. bipartitions of 8. An element with a
positive L-cycle has order L on that block; a negative L-cycle has order 2L.
So the prime orders available are 2, 3, 5, 7, and the prime-order classes are:

    order 2: 2a + b + c = 8, a + c > 0     (a positive 2-cycles, b positive
                                            1-cycles, c negative 1-cycles) -> 24
    order 3: 3a + b = 8, a >= 1                                            ->  2
    order 5: 5a + b = 8, a >= 1                                            ->  1
    order 7: 7a + b = 8, a >= 1                                            ->  1
                                                                    total    28

`--selftest` checks that count against random sampling instead of trusting the
derivation: it draws random elements of Aut(Q_8), keeps the prime-order ones,
and asserts every one is conjugate to a listed representative.
"""
import argparse
import itertools
import json
import random
import sys

N = 8


def apply_perm(perm, x):
    """y with y_{perm[i]} = x_i."""
    y = 0
    for i in range(N):
        if (x >> i) & 1:
            y |= 1 << perm[i]
    return y


def affine(perm, t, x):
    return apply_perm(perm, x) ^ t


def order_of(perm, t):
    x, k = None, 0
    # order of the affine map = smallest k>0 with g^k = identity on F_2^n
    g = list(range(1 << N))
    g = [affine(perm, t, v) for v in range(1 << N)]
    cur = list(range(1 << N))
    for k in range(1, 4 * N + 3):
        cur = [g[v] for v in cur]
        if all(cur[v] == v for v in range(1 << N)):
            return k
    return None


def signed_cycle_type(perm, t):
    """Bipartition (positive cycle lengths, negative cycle lengths).

    Sign of a cycle is the XOR of the translation bits around it.
    """
    seen, pos, neg = [False] * N, [], []
    for i in range(N):
        if seen[i]:
            continue
        cyc, j = [], i
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = perm[j]
        sign = 0
        for j in cyc:
            sign ^= (t >> j) & 1
        (neg if sign else pos).append(len(cyc))
    return (tuple(sorted(pos)), tuple(sorted(neg)))


def representatives():
    """One (perm, t, label) per prime-order conjugacy class."""
    reps = []
    # order 2
    for a in range(0, N // 2 + 1):
        for c in range(0, N - 2 * a + 1):
            b = N - 2 * a - c
            if b < 0 or a + c == 0:
                continue
            perm, t, pos = list(range(N)), 0, 0
            for _ in range(a):                      # positive 2-cycles
                perm[pos], perm[pos + 1] = pos + 1, pos
                pos += 2
            pos += b                                # positive fixed points
            for _ in range(c):                      # negative fixed points
                t |= 1 << pos
                pos += 1
            reps.append((tuple(perm), t,
                         "p2_a%d_b%d_c%d" % (a, b, c)))
    # odd primes: positive L-cycles only (a negative L-cycle has order 2L)
    for p in (3, 5, 7):
        for a in range(1, N // p + 1):
            perm, pos = list(range(N)), 0
            for _ in range(a):
                for k in range(p):
                    perm[pos + k] = pos + (k + 1) % p
                pos += p
            reps.append((tuple(perm), 0, "p%d_a%d" % (p, a)))
    return reps


def orbits_of(perm, t):
    seen, orbs = [False] * (1 << N), []
    for v in range(1 << N):
        if seen[v]:
            continue
        o, w = [], v
        while not seen[w]:
            seen[w] = True
            o.append(w)
            w = affine(perm, t, w)
        orbs.append(o)
    return orbs


def selftest(trials=4000, seed=0):
    reps = representatives()
    want = {signed_cycle_type(p, t) for p, t, _ in reps}
    assert len(reps) == 28, "expected 28 representatives, got %d" % len(reps)
    assert len(want) == 28, "representatives collide: %d distinct types" % len(want)
    for p, t, lab in reps:
        o = order_of(p, t)
        claimed = int(lab.split("_")[0][1:])
        assert o == claimed, "%s has order %s, expected %d" % (lab, o, claimed)
    rng = random.Random(seed)
    found, checked = set(), 0
    for _ in range(trials):
        perm = list(range(N))
        rng.shuffle(perm)
        t = rng.randrange(1 << N)
        o = order_of(tuple(perm), t)
        if o in (2, 3, 5, 7):
            checked += 1
            ty = signed_cycle_type(tuple(perm), t)
            assert ty in want, "sampled prime-order type %s not in the 28" % (ty,)
            found.add(ty)
    print(json.dumps({
        "representatives": len(reps),
        "distinct_signed_cycle_types": len(want),
        "random_elements_drawn": trials,
        "prime_order_samples_checked": checked,
        "distinct_types_hit_by_sampling": len(found),
        "all_samples_matched_a_representative": True,
        "orbit_counts": {lab: len(orbits_of(p, t)) for p, t, lab in reps},
    }, indent=2))
    print("SELFTEST PASS")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        for p, t, lab in representatives():
            print(lab, order_of(p, t), len(orbits_of(p, t)))


def ball(v):
    return [v] + [v ^ (1 << i) for i in range(N)]


def solve_class(perm, t, ub, mu=2):
    """Is there a g-invariant mu-fold covering with |C| <= ub?

    Variables are ORBITS of <g>: an invariant code is a union of orbits.
    Returns (status, size, code) with code a sorted word list when feasible.
    """
    import highspy
    import numpy as np
    orbs = orbits_of(perm, t)
    idx = {}
    for oi, o in enumerate(orbs):
        for v in o:
            idx[v] = oi
    n = len(orbs)
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.addVars(n, np.zeros(n), np.ones(n))
    h.changeColsIntegrality(n, np.arange(n, dtype=np.int32),
                            np.array([highspy.HighsVarType.kInteger] * n))
    # coverage: every vertex covered mu times (one row per vertex; cheap at 256)
    starts, indices, values, lower, upper = [], [], [], [], []
    for v in range(1 << N):
        cnt = {}
        for w in ball(v):
            cnt[idx[w]] = cnt.get(idx[w], 0) + 1
        starts.append(len(indices))
        for k, c in cnt.items():
            indices.append(k)
            values.append(float(c))
        lower.append(float(mu))
        upper.append(highspy.kHighsInf)
    # cardinality
    starts.append(len(indices))
    for oi, o in enumerate(orbs):
        indices.append(oi)
        values.append(float(len(o)))
    lower.append(-highspy.kHighsInf)
    upper.append(float(ub))
    h.addRows(len(lower), np.array(lower), np.array(upper),
              len(indices), np.array(starts), np.array(indices, dtype=np.int32),
              np.array(values))
    h.run()
    st = h.getModelStatus()
    name = h.modelStatusToString(st)
    if name != "Optimal":
        return name, None, None
    sol = h.getSolution().col_value
    code = sorted(v for oi, o in enumerate(orbs) if sol[oi] > 0.5 for v in o)
    return "Feasible", len(code), code
