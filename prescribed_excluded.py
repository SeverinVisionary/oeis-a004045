#!/usr/bin/env python3
"""Settle the three non-identity (pi, t) classes the orbit filter excluded.

`prescribed_filter_audit.py` shows the sweep's 8 <= K <= 140 filter drops
exactly four pairs, all with t = 0:

    (2,2,2,1,1)       K=144
    (2,2,1,1,1,1)     K=160
    (2,1,1,1,1,1,1)   K=192
    (1,1,1,1,1,1,1,1) K=256   <- the identity: the unrestricted problem, not a
                                 symmetry restriction, so out of scope here.

The first three are real symmetry classes and are settled here at ub = 63, the
question that actually matters: is there a G-invariant double covering of size
<= 63?

    python3 prescribed_excluded.py --timelimit 3600
"""
import argparse
import json
import time

from prescribed import cycle_type_perm, cyc_group, solve

TARGETS = [((2, 2, 2, 1, 1), 0), ((2, 2, 1, 1, 1, 1), 0),
           ((2, 1, 1, 1, 1, 1, 1), 0)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timelimit", type=float, default=3600.0)
    ap.add_argument("--ub", type=int, default=63)
    a = ap.parse_args()
    t0 = time.time()
    best = (10 ** 9, None, None)
    open_ = []
    for part, t in TARGETS:
        pi = cycle_type_perm(part)
        orbits, seen = cyc_group((pi, t))
        K = len(orbits)
        m, code = solve(orbits, seen, ub=a.ub, timelimit=a.timelimit)
        el = time.time() - t0
        if m is None:
            status = str(code)
            print(f"{part} t={t} orbits={K}: {status}  [{el:.0f}s]", flush=True)
            if status != "Infeasible":
                open_.append((part, t, K, status))
            continue
        print(f"{part} t={t} orbits={K}: min={m}  [{el:.0f}s]", flush=True)
        if m < best[0]:
            best = (m, code, (part, t, K))
    print("still open:", len(open_))
    print("BEST", best[0], best[2], f"total {time.time()-t0:.0f}s")
    if best[1]:
        json.dump(best[1], open("presc_excluded_best.json", "w"))
        print("wrote presc_excluded_best.json size", len(best[1]))


if __name__ == "__main__":
    main()
