#!/usr/bin/env python3
"""Prescribed-automorphism search over NON-CYCLIC subgroups of Aut(Q_8).

prescribed.py exhausted the cyclic stratum (746 (pi,t) classes, all but the
trivial one settled negative -- see WORKLOAD_ESTIMATE_2026-08-28.md S3.2).
This sweeps the next stratum named there: non-cyclic subgroups of
Aut(Q_8) = F_2^8 : S_8 of order 4 to 32.

Group law. g = (pi, t) acts as x -> pi(x) xor t, where pi in S_8 permutes bit
positions (pi[i] = destination of source position i) and t in F_2^8.
Composition: (pi1,t1)*(pi2,t2) = (pi1 o pi2, t1 xor perm_act(pi1,t2)), where
(pi1 o pi2)[i] = pi1[pi2[i]]. This is the semidirect product multiplication;
verified against the special case pi2=id used throughout.

Two families, both built from a partition of the 8 coordinates into disjoint
blocks so that generators supported on different blocks automatically
commute (each pi_j is the identity outside its own block, so pi_j fixes
every t_k, k != j, trivially):

  1. Block-diagonal elementary abelian groups (Klein four and beyond).
     Per block B of size m, an order-2 generator, either
       - "flip": pi = id on B, t = a fixed weight-w vector on B (w = 1..m)
       - "swap": pi = a fixed-point-free involution on B (m even, m>=2),
         t = a pi-invariant vector on B, i.e. constant on each transposed
         pair (w' pairs set to 11, the rest 00; w' = 0..m/2)
     One generator per block, direct product across r = 2..5 blocks gives
     an elementary abelian group of order 2^r: order 4 is Klein four,
     order 8/16/32 are the higher-rank elementary abelian groups named in
     the README's task list. The sweep ranges over integer partitions of 8
     into r parts (only the partition shape matters up to S_8-conjugacy,
     exactly as prescribed.py's cycle types) and over generator-type +
     weight-class choices per block.

  2. Small dihedral groups D_m (order 2m), m = 3..8, realized on a single
     block of size m as a coordinate "ring": rotation rho = the m-cycle
     (0 1 ... m-1), reflection sigma: i -> -i mod m (so sigma rho sigma^-1
     = rho^-1, the defining dihedral relation, which holds in S_8 before
     any translation is added). The rotation carries no translation (so it
     already has order exactly m); the reflection's translation ranges over
     all sigma-invariant vectors on the block (constant on each orbit of
     sigma, size 2^(#orbits of sigma)). Coordinates outside the block are
     fixed by both generators (identity, zero translation). m=2 is skipped:
     the reflection degenerates to the identity permutation there and D_2 is
     just the abelian Klein four already covered by family 1.

Both families produce the group by explicit BFS closure of the named
generators (not assumed), so a construction error shows up as an unexpected
order rather than silently mis-swept. Every instance whose resulting group
order is not in [4, 32], or is cyclic (checked directly: a group is cyclic
iff it has an element whose order equals |G|), is skipped before solving --
the sweep only ever *solves* genuinely non-cyclic order-4..32 instances.

Each orbit-ILP is solved with an explicit per-instance time limit. A solve
that is not "Optimal" and not "Infeasible" is recorded as UNRESOLVED and
printed -- exactly the fix prescribed_followup.py made to the original bug,
where 31%% of instances silently defaulted to "negative" on a timeout. This
sweep is exhaustive over its own two families only if UNRESOLVED is empty;
that is checked and printed at the end, not assumed.

Requires: highspy, numpy. Witnesses must still go through verify.py.
"""
import sys, time, json, argparse
from collections import Counter
import highspy
import numpy as np

n = 8
N = 1 << n


def perm_act(pi, x):
    y = 0
    for i in range(n):
        if (x >> i) & 1:
            y |= 1 << pi[i]
    return y


def elem_act(g, x):
    pi, t = g
    return perm_act(pi, x) ^ t


def compose(g1, g2):
    pi1, t1 = g1
    pi2, t2 = g2
    pi = tuple(pi1[pi2[i]] for i in range(n))
    return (pi, t1 ^ perm_act(pi1, t2))


IDENTITY = (tuple(range(n)), 0)


def closure(gens, cap=64):
    """BFS closure of <gens>. Returns None if it grows past cap (a
    construction bug, since every family here is designed to close at
    order <= 32)."""
    elems = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        nxt = []
        for a in frontier:
            for g in gens:
                b = compose(a, g)
                if b not in elems:
                    elems.add(b)
                    nxt.append(b)
                    if len(elems) > cap:
                        return None
        frontier = nxt
    return elems


def element_order(g, cap=64):
    a = g
    k = 1
    while a != IDENTITY:
        a = compose(a, g)
        k += 1
        if k > cap:
            return None
    return k


def is_cyclic(elems):
    order = len(elems)
    return any(element_order(g, cap=order) == order for g in elems)


def group_orbits(elems):
    seen = [-1] * N
    orbits = []
    for v in range(N):
        if seen[v] >= 0:
            continue
        o = sorted({elem_act(g, v) for g in elems})
        oid = len(orbits)
        orbits.append(o)
        for u in o:
            seen[u] = oid
    return orbits, seen


def solve(orbits, seen, ub=63, timelimit=30.0):
    """min sum |O| y_O  s.t. every v: sum_O |O cap B(v)| y_O >= 2, sum|C|<=ub.
    Identical formulation to prescribed.py's solve(), independent copy since
    this file must stand on its own as a distinct search instance generator.
    """
    K = len(orbits)
    sizes = np.array([len(o) for o in orbits], dtype=float)
    A = np.zeros((N, K))
    for v in range(N):
        for c in [v] + [v ^ (1 << i) for i in range(n)]:
            A[v, seen[c]] += 1.0
    A = np.unique(A, axis=0)
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("time_limit", timelimit)
    inf = highspy.kHighsInf
    h.addVars(K, np.zeros(K), np.ones(K))
    h.changeColsCost(K, np.arange(K, dtype=np.int32), sizes)
    h.changeColsIntegrality(K, np.arange(K, dtype=np.int32),
                             np.array([highspy.HighsVarType.kInteger] * K))
    for r in A:
        idx = np.nonzero(r)[0].astype(np.int32)
        h.addRow(2.0, inf, len(idx), idx, r[idx])
    allidx = np.arange(K, dtype=np.int32)
    h.addRow(-inf, float(ub), K, allidx, sizes)
    h.run()
    st = h.getModelStatus()
    name = h.modelStatusToString(st)
    if name == "Optimal":
        sol = h.getSolution()
        y = np.array(sol.col_value)
        code = sorted(c for j in range(K) if y[j] > 0.5 for c in orbits[j])
        return len(code), code, name
    return None, name, name


# ---------------------------------------------------------------- family 1

def partitions_into_r_parts(total, r, mx=None):
    if mx is None:
        mx = total
    if r == 1:
        if 1 <= total <= mx:
            yield (total,)
        return
    lo = 1
    for k in range(min(total - (r - 1), mx), lo - 1, -1):
        for rest in partitions_into_r_parts(total - k, r - 1, k):
            yield (k,) + rest


def swap_perm(block):
    """fixed-point-free involution pairing block[2i] with block[2i+1]."""
    pi = list(range(n))
    for i in range(0, len(block), 2):
        a, b = block[i], block[i + 1]
        pi[a], pi[b] = b, a
    return tuple(pi)


def flip_gens(block):
    """(pi=id, t=weight-w vector on block) for w = 1..len(block)."""
    out = []
    for w in range(1, len(block) + 1):
        t = 0
        for c in block[:w]:
            t |= 1 << c
        out.append((tuple(range(n)), t))
    return out


def swap_gens(block):
    """(pi=fpf involution on block, t=pi-invariant vector) for w'=0..m/2
    pairs set. Requires len(block) even and >= 2."""
    m = len(block)
    if m < 2 or m % 2 != 0:
        return []
    pi = swap_perm(block)
    pairs = [(block[i], block[i + 1]) for i in range(0, m, 2)]
    out = []
    for wprime in range(0, len(pairs) + 1):
        t = 0
        for a, b in pairs[:wprime]:
            t |= (1 << a) | (1 << b)
        out.append((pi, t))
    return out


def block_gen_choices(block):
    return [("flip", g) for g in flip_gens(block)] + \
           [("swap", g) for g in swap_gens(block)]


def sweep_elementary_abelian(ub, timelimit, log):
    results, unresolved = [], []
    best = (10**9, None, None)
    ninstances = 0
    for r in range(2, 6):
        for part in partitions_into_r_parts(n, r):
            blocks = []
            pos = 0
            for sz in part:
                blocks.append(tuple(range(pos, pos + sz)))
                pos += sz
            choices = [block_gen_choices(b) for b in blocks]
            counts = [len(c) for c in choices]
            total_combos = 1
            for c in counts:
                total_combos *= c
            log(f"family1 r={r} part={part} blocks={blocks} "
                f"combos={total_combos}")
            idxs = [0] * r

            def combos():
                idx = [0] * r
                while True:
                    yield tuple(choices[j][idx[j]] for j in range(r))
                    for j in range(r - 1, -1, -1):
                        idx[j] += 1
                        if idx[j] < counts[j]:
                            break
                        idx[j] = 0
                    else:
                        return
                    if all(x == 0 for x in idx):
                        return

            seen_combo = set()
            for combo in combos():
                key = tuple((kind, g) for kind, g in combo)
                if key in seen_combo:
                    continue
                seen_combo.add(key)
                gens = [g for _, g in combo]
                if all(g == IDENTITY for g in gens):
                    continue
                elems = closure(gens, cap=32)
                if elems is None or len(elems) not in (4, 8, 16, 32):
                    continue
                if is_cyclic(elems):
                    continue
                ninstances += 1
                orbits, seenv = group_orbits(elems)
                K = len(orbits)
                m, code, status = solve(orbits, seenv, ub=ub,
                                         timelimit=timelimit)
                label = f"family1 part={part} order={len(elems)} " \
                        f"orbits={K} kinds={[k for k,_ in combo]}"
                if m is None:
                    unresolved.append((status, label))
                    if status != "Infeasible":
                        log(f"  UNRESOLVED [{status}] {label}")
                    continue
                results.append((m, label))
                if m < best[0]:
                    best = (m, code, label)
                    log(f"  NEW BEST {m}  {label}")
    return results, unresolved, best, ninstances


# --------------------------------------------------------------- family 2

def sigma_orbits(m):
    """orbits of i -> -i mod m on {0,...,m-1}."""
    seen = [False] * m
    orbits = []
    for i in range(m):
        if seen[i]:
            continue
        j = (-i) % m
        if j == i:
            orbits.append((i,))
        else:
            orbits.append((i, j))
        seen[i] = seen[j] = True
    return orbits


def sweep_dihedral(ub, timelimit, log):
    results, unresolved = [], []
    best = (10**9, None, None)
    ninstances = 0
    for m in range(3, n + 1):
        block = tuple(range(m))
        rho = list(range(n))
        for i in range(m):
            rho[i] = (i + 1) % m
        rho = tuple(rho)
        r_gen = (rho, 0)
        orbs = sigma_orbits(m)
        log(f"family2 dihedral m={m} order={2*m} sigma_orbits={orbs} "
            f"combos={2**len(orbs)}")
        for mask in range(1 << len(orbs)):
            sigma = list(range(n))
            for i in range(m):
                sigma[i] = (-i) % m
            sigma = tuple(sigma)
            t = 0
            for bit, orb in enumerate(orbs):
                if (mask >> bit) & 1:
                    for c in orb:
                        t |= 1 << c
            s_gen = (sigma, t)
            # cap=64, not 32: a reflection translation that is sigma-
            # invariant but not the trivial or all-ones choice does NOT
            # generally satisfy the dihedral relation once translations are
            # included -- it can generate a strictly larger group (observed:
            # up to 2x-4x the target order 2m). Only masks 0 and all-ones
            # were found to reproduce the intended order-2m dihedral group;
            # every other mask is still a genuine subgroup of Aut(Q_8) and
            # is kept (not silently dropped) whenever its actual order lands
            # in [4, 32] -- the stated target range -- even though it is not
            # literally D_m. cap=64 lets a >32 group be *seen and rejected as
            # out of range*, rather than conflated with "did not close".
            elems = closure([r_gen, s_gen], cap=64)
            if elems is None or not (4 <= len(elems) <= 32):
                continue
            if is_cyclic(elems):
                continue
            ninstances += 1
            orbits, seenv = group_orbits(elems)
            K = len(orbits)
            mm, code, status = solve(orbits, seenv, ub=ub,
                                      timelimit=timelimit)
            label = f"family2 ring m={m} target_D_order={2*m} " \
                    f"actual_order={len(elems)} " \
                    f"orbits={K} refl_mask={mask:0{len(orbs)}b}"
            if mm is None:
                unresolved.append((status, label))
                if status != "Infeasible":
                    log(f"  UNRESOLVED [{status}] {label}")
                continue
            results.append((mm, label))
            if mm < best[0]:
                best = (mm, code, label)
                log(f"  NEW BEST {mm}  {label}")
    return results, unresolved, best, ninstances


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ub", type=int, default=63,
                     help="upper bound on |C| for the feasibility question")
    ap.add_argument("--timelimit", type=float, default=30.0,
                     help="per-instance HiGHS wall-clock limit (seconds)")
    ap.add_argument("--out", default="presc_noncyclic_best.json")
    ap.add_argument("--log", default=None)
    a = ap.parse_args()

    logf = open(a.log, "a") if a.log else None

    def log(msg):
        line = f"[{time.time()-t0:.0f}s] {msg}"
        print(line, flush=True)
        if logf:
            logf.write(line + "\n")
            logf.flush()

    t0 = time.time()
    log(f"start: ub<={a.ub}, per-instance timelimit={a.timelimit}s")

    r1, u1, b1, n1 = sweep_elementary_abelian(a.ub, a.timelimit, log)
    r2, u2, b2, n2 = sweep_dihedral(a.ub, a.timelimit, log)

    results = r1 + r2
    unresolved = u1 + u2
    best = min([b1, b2], key=lambda b: b[0])
    ninstances = n1 + n2

    log(f"family1 (elementary abelian): {n1} genuine non-cyclic instances, "
        f"{len(r1)} solved, {len(u1)} not Optimal")
    log(f"family2 (dihedral): {n2} genuine non-cyclic instances, "
        f"{len(r2)} solved, {len(u2)} not Optimal")

    resolved_neg = [x for x in unresolved if x[0] == "Infeasible"]
    truly_unresolved = [x for x in unresolved if x[0] != "Infeasible"]
    stat = Counter(s for s, _ in unresolved)
    log(f"total instances: {ninstances}")
    log(f"status counts (non-optimal): {dict(stat)}")
    log(f"TRULY UNRESOLVED (timeouts / other, not counted as negative): "
        f"{len(truly_unresolved)}")
    log(f"sweep is exhaustive over families 1+2 only if the count above is 0")
    log(f"BEST {best[0]} via {best[2]}  total {time.time()-t0:.0f}s")

    size_dist = sorted(Counter(m for m, _ in results).items())
    log(f"size distribution over solved instances: {size_dist}")

    json.dump({
        "size": best[0],
        "code": best[1],
        "label": best[2],
        "ub": a.ub,
        "timelimit": a.timelimit,
        "total_instances": ninstances,
        "solved_optimal": len(results),
        "infeasible": len(resolved_neg),
        "unresolved": len(truly_unresolved),
        "unresolved_detail": truly_unresolved,
        "size_distribution": size_dist,
        "wall_seconds": round(time.time() - t0, 1),
    }, open(a.out, "w"), indent=2)
    log(f"wrote {a.out}")

    if logf:
        logf.close()


if __name__ == "__main__":
    main()
