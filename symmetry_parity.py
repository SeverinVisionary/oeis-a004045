#!/usr/bin/env python3
"""Parity of `g`-invariant double coverings, for `g` of order 2.

`SYMMETRY_THEOREM.md` reduces "every `<= 63` double covering of `Q_8` is
asymmetric" to 28 prime-order conjugacy classes of `Aut(Q_8) = F_2^8 : S_8`.
Twenty-four of them have order 2 and none is certified: both certification
routes blow up on them, while every order-3/5/7 class certifies in minutes.

This script narrows what has to be certified, using a fact that costs nothing
and a bound that is now machine-checked.

  * An order-2 `g = (pi, t)` acts **freely** exactly when its signed cycle type
    has `c > 0`, i.e. `t` is supported on a coordinate that `pi` fixes. Then
    `t` is not in `im(1 + pi)`, the equation `x xor pi(x) = t` has no solution,
    and every orbit has size 2. A `g`-invariant code is a disjoint union of
    orbits, so **its cardinality is even**.

  * `K(8,1,2) >= 61` is proved in `m61_refutation.py` and formalised in `lean/`
    with zero `sorry`s. So a double covering has `|C| >= 61` unconditionally.

Together, for a freely-acting `g`: `|C|` is even, `61 <= |C| <= 63`, hence
`|C| = 62` **exactly**. The certification target for those classes is therefore
not the inequality `sum |O| y_O <= 63` but the equality `= 62` -- one size, not
three, and an equality constraint rather than an inequality.

The four classes with `c = 0` have fixed points, so this gives nothing there and
they keep the full range `{61, 62, 63}`.

Standard library only; shares no code with `symmetry_prime.py`. Self-asserting:
it raises rather than printing a wrong number.

    python3 symmetry_parity.py
"""
n = 8
N = 1 << n


def par(v):
    return bin(v).count('1') & 1


def perm_act(pi, x):
    y = 0
    for i in range(n):
        if (x >> i) & 1:
            y |= 1 << pi[i]
    return y


def affine(pi, t, x):
    return perm_act(pi, x) ^ t


def orbit_sizes(pi, t):
    seen = [False] * N
    sizes = []
    for v in range(N):
        if seen[v]:
            continue
        k, w = 0, v
        while not seen[w]:
            seen[w] = True
            k += 1
            w = affine(pi, t, w)
        sizes.append(k)
    return sizes


def order2_classes():
    """(a, b, c) with 2a + b + c = 8 and a + c > 0, as (label, pi, t)."""
    out = []
    for a in range(0, n // 2 + 1):
        for c in range(0, n - 2 * a + 1):
            b = n - 2 * a - c
            if b < 0 or a + c == 0:
                continue
            pi, t, pos = list(range(n)), 0, 0
            for _ in range(a):
                pi[pos], pi[pos + 1] = pos + 1, pos
                pos += 2
            pos += b
            for _ in range(c):
                t |= 1 << pos
                pos += 1
            out.append(("p2_a%d_b%d_c%d" % (a, b, c), tuple(pi), t, a, b, c))
    return out


def main():
    cls = order2_classes()
    assert len(cls) == 24, len(cls)

    free, fixed = [], []
    print("%-14s %4s %8s %9s %s" % ("class", "orbs", "orbit", "fixed", "sizes"))
    for label, pi, t, a, b, c in cls:
        sizes = orbit_sizes(pi, t)
        # g has order 2, so every orbit has size 1 or 2.
        assert set(sizes) <= {1, 2}, (label, sorted(set(sizes)))
        nfix = sizes.count(1)
        isfree = nfix == 0

        # The characterisation being claimed: free  <=>  c > 0.
        assert isfree == (c > 0), (label, isfree, c)

        # And when it is not free, the fixed set is ker(1+pi), of size 2^(8-a).
        if not isfree:
            assert nfix == 1 << (n - a), (label, nfix, a)

        # g really has order 2 (it is not the identity, and squares to it).
        assert any(affine(pi, t, x) != x for x in range(N)), label
        assert all(affine(pi, t, affine(pi, t, x)) == x for x in range(N)), label

        (free if isfree else fixed).append(label)
        print("%-14s %4d %8s %9d %s"
              % (label, len(sizes), "free" if isfree else "has fix",
                 nfix, sorted(set(sizes))))

    assert len(free) == 20, len(free)
    assert len(fixed) == 4, len(fixed)
    assert fixed == ["p2_a1_b6_c0", "p2_a2_b4_c0", "p2_a3_b2_c0",
                     "p2_a4_b0_c0"], fixed

    # A freely-acting g of order 2 partitions F_2^8 into 128 orbits of size 2,
    # so an invariant code has even size. Check the partition, not just the count.
    for label, pi, t, a, b, c in cls:
        if c == 0:
            continue
        sizes = orbit_sizes(pi, t)
        assert len(sizes) == 128 and all(k == 2 for k in sizes), label
        assert sum(sizes) == N, label

    LOWER = 61   # m61_refutation.py, formalised in lean/ with zero sorries
    UPPER = 63   # the size the symmetry theorem must rule out
    admissible_free = [m for m in range(LOWER, UPPER + 1) if m % 2 == 0]
    admissible_fix = list(range(LOWER, UPPER + 1))
    assert admissible_free == [62], admissible_free
    assert admissible_fix == [61, 62, 63], admissible_fix

    print()
    print("order-2 classes                  : 24")
    print("  act freely (c > 0)             : %d" % len(free))
    print("  have fixed points (c = 0)      : %d   %s" % (len(fixed), fixed))
    print()
    print("Using K(8,1,2) >= %d (m61_refutation.py, formalised in lean/):" % LOWER)
    print("  freely-acting classes: |C| even and %d <= |C| <= %d"
          % (LOWER, UPPER))
    print("      => admissible sizes %s -- ONE equality instance, not <= %d"
          % (admissible_free, UPPER))
    print("  fixed-point classes  : no parity restriction")
    print("      => admissible sizes %s" % (admissible_fix,))
    # ---- weight-parity split -------------------------------------------
    # wt(pi(x) xor t) = wt(x) + wt(t) (mod 2), and wt(t) = c for these
    # representatives. So g swaps the even- and odd-weight halves exactly when
    # c is odd. Verified below from the ORBITS, not from that argument.
    print()
    print("%-14s %3s %-11s %s" % ("class", "c", "orbits are", "forced split of |C|=62"))
    odd_c, even_c = [], []
    for label, pi, t, a, b, c in cls:
        if c == 0:
            continue
        mixed = homog = 0
        seen = [False] * N
        for v in range(N):
            if seen[v]:
                continue
            w = affine(pi, t, v)
            seen[v] = seen[w] = True
            if par(v) == par(w):
                homog += 1
            else:
                mixed += 1
        # every orbit is mixed, or every orbit is parity-homogeneous
        assert (mixed == 128 and homog == 0) or (homog == 128 and mixed == 0), \
            (label, mixed, homog)
        assert (mixed == 128) == (c % 2 == 1), (label, c, mixed)
        if c % 2:
            odd_c.append(label)
            desc, forced = "even+odd", "M_e = M_o = 31 (unique)"
        else:
            even_c.append(label)
            desc, forced = "same parity", "M_e, M_o both even"
        print("%-14s %3d %-11s %s" % (label, c, desc, forced))
    assert len(odd_c) == 10 and len(even_c) == 10, (len(odd_c), len(even_c))

    # Which (M_e, M_o) splits survive the excess rows and the half-excess
    # inequality at |C| = 62?  (Same rows as bipartite_split.py / half_excess.py.)
    alive = []
    for Me in range(63):
        Mo = 62 - Me
        Ee = Me + n * Mo - (1 << n)
        Eo = Mo + n * Me - (1 << n)
        if Ee < 0 or Eo < 0:
            continue
        if 2 * Me - Mo <= 3 * Eo and 2 * Mo - Me <= 3 * Ee:
            alive.append((Me, Mo))
    assert len(alive) == 5, alive
    bal = [x for x in alive if x[0] == x[1]]
    ev = [x for x in alive if x[0] % 2 == 0 and x[1] % 2 == 0]
    assert bal == [(31, 31)], bal
    assert ev == [(30, 32), (32, 30)], ev

    print()
    print("At |C| = 62 the excess rows plus the half-excess inequality leave")
    print("  %d splits (M_e, M_o): %s" % (len(alive), alive))
    print("Symmetry cuts that down:")
    print("  c odd  (%d classes): %s  -- ONE split" % (len(odd_c), bal))
    print("  c even (%d classes): %s  -- TWO splits" % (len(even_c), ev))
    print()
    print("So 20 of the 24 uncertified classes reduce to a single equality")
    print("instance `sum |O| y_O = 62`, and 4 keep a three-size range.")
    print("OK")


if __name__ == "__main__":
    main()
