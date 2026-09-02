#!/usr/bin/env python3
"""Prescribed-automorphism search for minimum double coverings of Q_n.

Restrict to codes invariant under a cyclic subgroup G = <(pi, t)> of
Aut(Q_n) = F_2^n : S_n, acting by x -> pi(x) xor t. Variables become G-orbits,
so the ILP shrinks from 256 columns to |orbits|, and each instance solves in
seconds. This is the cheap high-symmetry sweep: it either hands back a small
witness or rules the whole symmetric stratum out.

Two reductions keep the sweep finite:
  * pi ranges over the 22 cycle types of S_8 (conjugate pi give conjugate G);
  * t ranges over coset representatives of the image of (1 + pi), because
    conjugating by the translation s sends (pi, t) to (pi, t xor s xor pi(s)).

    python3 prescribed.py            # full sweep, prints every improvement

Requires: highspy, numpy. Witnesses must still be checked by verify.py.
"""
import sys, time, itertools, json
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

def cyc_group(g):
    """orbits of <g> on F_2^n, plus the order of g"""
    seen = [-1] * N
    orbits = []
    for v in range(N):
        if seen[v] >= 0:
            continue
        o = []
        u = v
        while seen[u] < 0:
            seen[u] = len(orbits)
            o.append(u)
            u = elem_act(g, u)
        orbits.append(o)
    return orbits, seen

def solve(orbits, seen, ub=64, timelimit=20.0):
    """min sum |O| y_O  s.t. every v: sum_O |O cap B(v)| y_O >= 2"""
    K = len(orbits)
    sizes = np.array([len(o) for o in orbits], dtype=float)
    A = np.zeros((N, K))
    for v in range(N):
        for c in [v] + [v ^ (1 << i) for i in range(n)]:
            A[v, seen[c]] += 1.0
    # dedupe identical rows
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
    # |C| <= ub
    allidx = np.arange(K, dtype=np.int32)
    h.addRow(-inf, float(ub), K, allidx, sizes)
    h.run()
    st = h.getModelStatus()
    name = h.modelStatusToString(st)
    if name == "Optimal":
        sol = h.getSolution()
        y = np.array(sol.col_value)
        code = sorted(c for j in range(K) if y[j] > 0.5 for c in orbits[j])
        return len(code), code
    return None, name

def cycle_type_perm(part):
    pi = [0] * n
    pos = 0
    for L in part:
        for k in range(L):
            pi[pos + k] = pos + (k + 1) % L
        pos += L
    return pi

def partitions(m, mx=None):
    if mx is None: mx = m
    if m == 0:
        yield ()
        return
    for k in range(min(m, mx), 0, -1):
        for rest in partitions(m - k, k):
            yield (k,) + rest

if __name__ == "__main__":
    best = (10**9, None, None)
    t0 = time.time()
    results = []
    nonoptimal = []
    parts = list(partitions(n))
    print(f"{len(parts)} cycle types", flush=True)
    def coker_reps(pi):
        """t matters only modulo image of (1+pi): (pi,t) ~ (pi, t^s^pi(s))."""
        img = set()
        for s in range(N):
            img.add(s ^ perm_act(pi, s))
        img = sorted(img)
        seen = set(); reps = []
        for t in range(N):
            if t in seen: continue
            reps.append(t)
            for u in img: seen.add(t ^ u)
        return reps
    ngroups = 0
    for part in parts:
        pi = cycle_type_perm(part)
        reps = coker_reps(pi)
        print(f"cycle type {part}: {len(reps)} translation classes  [{time.time()-t0:.0f}s]", flush=True)
        for t in reps:
            orbits, seen = cyc_group((pi, t))
            K = len(orbits)
            if K > 140 or K < 8:      # keep the reduction meaningful
                continue
            ngroups += 1
            m, code = solve(orbits, seen, ub=64, timelimit=20.0)
            if m is None:
                # `code` holds the HiGHS status string. "Infeasible" is a
                # genuine negative (no G-invariant covering of size <= 64);
                # anything else (notably a time limit) leaves the instance
                # UNRESOLVED and must not be counted as a negative.
                nonoptimal.append((str(code), part, t, K))
                if code != "Infeasible":
                    print(f"  UNRESOLVED [{code}]  cycle type {part} t={t} "
                          f"orbits={K}  [{time.time()-t0:.0f}s]", flush=True)
                continue
            results.append((m, part, t, K))
            if m < best[0]:
                best = (m, code, (part, t, K))
                print(f"  new best {m}  cycle type {part} t={t} orbits={K}  [{time.time()-t0:.0f}s]", flush=True)
    print("groups solved:", ngroups)
    from collections import Counter as _C
    nstat = _C(s for s, _, _, _ in nonoptimal)
    print("non-optimal instances:", dict(nstat) or "none")
    unresolved = [r for r in nonoptimal if r[0] != "Infeasible"]
    print("UNRESOLVED (sweep is exhaustive only if this is 0):", len(unresolved))
    print("BEST", best[0], best[2], f"total {time.time()-t0:.0f}s")
    json.dump({"size": best[0], "code": best[1], "group": str(best[2])},
              open("presc_best.json", "w"))
    from collections import Counter
    print("size distribution over groups:", sorted(Counter(r[0] for r in results).items()))
