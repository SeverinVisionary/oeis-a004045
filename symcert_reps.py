#!/usr/bin/env python3
"""Independent re-derivation of the 28 prime-order conjugacy-class
representatives of Aut(Q_8) = F_2^8 : S_8, and their orbits on F_2^8.

This module is written from scratch for the certification job in
symcert_encode.py / symcert_certify.py. It does NOT import symmetry_prime.py,
so the encoder producing the instances being certified is not the same program
that produced the "Infeasible" solver statuses in
logs/symmetry_prime_sweep_2026-08-30.log.

How much that independence is worth, stated precisely, because an earlier
version of this docstring overstated it. The two modules were typed
independently but they REASON identically: prime_order_classes() below and
symmetry_prime.representatives() both enumerate the 28 classes through the
same a/b/c parameterisation (a positive 2-cycles, b positive fixed points,
c negative fixed points; positive p-cycles for odd p). Agreement between them
on labels and orbit counts is therefore weak evidence -- a shared error in
that reasoning would appear in both. Verified 2026-08-30: all 28 labels,
orders, orbit counts and orbit-size profiles agree exactly, which rules out
transcription slips but not a common misunderstanding.

The genuinely independent check is elsewhere, and it passes:
symmetry_prime.completeness_check() reaches the number 28 from the opposite
direction -- it enumerates all 185 signed cycle types of B_8 and filters by
element order, rather than constructing the prime-order ones directly. Two
different routes to the same 28 is the real cross-check. Cite that one, not
this module's mere non-importing.

Group model
-----------
An element of Aut(Q_8) acts on F_2^8 (words of length 8) as

    g(x) = P(x) XOR t

where P permutes the 8 coordinate positions and t in F_2^8 is a translation.
Composition is (P2,t2) . (P1,t1) = (P2 P1, P2(t1) XOR t2) -- this is exactly
the semidirect product F_2^8 : S_8. Conjugacy classes of the hyperoctahedral
group B_8 are indexed by "signed cycle types": partition the 8 coordinates
into cycles of P, and give each cycle a sign (XOR of the t-bits visited going
around it). A cycle of length L has order L if its sign is +, order 2L if its
sign is -.

Representatives are built directly from a signed cycle type rather than by
reusing symmetry_prime.py's parameterisation, and every representative is
checked (order, orbit count) by brute-force simulation before use.
"""
import itertools

N = 8
UNIVERSE = 1 << N  # 256


def act(coord_perm, translation, word):
    """Apply g = (coord_perm, translation) to one word of F_2^N.

    coord_perm[i] is the destination coordinate for source coordinate i:
    bit i of `word` lands in bit coord_perm[i] of the image, then the whole
    thing is XORed with `translation`.
    """
    out = 0
    for src in range(N):
        if (word >> src) & 1:
            out |= 1 << coord_perm[src]
    return out ^ translation


def element_order(coord_perm, translation, cap=4 * N + 4):
    """Brute-force order of g on F_2^N by iterating until every point returns."""
    cur = list(range(UNIVERSE))
    for k in range(1, cap + 1):
        cur = [act(coord_perm, translation, w) for w in cur]
        if all(w == v for w, v in zip(cur, range(UNIVERSE))):
            return k
    raise RuntimeError("order exceeds cap %d" % cap)


def orbits(coord_perm, translation):
    """All orbits of <g> on F_2^N, via plain BFS/iteration (no shortcuts)."""
    visited = bytearray(UNIVERSE)
    out = []
    for start in range(UNIVERSE):
        if visited[start]:
            continue
        block, w = [], start
        while not visited[w]:
            visited[w] = 1
            block.append(w)
            w = act(coord_perm, translation, w)
        out.append(block)
    return out


def _cyclic_block(perm, translation, positions, sign):
    """Wire up one cycle of coordinates `positions` (in cycle order) with the
    given sign: perm sends positions[i] -> positions[(i+1) % L], and if
    sign=1 exactly one of the L "hops" carries a translation bit at the
    destination coordinate positions[0], making the whole cycle's XOR = 1.
    """
    L = len(positions)
    for i in range(L):
        perm[positions[i]] = positions[(i + 1) % L]
    if sign:
        translation[0] |= 1 << positions[0]


def build_representative(pos_cycles, neg_cycles):
    """Build one (coord_perm, translation) whose signed cycle type is exactly
    (sorted(pos_cycles), sorted(neg_cycles)); cycles are laid out on disjoint
    blocks of coordinates 0..7 in the order given.
    """
    assert sum(pos_cycles) + sum(neg_cycles) == N
    perm = list(range(N))
    trans = [0]
    cursor = 0
    for L in pos_cycles:
        _cyclic_block(perm, trans, list(range(cursor, cursor + L)), sign=0)
        cursor += L
    for L in neg_cycles:
        _cyclic_block(perm, trans, list(range(cursor, cursor + L)), sign=1)
        cursor += L
    return tuple(perm), trans[0]


def signed_cycle_type(coord_perm, translation):
    """Read back the (positive cycle lengths, negative cycle lengths) of an
    element, independently of how it was built -- used to self-check
    build_representative and to confirm the 28 classes are pairwise distinct.
    """
    seen = [False] * N
    pos, neg = [], []
    for i in range(N):
        if seen[i]:
            continue
        cyc = []
        j = i
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = coord_perm[j]
        parity = 0
        for j in cyc:
            parity ^= (translation >> j) & 1
        (neg if parity else pos).append(len(cyc))
    return tuple(sorted(pos)), tuple(sorted(neg))


def prime_order_classes():
    """One representative per prime-order conjugacy class of Aut(Q_8), built
    from bipartitions of 8 into signed cycle lengths.

    order 2: a positive 2-cycles, b positive fixed points, c negative fixed
              points, 2a+b+c=8, a+c>0 (need at least one 2-cycle or one
              negative fixed point to have order exactly 2)
    order p (p in {3,5,7}): a positive p-cycles, b positive fixed points,
              ap+b=8, a>=1  (a negative p-cycle has order 2p, not p, so it is
              excluded here on purpose)

    Returns a list of dicts: label, perm, t, order (claimed), orbit sizes.
    """
    reps = []

    for a in range(0, N // 2 + 1):
        for c in range(0, N - 2 * a + 1):
            b = N - 2 * a - c
            if b < 0:
                continue
            if a + c == 0:
                continue  # identity, not order 2
            pos_cycles = [2] * a + [1] * b
            neg_cycles = [1] * c
            perm, t = build_representative(pos_cycles, neg_cycles)
            label = "p2_a%d_b%d_c%d" % (a, b, c)
            reps.append((label, perm, t, 2))

    for p in (3, 5, 7):
        for a in range(1, N // p + 1):
            b = N - a * p
            pos_cycles = [p] * a + [1] * b
            perm, t = build_representative(pos_cycles, [])
            label = "p%d_a%d" % (p, a)
            reps.append((label, perm, t, p))

    return reps


def validated_classes():
    """prime_order_classes(), but every entry is checked before being
    returned: the built element really has the claimed prime order, its
    signed cycle type really matches what was asked for, and all 28 types
    are pairwise distinct. Raises AssertionError on any mismatch.
    """
    reps = prime_order_classes()
    assert len(reps) == 28, "expected 28 prime-order classes, built %d" % len(reps)
    seen_types = set()
    out = []
    for label, perm, t, claimed_order in reps:
        actual_order = element_order(perm, t)
        assert actual_order == claimed_order, (
            "%s: built order %d, claimed %d" % (label, actual_order, claimed_order))
        ty = signed_cycle_type(perm, t)
        assert ty not in seen_types, "%s: signed cycle type %r collides" % (label, ty)
        seen_types.add(ty)
        orbs = orbits(perm, t)
        assert sum(len(o) for o in orbs) == UNIVERSE
        # every orbit's size must divide the element order (orbit-stabilizer)
        for o in orbs:
            assert actual_order % len(o) == 0, (
                "%s: orbit of size %d does not divide order %d" %
                (label, len(o), actual_order))
        out.append({
            "label": label, "perm": perm, "t": t, "order": actual_order,
            "orbits": orbs, "n_orbits": len(orbs),
        })
    return out


if __name__ == "__main__":
    import json
    classes = validated_classes()
    summary = [{"label": c["label"], "order": c["order"], "n_orbits": c["n_orbits"]}
               for c in classes]
    print(json.dumps(summary, indent=2))
    print("VALIDATED %d CLASSES" % len(classes))
