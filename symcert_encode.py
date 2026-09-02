#!/usr/bin/env python3
"""OPB encoder for one prime-order-symmetric orbit-ILP of the Q_8 symmetry
theorem (SYMMETRY_THEOREM.md).

Independent of symmetry_prime.py: this module imports only symcert_reps.py
(the from-scratch representative/orbit derivation checked in that file), and
never imports symmetry_prime itself or any of its functions. The instances
this file writes are checked by RoundingSat/VeriPB or exact SCIP/VIPR -- an
independent encoder is the point of the exercise, not a formality.

Encoding, for a fixed representative g = (perm, t) with orbits O_1 .. O_k of
<g> acting on F_2^8:

    one 0/1 variable y_i per orbit O_i        (an invariant code is a union
                                                of whole orbits)
    coverage:  for every vertex v of F_2^8,
                   sum_i cov(v, O_i) * y_i >= mu
               where cov(v, O_i) = |B(v) intersect O_i|, B(v) the closed
               Hamming ball of radius 1 around v (n+1 = 9 points)
    cardinality:  sum_i |O_i| * y_i <= ub          (ub = 63 for the refutation
                                                     instances, 64 for the
                                                     feasibility controls)

256 coverage rows are emitted, one per vertex, exactly as the theorem states
it ("coverage >= 2 at every vertex") -- not collapsed to one row per orbit,
even though rows for vertices in the same orbit are always identical (g maps
orbits to themselves, so ball(g(v)) and ball(v) meet the same orbits with the
same multiplicities). Keeping all 256 makes the instance checkable directly
against the English statement without a "why are there only k rows" step.
"""
import argparse
import hashlib
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
import symcert_reps  # noqa: E402

N = 8
UNIVERSE = 1 << N


def ball(v):
    return [v] + [v ^ (1 << i) for i in range(N)]


def orbit_index_map(orbs):
    idx = {}
    for oi, o in enumerate(orbs):
        for v in o:
            idx[v] = oi
    return idx


def opb_lines(label, perm, t, orbs, ub, mu=2):
    idx = orbit_index_map(orbs)
    k = len(orbs)
    sizes = [len(o) for o in orbs]

    rows = []  # list of (dict orbit_index->coeff, rhs)
    for v in range(UNIVERSE):
        counts = {}
        for w in ball(v):
            oi = idx[w]
            counts[oi] = counts.get(oi, 0) + 1
        rows.append((counts, mu))
    # cardinality, in >= form: -sum |O_i| y_i >= -ub
    card = {oi: -sizes[oi] for oi in range(k)}
    rows.append((card, -ub))

    nc = len(rows)
    widest = [len(str(mu)), len(str(-ub))]
    for counts, rhs in rows:
        widest.extend(len(str(c)) for c in counts.values())
        widest.append(len(str(rhs)))
    intsize = max(widest)

    yield "* #variable= %d #constraint= %d #equal= 0 intsize= %d" % (k, nc, intsize)
    yield "* prime-order-symmetric orbit-ILP for class %s (order %d, %d orbits)" % (
        label, symcert_reps.element_order(perm, t), k)
    yield "* x{i+1} = 1  iff  orbit O_i (0-indexed) is included in the invariant code"
    yield "* coverage: sum_i cov(v,O_i) y_i >= %d for every vertex v in F_2^%d (256 rows)" % (mu, N)
    yield "* cardinality: sum_i |O_i| y_i <= %d, in >= form" % ub
    for counts, rhs in rows[:-1]:
        terms = " ".join("+%d x%d" % (c, oi + 1) for oi, c in sorted(counts.items()))
        yield "%s >= %d ;" % (terms, rhs)
    counts, rhs = rows[-1]
    terms = " ".join("%d x%d" % (c, oi + 1) for oi, c in sorted(counts.items()))
    yield "%s >= %d ;" % (terms, rhs)


def write_opb(path, label, perm, t, orbs, ub, mu=2):
    body = "\n".join(opb_lines(label, perm, t, orbs, ub, mu)) + "\n"
    with open(path, "w") as f:
        f.write(body)
    return {
        "path": path, "label": label, "ub": ub, "mu": mu,
        "orbits": len(orbs),
        "variables": len(orbs),
        "constraints": UNIVERSE + 1,
        "bytes": len(body.encode()),
        "sha256": hashlib.sha256(body.encode()).hexdigest(),
    }


def orbit_code_from_selection(orbs, selected_orbit_indices):
    """Expand a set of selected orbit indices back into a flat word list --
    used by the ub=64 feasibility control to hand a genuine code to verify.py.
    """
    out = []
    for oi in selected_orbit_indices:
        out.extend(orbs[oi])
    return sorted(out)


def find_class(label):
    for c in symcert_reps.validated_classes():
        if c["label"] == label:
            return c
    raise KeyError("no such class: %s" % label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True, help="e.g. p7_a1, p2_a2_b4_c0")
    ap.add_argument("--ub", type=int, default=63)
    ap.add_argument("--mu", type=int, default=2)
    ap.add_argument("-o", default=None)
    a = ap.parse_args()
    c = find_class(a.label)
    if a.o is None:
        for line in opb_lines(c["label"], c["perm"], c["t"], c["orbits"], a.ub, a.mu):
            print(line)
        return 0
    import json
    meta = write_opb(a.o, c["label"], c["perm"], c["t"], c["orbits"], a.ub, a.mu)
    meta["order"] = c["order"]
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
