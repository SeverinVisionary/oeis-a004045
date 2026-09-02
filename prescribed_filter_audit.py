#!/usr/bin/env python3
"""Audit which (pi, t) pairs the sweep's orbit-count filter excludes.

`prescribed.py` skips any cyclic group whose orbit count K falls outside
8 <= K <= 140. The sweep's negative result is exhaustive only over the pairs
that pass, so the excluded ones have to be named rather than left implicit.

    python3 prescribed_filter_audit.py
"""
from prescribed import cycle_type_perm, cyc_group, partitions, perm_act, n, N


def coker_reps(pi):
    img = set()
    for s in range(N):
        img.add(s ^ perm_act(pi, s))
    img = sorted(img)
    seen, reps = set(), []
    for t in range(N):
        if t in seen:
            continue
        reps.append(t)
        for u in img:
            seen.add(t ^ u)
    return reps


def main():
    total = passed = 0
    excluded = []
    for part in partitions(n):
        pi = cycle_type_perm(part)
        for t in coker_reps(pi):
            total += 1
            orbits, _ = cyc_group((pi, t))
            K = len(orbits)
            if K > 140 or K < 8:
                excluded.append((part, t, K))
            else:
                passed += 1
    print("total (pi,t) pairs:", total)
    print("passed filter 8 <= K <= 140:", passed)
    print("excluded:", len(excluded))
    for part, t, K in excluded:
        note = "  <-- identity, t=0: the unrestricted 256-variable problem" \
            if K == N else ""
        print(f"  cycle type {part} t={t} orbits={K}{note}")


if __name__ == "__main__":
    main()
