#!/usr/bin/env python3
"""OPB (pseudo-Boolean) encoder for the K(n,r=1,mu) decision problem.

Emits the *decision* instance "does a mu-fold radius-1 covering of F_2^n with
at most M codewords exist?" in OPB format, ready for a pseudo-Boolean solver
that logs a VeriPB cutting-planes proof.

    python3 pb_encode.py --n 8 --M 60 -o inst_n8_M60.opb

Encoding, in full
-----------------
One 0/1 variable per word of F_2^n:

    x{v+1} = 1  iff  v is in the code C          (v = 0 .. 2^n - 1)

so OPB variable ``x1`` is the word 0 and ``x{2^n}`` is the word 2^n - 1.
There are exactly 2^n variables and 2^n + 1 constraints:

  * coverage, one per word v of F_2^n (2^n constraints)

        sum_{c in B(v)} x_c >= mu,      B(v) = {v} u {v ^ 2^i : i < n}

    i.e. every word must have at least mu codewords in its closed radius-1
    Hamming ball, which has n+1 members.

  * cardinality, one constraint

        sum_v x_v <= M,   written in OPB's >= form as  -sum_v x_v >= -M.

This is a *set* formulation: a variable is in or out, so codewords are
automatically distinct, matching README.md's normalisation and verify.py.

Relation to the other models
----------------------------
The feasible set is by construction identical to `milp_model.py`'s
(`--mode M`) and `scip_model.py`'s: the same 2^n binary variables, the same
2^n ball rows with the same right-hand side, and the same single cardinality
row. `pb_audit.py` checks that claim mechanically rather than by inspection --
it reads the constraint rows straight out of the HiGHS model that
`milp_model.py` actually builds and compares them to a fresh parse of the OPB
file. No symmetry breaking is added: a refutation of this file is a refutation
of the unrestricted problem, with nothing further to justify.

Standard library only.
"""
import argparse
import hashlib
import sys


def ball(v, n):
    """Closed radius-1 Hamming ball around v, as a sorted list of words."""
    return sorted([v] + [v ^ (1 << i) for i in range(n)])


def opb_lines(n, M, mu=2):
    """Yield the OPB file for K(n,1,mu) <= M, line by line, without newlines.

    `M = None` emits the *optimisation* form instead: objective `min sum_v x_v`
    and no cardinality constraint. A solver that proves a lower bound `L` on
    that objective certifies `K(n,1,mu) >= L` -- one proof covering every rung
    below `L` at once, rather than one refutation per rung -- and if it proves
    matching bounds, `K(n,1,mu) = L` outright. The two forms carry the same
    coverage constraints and differ only in the objective and the last row.

    The header carries the `#equal=` and `intsize=` fields of the PB
    competition 2024 revision. They are not decoration: RoundingSat refuses
    the file with "Invalid opb header." when proof logging is on and they are
    absent, because the proof's `f` line has to count the constraints the
    checker will load. `#equal=` is 0 (this encoder emits only `>=`), and
    `intsize` is the widest integer in the file, in characters.
    """
    N = 1 << n
    nc = N if M is None else N + 1
    # widest integer in the file, in characters: coefficients are "+1"/"-1",
    # degrees are mu and (for the decision form) -M
    widest = [2, len(str(mu))] + ([] if M is None else [len(str(-M))])
    intsize = max(widest)
    yield "* #variable= %d #constraint= %d #equal= 0 intsize= %d" % (N, nc, intsize)
    if M is None:
        yield "* K(n,r=1,mu) optimisation instance: n=%d mu=%d, minimise |C|" % (n, mu)
    else:
        yield "* K(n,r=1,mu) decision instance: n=%d mu=%d M=%d" % (n, mu, M)
    yield "* x{v+1} = 1  iff  word v in {0..%d} is a codeword" % (N - 1)
    yield "* coverage: sum_{c in B(v)} x_c >= %d for every v; B(v) = ball of radius 1" % mu
    if M is None:
        yield "* objective: minimise sum_v x_v = |C|"
        yield "min: %s ;" % " ".join("+1 x%d" % (v + 1) for v in range(N))
    else:
        yield "* cardinality: sum_v x_v <= %d, in >= form" % M
    for v in range(N):
        terms = " ".join("+1 x%d" % (c + 1) for c in ball(v, n))
        yield "%s >= %d ;" % (terms, mu)
    if M is not None:
        terms = " ".join("-1 x%d" % (v + 1) for v in range(N))
        yield "%s >= %d ;" % (terms, -M)


def write_opb(path, n, M, mu=2):
    body = "\n".join(opb_lines(n, M, mu)) + "\n"
    with open(path, "w") as f:
        f.write(body)
    return {
        "path": path, "n": n, "M": M, "mu": mu,
        "variables": 1 << n,
        "constraints": (1 << n) + (0 if M is None else 1),
        "bytes": len(body.encode()),
        "sha256": hashlib.sha256(body.encode()).hexdigest(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--M", type=int, default=None,
                    help="cardinality bound |C| <= M; omit with --opt")
    ap.add_argument("--opt", action="store_true",
                    help="emit the optimisation form (minimise |C|, no cardinality row)")
    ap.add_argument("--mu", type=int, default=2)
    ap.add_argument("-o", default=None, help="output file (default: stdout)")
    a = ap.parse_args()
    if a.opt:
        a.M = None
    elif a.M is None:
        ap.error("give --M or --opt")
    if a.o is None:
        for line in opb_lines(a.n, a.M, a.mu):
            print(line)
        return 0
    import json
    print(json.dumps(write_opb(a.o, a.n, a.M, a.mu), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
