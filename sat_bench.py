#!/usr/bin/env python3
"""How does a SAT refutation of M=59/60 compare with the MILP route?

Uses the repository's own CNF model (sat_model.build), WITHOUT symmetry
breaking, because a certificate must be about the unrestricted problem.
Symmetry breaking is timed separately for reference only.

Control: n=6, M=20 must be SATISFIABLE.
"""
import functools, sys, time
print = functools.partial(print, flush=True)
sys.path.insert(0, "<local-path-redacted>")
from sat_model import build
from pysat.solvers import Cadical195

def run(n, M, sym, budget=None):
    cnf = build(n, M, sym=sym)
    s = Cadical195(bootstrap_with=cnf.clauses)
    t = time.time()
    r = s.solve() if budget is None else s.solve_limited(expect_interrupt=False)
    el = time.time() - t
    st = s.accum_stats()
    s.delete()
    return ("SAT" if r else "UNSAT" if r is False else "UNKNOWN"), el, st.get('conflicts'), len(cnf.clauses)

print("=== control: n=6, M=20 must be SAT ===")
r, el, cf, nc = run(6, 20, False)
print("   %s  %.1fs  conflicts=%s  clauses=%d" % (r, el, cf, nc))
assert r == "SAT", "CONTROL FAILED: an achievable size came back UNSAT; encoding is wrong"
print("   control passes.\n")

for M in (58, 59, 60):
    for sym in (False, True):
        r, el, cf, nc = run(8, M, sym)
        print("  n=8 M=%d sym=%-5s  %-7s %8.1fs  conflicts=%-9s clauses=%d"
              % (M, sym, r, el, cf, nc))
