#!/usr/bin/env python3
"""CNF search model for K(n,1,2): is there an M-word double covering of Q_n?

    python3 sat_model.py --n 8 --M 63 --budget 20000000   # 2e7 conflict budget

Encoding (256 vars at n = 8):
  x_c        c is a codeword
  >= 2 of B(v) for every v, as (OR B(v)) and (OR B(v)\{c}) for each c in B(v)
  sum x_c <= M, totalizer (PySAT CardEnc)

Symmetry breaking (both sound; see WORKLOAD_ESTIMATE §4):
  translation  -- 0 in C, since C is nonempty and Aut(Q_n) is transitive
  coordinates  -- the stabiliser of 0 is S_n, so the weight-1 codewords may be
                  taken to be a prefix e_1..e_k

Requires: python-sat (pip install python-sat).  Verification is NOT done here;
pipe any model through verify.py.
"""
import argparse
import json
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical195


def ball(v, n):
    return [v] + [v ^ (1 << i) for i in range(n)]


def build(n, M, sym=True):
    N = 1 << n
    pool = IDPool(start_from=N + 1)
    var = lambda v: v + 1
    cnf = CNF()
    for v in range(N):
        b = ball(v, n)
        cnf.append([var(c) for c in b])
        for c in b:
            cnf.append([var(d) for d in b if d != c])
    cnf.extend(CardEnc.atmost(lits=[var(v) for v in range(N)], bound=M,
                              vpool=pool, encoding=EncType.totalizer).clauses)
    if sym:
        cnf.append([var(0)])
        for i in range(n - 1):
            cnf.append([-var(1 << (i + 1)), var(1 << i)])
    return cnf


def solve(n, M, budget=None, sym=True):
    t0 = time.time()
    cnf = build(n, M, sym)
    s = Cadical195(bootstrap_with=cnf.clauses)
    # A conflict budget, not a wall-clock budget: PySAT's Cadical195 does not
    # honour interrupt(), and a conflict count is hardware- and load-independent,
    # which is what an extrapolation needs.
    if budget is None:
        res = s.solve()
    else:
        s.conf_budget(int(budget))
        res = s.solve_limited()
    dt = time.time() - t0
    code = None
    if res:
        m = s.get_model()
        code = sorted(v for v in range(1 << n) if m[v] > 0)
    stats = s.accum_stats()
    s.delete()
    return {
        "n": n, "M": M, "sym": sym,
        "status": {True: "SAT", False: "UNSAT", None: "BUDGET_EXHAUSTED"}[res],
        "seconds": round(dt, 2),
        "vars": cnf.nv, "clauses": len(cnf.clauses),
        "conflicts": stats.get("conflicts"), "propagations": stats.get("propagations"),
        "code": code,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--budget", type=float, default=None,
                    help="conflict budget (not seconds); omit to run to completion")
    ap.add_argument("--nosym", action="store_true")
    ap.add_argument("-o", default=None)
    a = ap.parse_args()
    r = solve(a.n, a.M, a.budget, not a.nosym)
    code = r.pop("code")
    print(json.dumps(r))
    if code and a.o:
        json.dump(code, open(a.o, "w"))
        print("wrote", a.o, "size", len(code))
