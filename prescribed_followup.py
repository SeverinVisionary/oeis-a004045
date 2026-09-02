#!/usr/bin/env python3
"""Re-solve the prescribed-automorphism instances that the 20 s sweep left open.

`prescribed.py` gives each orbit-ILP a 20 s limit and (before instrumentation)
silently discarded every non-optimal outcome. That conflates two very different
things:

  * "Infeasible"        -- a genuine negative: no G-invariant double covering
                           of size <= 64 exists for that group;
  * "Time limit reached" -- the instance is simply UNRESOLVED.

The unresolved instances are the ones with the largest orbit counts, i.e. the
*least* symmetric groups -- exactly where a code below 64 is most likely to
survive. So "the minimum G-invariant double covering is 64" is not an
exhaustive negative until these are closed.

This script parses the sweep log for UNRESOLVED lines and re-solves each with a
long time limit, reporting any code of size < 64 it finds.

    python3 prescribed_followup.py logs/prescribed_cyclic_sweep_full.log --timelimit 900

Requires: highspy, numpy. Any witness must still be checked by verify.py.
"""
import argparse
import ast
import json
import re
import time

from prescribed import cycle_type_perm, cyc_group, solve

# Matches both the sweep's "UNRESOLVED [...] cycle type (..) t=N orbits=K" and
# this script's own "STILL OPEN [...] (..) t=N orbits=K", so a run can be
# escalated by feeding its own log back in with a longer --timelimit.
LINE = re.compile(
    r"(?:UNRESOLVED|STILL OPEN) \[(?P<status>[^\]]+)\]\s+(?:cycle type )?"
    r"(?P<part>\([^)]*\))\s+t=(?P<t>\d+)\s+orbits=(?P<K>\d+)")


def parse(path):
    out = []
    with open(path) as fh:
        for line in fh:
            m = LINE.search(line)
            if m:
                part = ast.literal_eval(m.group("part"))
                if isinstance(part, int):
                    part = (part,)
                out.append((part, int(m.group("t")), int(m.group("K"))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--timelimit", type=float, default=900.0)
    ap.add_argument("--ub", type=int, default=63,
                    help="ask the research question directly: is there a "
                         "G-invariant covering of size <= ub? ub=63 is both "
                         "the question we care about and cheaper than proving "
                         "optimality at 64.")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    a = ap.parse_args()

    todo = parse(a.log)
    todo = [x for i, x in enumerate(todo) if i % a.nshards == a.shard]
    print(f"{len(todo)} unresolved instances to re-solve, "
          f"{a.timelimit:.0f}s each, ub={a.ub}", flush=True)

    t0 = time.time()
    best = (10 ** 9, None, None)
    still_open, resolved = [], []
    for part, t, K in todo:
        pi = cycle_type_perm(part)
        orbits, seen = cyc_group((pi, t))
        m, code = solve(orbits, seen, ub=a.ub, timelimit=a.timelimit)
        el = time.time() - t0
        if m is None:
            status = str(code)
            if status == "Infeasible":
                resolved.append((part, t, K, "Infeasible"))
                print(f"  Infeasible  {part} t={t} orbits={K}  [{el:.0f}s]",
                      flush=True)
            else:
                still_open.append((part, t, K, status))
                print(f"  STILL OPEN [{status}]  {part} t={t} orbits={K} "
                      f" [{el:.0f}s]", flush=True)
            continue
        resolved.append((part, t, K, m))
        print(f"  min={m}  {part} t={t} orbits={K}  [{el:.0f}s]", flush=True)
        if m < best[0]:
            best = (m, code, (part, t, K))
            print(f"  *** new best {m}  {part} t={t} orbits={K}", flush=True)

    print("resolved:", len(resolved), " still open:", len(still_open))
    print("EXHAUSTIVE" if not still_open else "NOT EXHAUSTIVE")
    print("BEST", best[0], best[2], f"total {time.time()-t0:.0f}s")
    if best[1]:
        fn = "presc_followup_best_shard%d.json" % a.shard
        json.dump(best[1], open(fn, "w"))
        print("wrote", fn, "size", len(best[1]))


if __name__ == "__main__":
    main()
