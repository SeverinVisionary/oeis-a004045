#!/usr/bin/env python3
"""Tabu search for a double covering of Q_n of fixed size M.

Rewrite of local_search.py, which was quarantined for failing the n=8 gate.
Three defects there, in order of importance:

  1. The tabu list was inert. A word was marked tabu at the moment it was
     removed from the code, but the tabu test ran only over words *in* the
     code -- so the mark could never fire, and nothing prevented re-adding the
     word just dropped. The search was a random walk.
  2. Cost was recomputed with an O(2^n) sum every iteration although the exact
     delta had already been computed for the move.
  3. The added word was chosen uniformly at random rather than by gain.

Here the tabu forbids RE-ADDING a recently removed word, cost is maintained
incrementally, and both ends of the swap are chosen greedily.

    python3 ls2.py --n 8 --M 64 --restarts 20 --iters 200000
"""
import argparse
import json
import random
import time


def neighbours(n):
    N = 1 << n
    return [tuple([v] + [v ^ (1 << i) for i in range(n)]) for v in range(N)]


def search(n, M, mu, iters, seed, tenure=None, report=None):
    N = 1 << n
    nb = neighbours(n)
    rng = random.Random(seed)
    if tenure is None:
        tenure = max(6, M // 8)

    code = set(rng.sample(range(N), M))
    cov = [0] * N
    for c in code:
        for v in nb[c]:
            cov[v] += 1
    cost = sum(mu - k for k in cov if k < mu)
    best = cost
    best_code = sorted(code)
    tabu_until = {}          # word -> iteration before which it may not be re-ADDED

    for it in range(iters):
        if cost == 0:
            return 0, sorted(code), it
        deficient = [v for v in range(N) if cov[v] < mu]
        v = rng.choice(deficient)

        # --- choose the word to add, by immediate gain, respecting tabu ---
        cands = [c for c in nb[v] if c not in code]
        if not cands:
            cands = [c for c in range(N) if c not in code]
        scored = []
        for a in cands:
            if tabu_until.get(a, -1) > it:
                continue
            g = sum(1 for u in nb[a] if cov[u] < mu)
            scored.append((-g, a))
        if not scored:                       # everything tabu: take any
            scored = [(0, rng.choice(cands))]
        scored.sort()
        topg = scored[0][0]
        add = rng.choice([a for g, a in scored if g == topg])
        badd = set(nb[add])

        # --- choose the word to drop, by least damage, over the whole code ---
        gain = sum(1 for u in badd if cov[u] < mu)
        bestdrop, bestloss = None, None
        for c in code:
            loss = 0
            for u in nb[c]:
                k = cov[u] + (1 if u in badd else 0)
                if k - 1 < mu:
                    loss += 1
            if bestloss is None or loss < bestloss:
                bestdrop, bestloss = c, loss
        # apply
        code.discard(bestdrop)
        code.add(add)
        for u in badd:
            cov[u] += 1
        for u in nb[bestdrop]:
            cov[u] -= 1
        cost += bestloss - gain
        tabu_until[bestdrop] = it + tenure + rng.randint(0, 4)
        if cost < best:
            best, best_code = cost, sorted(code)
            if report:
                report(it, cost)
    return best, best_code, iters


RUNGS_MAX_RESTARTS = 20


def gate(verbose=True):
    """Known-answer gate: find a witness at every published term, n = 4..8.

    The previous implementation passed n <= 7 and stalled at cost 11 on
    n = 8, M = 64 -- a case where a solution is known to exist. That was
    recorded in the workload estimate as evidence that a C rewrite was needed.
    It was not: it was the inert tabu list (see the module docstring).
    """
    rungs = [(4, 8), (5, 12), (6, 20), (7, 32), (8, 64)]
    ok = True
    for n, M in rungs:
        t0 = time.time()
        # Restarts are part of the method, not a workaround: a single descent
        # can land in a local minimum of positive cost even at M = 64, where a
        # solution certainly exists. Seed 20260901 does exactly that.
        cost, code, used, restarts = None, None, 0, 0
        for r in range(RUNGS_MAX_RESTARTS):
            restarts = r + 1
            cost, code, used = search(n, M, 2, 200000, 20260901 + r)
            if cost == 0:
                break
        good = cost == 0 and len(code) == M and len(set(code)) == M
        if good:                       # re-verify from scratch, sharing no state
            cov = [0] * (1 << n)
            for c in code:
                cov[c] += 1
                for i in range(n):
                    cov[c ^ (1 << i)] += 1
            good = min(cov) >= 2
        ok &= good
        if verbose:
            print("  n=%d M=%2d  cost=%d  restarts=%2d  iters=%6d  %5.1fs  %s"
                  % (n, M, cost, restarts, used, time.time() - t0,
                     "PASS" if good else "FAIL"))
    assert ok, "known-answer gate FAILED -- do not use this model for n=8 claims"
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--M", type=int, default=None)
    ap.add_argument("--mu", type=int, default=2)
    ap.add_argument("--restarts", type=int, default=50)
    ap.add_argument("--iters", type=int, default=50000)
    ap.add_argument("--seed", type=int, default=20260901)
    ap.add_argument("-o", default=None)
    ap.add_argument("--gate", action="store_true",
                    help="run the known-answer gate and exit")
    a = ap.parse_args()
    if a.gate:
        print("== local search known-answer gate ==")
        gate()
        raise SystemExit(0)
    t0 = time.time()
    overall, witness = None, None
    for r in range(a.restarts):
        cost, code, used = search(a.n, a.M, a.mu, a.iters, a.seed + r)
        if overall is None or cost < overall:
            overall, witness = cost, code
            print(json.dumps({"restart": r, "best_cost": cost, "iters_used": used,
                              "seconds": round(time.time() - t0, 1)}), flush=True)
        if overall == 0:
            break
    print(json.dumps({"n": a.n, "M": a.M, "mu": a.mu, "restarts": a.restarts,
                      "iters": a.iters, "seed": a.seed, "best_cost": overall,
                      "seconds": round(time.time() - t0, 1)}))
    if overall == 0 and a.o:
        json.dump(witness, open(a.o, "w"))
        print("WITNESS written to", a.o)
