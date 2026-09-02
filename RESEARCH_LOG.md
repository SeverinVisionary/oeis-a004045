# Research target: determine `K(8,1,2)` = `A004045(8)`

**Status:** admitted, prior-art gate passed, **planning + pilot only**. No
record claim.
**Published record:** `59 <= K(8,1,2) <= 64` (Krotov–Potapov 2020 / Östergård
1995) — see [`PRIOR_ART.md`](PRIOR_ART.md).
**This directory contains:** the gate, a reproduced incumbent, a standalone
verifier, two independent search models, a measured pilot, a costed plan, and —
since 2026-08-29 — a **certification leg**: machine-checkable proof objects and
a standalone re-checker ([`CERTIFICATION.md`](CERTIFICATION.md),
[`certs/MANIFEST.md`](certs/MANIFEST.md)).
**It does not claim a new bound.** Most certified statements in `certs/` and
`certs_exact/` are already published or *weaker* than the published lower bound
of 59. One is not: an exact-rational certificate for `K(8,1,2) > 59` was
accepted by `viprchk`. It rests on a single route, a single checker, and an
artifact too large to commit, and it is recorded as such —
see [`certs/MANIFEST.md`](certs/MANIFEST.md). It is **not** claimed as a
result and `PRIOR_ART.md` is unchanged.

## Exact statement

Find the minimum `|C|` over sets `C ⊆ F_2^8` such that every `x ∈ F_2^8` has at
least two codewords of `C` in its closed radius-1 Hamming ball `B(x)`
(`|B(x)| = 9`). This is `K(8,1,2)` in Cohen–Honkala–Litsyn–Lobstein Ch. 14
notation, the double-domination number `gamma_{x2}(Q_8)`, and the first unknown
term of OEIS [A004045](https://oeis.org/A004045).

Score direction: **minimise**. Normalisation: codewords are distinct (a *set*,
not a multiset). Frozen 2026-08-28.

## Why this row and not another

| Axis | Rating | Reasoning |
|---|---|---|
| `Tier` | **T2** for the upper bound, **T3** for full closure | 256 binary variables, 256 nine-term constraints. A witness is a 63-word list anyone can check in microseconds. Closure needs an exhaustive `M = 59..62` infeasibility proof with symmetry handling — the shape of Östergård–Blass's `K(9,1) = 62`, not of a breakthrough. |
| `Crowd` | **C1** | Seuranen 2007 has one citation (Krotov–Potapov); Krotov–Potapov's six citing papers all go to colorings, packings and 1-perfect codes. No one has published on this row in six years. |
| `Value` | **V3**, rising to **V4** on closure | Would add a term to a sequence flagged `hard,more` since 1996 and close the `n = 8` row of a table that has stood since 1993. Not a named open question. |

**`C1` diagnosis: neglected, not worthless.** The distinguishing evidence is
that the row *moved recently* — Krotov–Potapov lifted the `n = 8` lower bound
from Seuranen's value to 59 in 2020 as a corollary of a packing theorem, and
Tabatabai closed `n = 6, 7` in the same year with a solver. Two independent
2020 advances on adjacent cells is the signature of an under-attacked problem,
not a dead one. What is missing is that **nobody has pointed a modern
PB/SAT/MILP stack at `n = 8` and published the result.**

**The honest counterweight:** the published lower bound `59` is *cheap*. Stock
HiGHS reaches dual bound `59.0` on the raw 256-variable MILP in 120 s from a
cold start (§3 of the estimate). A bound that a general-purpose solver
reproduces in two minutes is exactly what `AGENTS.md` §0 warns about — it says
nothing about whether the *next* increment is cheap, and we assume it is not.

## The two finish paths

1. **Improve the upper bound** (`64 -> <= 63`). One verified witness is the
   whole deliverable. The cyclic prescribed-automorphism route is **closed and
   negative**: 745 of the 746 cyclic `(π, t)` classes admit no invariant code of
   size `<= 63` (estimate §3.2), so such a witness has trivial cyclic
   automorphism group. Attack: prescribed automorphisms over *non-cyclic*
   subgroups, local search
   (Östergård used tabu in 1995 — a 2026 stack should beat it), MaxSAT.
2. **Improve the lower bound / close the interval** (`59 -> 60..64`). Needs
   infeasibility proofs at `M = 59, 60, ...`, each an exhaustive statement.
   This is where essentially all the cost lives.

Costs for both, with measured pilot data and the extrapolation, are in
[`WORKLOAD_ESTIMATE_2026-08-28.md`](WORKLOAD_ESTIMATE_2026-08-28.md).

## Forced structure a solution must have

Total ball incidence is `9M` against a mandatory `2 * 256 = 512`, so the
**coverage excess** of an `M`-word double covering is exactly

```
E(M) = 9M - 512
```

| `M` | 59 | 60 | 61 | 62 | 63 | 64 |
|---|---:|---:|---:|---:|---:|---:|
| excess `E(M)` | 19 | 28 | 37 | 46 | 55 | 64 |

Writing `n_k` for the number of words covered exactly `k` times,
`sum_k n_k = 256` and `sum_k (k-2) n_k = E(M)`. At `M = 59` at most 19 of the
256 words may be covered more than twice, and at least 237 must be covered
*exactly* twice. A hypothetical 59-word code is therefore a near-perfect double
covering, which is strong branching material and the main reason the low end of
the interval is more attackable than its size suggests.

The reproduced incumbent (`C0 ∪ (C0 + e1)`, `C0 = H_7 × F_2`) has profile
`n_2 = 192, n_3 = 64`, excess 64 — maximally slack, consistent with it being a
lazy construction rather than an optimum.

## Layout

| File | Role |
|---|---|
| [`PRIOR_ART.md`](PRIOR_ART.md) | blocking gate: record, chain, forward-citation sweep, adjacent-notion audit |
| [`WORKLOAD_ESTIMATE_2026-08-28.md`](WORKLOAD_ESTIMATE_2026-08-28.md) | **the costed plan** — measured pilot, extrapolation, go/no-go |
| [`verify.py`](verify.py) | standalone verifier, stdlib only; also rebuilds the 64-word incumbent from the Hamming code |
| [`sat_model.py`](sat_model.py) | CNF search model (CaDiCaL via PySAT) |
| [`milp_model.py`](milp_model.py) | independent MILP search model (HiGHS) |
| [`scip_model.py`](scip_model.py) | third model (SCIP), used to take every infeasibility reading twice |
| [`prescribed.py`](prescribed.py) | prescribed-automorphism reduction over cyclic subgroups of `Aut(Q_8)` |
| [`prescribed_followup.py`](prescribed_followup.py) | re-solves the sweep instances that hit the 20 s limit, at `ub = 63` |
| [`prescribed_filter_audit.py`](prescribed_filter_audit.py) | names the `(π, t)` classes the sweep's orbit-count filter excludes |
| [`prescribed_excluded.py`](prescribed_excluded.py) | settles the three non-identity classes that filter drops |
| [`local_search.py`](local_search.py) | tabu search; **passes** the `n = 8` gate since 2026-09-01 (`python3 local_search.py --gate`) |
| [`logs/`](logs/) | raw pilot logs, seeds, solver versions, wall-clock, negative results |
| [`reviews/`](reviews/) | archived independent review of the prior-art gate |
| [`code64.json`](code64.json) | reproduced incumbent |
| [`CERTIFICATION.md`](CERTIFICATION.md) | **how to rebuild the certification pipeline and re-check every certificate from scratch** — exact versions, build flags, and what stays trusted |
| [`pb_encode.py`](pb_encode.py) | pseudo-Boolean (OPB) encoder — the instance a PB solver and an exact MILP both refute |
| [`pb_audit.py`](pb_audit.py) | encoding-faithfulness audit: the OPB rows must equal the rows `milp_model.py` feeds HiGHS, and known-good / deliberately-broken codes must agree with `verify.py` |
| [`certify.py`](certify.py) | route 1 driver — RoundingSat emits a VeriPB cutting-planes proof, VeriPB checks it |
| [`certify_exact.py`](certify_exact.py) | route 2 driver — exact-rational SCIP emits a VIPR certificate, `viprcomp` completes it, `viprchk` checks it |
| [`recheck.py`](recheck.py) | **the standalone checker** — re-derives each instance from the definition, re-hashes the artifacts, re-runs the route's checker, and requires it to reject the same proof against a deliberately weaker instance. Handles both routes. |
| [`certs/`](certs/) | route 1 artifacts, and [`certs/MANIFEST.md`](certs/MANIFEST.md): what is certified, by what, checked by what, with sizes, hashes and regeneration commands for **both** routes |
| [`certs_exact/`](certs_exact/) | route 2 artifacts — exact-rational MILP certificates over the *same* `.opb` files |

**Search and verification are separate implementations** (`AGENTS.md`): the
verifier shares no code with the models, uses no third-party package, and takes
a code as data.

## Known-answer gate

Before any `n = 8` run, both models reproduce every published term:

```
n = 4:  SAT at 8,  UNSAT at 7
n = 5:  SAT at 12, UNSAT at 11
n = 6:  SAT at 20, UNSAT at 19
n = 7:  SAT at 32, UNSAT at 31
```

`make gate` runs it, for all three models. A model that does not pass this is
not allowed to produce an `n = 8` statement. The local search **failed** this at
`n = 8` until 2026-09-01 and was quarantined; the cause was a bug, not a
performance limit (see the estimate, §3.2), and it now passes —
`python3 local_search.py --gate` finds a witness at every rung `n = 4..8`,
each re-verified by an independent coverage recount.

**The certification pipeline has its own gate, and it is a stronger one.**
`make certify-gate` does not merely reproduce the published terms — it
*certifies* them, with a proof object that a separate program checks:

```
K(6,1,2) = 20     VERIFIED BOUNDS 20 <= obj <= 20   (VeriPB 3.0.2)
K(7,1,2) = 32     VERIFIED BOUNDS 32 <= obj <= 32
K(6,1,2) > 19     VERIFIED UNSATISFIABLE
K(7,1,2) > 31     VERIFIED UNSATISFIABLE
```

`K(6,1,2) = 20` is the one that matters: `n = 6` is the smallest case whose
lower bound is *not* the sphere bound (`7·19 = 133 >= 128`), so it is the
smallest instance where the machinery has to do real work. `make recheck`
re-verifies every committed certificate from its artifacts alone.
