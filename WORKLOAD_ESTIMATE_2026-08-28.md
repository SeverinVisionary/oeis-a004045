# `K(8,1,2)` — compute and calendar estimate

**Date:** 2026-08-28 America/Los_Angeles, §5 revised 2026-08-29
**Status:** planning estimate, a measured pilot, and — since 2026-08-29 — a
built and measured certification leg. **Not a mathematical result.** No bound
in this file is claimed as new. §5 now reports what certification *cost*
rather than what it was expected to cost, and `certs/MANIFEST.md` reports
exactly which statements a checker has accepted.
**Prior art frozen at:** `59 <= K(8,1,2) <= 64` — [`PRIOR_ART.md`](PRIOR_ART.md).

---

## 1. What "done" means

Two independent deliverables. Either alone is publishable; both together
determine `A004045(8)`.

| Path | Deliverable | Checkable by |
|---|---|---|
| **U** — upper bound | one code of size `<= 63` | `verify.py`, microseconds, by anyone |
| **L** — lower bound | infeasibility at `M = 59, 60, ...` | only by a proof object; this is where the cost is |

Closure needs `U` at some `M*` and `L` at `M* - 1`. Because the published
interval is `59..64`, the work is at most five infeasibility rungs
(`59, 60, 61, 62, 63`) and at most five feasibility probes.

**Infeasibility gets harder as `M` grows.** The last rung below the true value
dominates the whole budget. If `K(8,1,2) = 64`, the bill is essentially the
cost of rung `M = 63` alone.

---

## 2. Known-answer gates (passed before any `n = 8` run)

`AGENTS.md` §1: check the cases whose answers you already know first. Both
search models reproduce every published term, and every witness they emit is
re-checked by `verify.py`, which shares no code with either model.

| `n` | `M` | expected | MILP (HiGHS 1.15.1) | MILP (SCIP 10.0) | CNF (CaDiCaL via PySAT 1.9) |
|---:|---:|---|---|---|---|
| 4 | 8 / 7 | feasible / infeasible | — | — | SAT 11 confl / UNSAT 48 confl |
| 5 | 12 / 11 | feasible / infeasible | — | — | SAT 350 / UNSAT 636 |
| 6 | 20 / 19 | feasible / infeasible | 0.0 s / 0.1 s | 0.0 s / 0.1 s | SAT 10 018 / UNSAT 67 423 (0.8 s) |
| 7 | 32 / 31 | feasible / infeasible | 0.0 s / 0.0 s | 0.0 s / 0.0 s | SAT 496 055 (11.9 s) / **no result in 9 min** |
| 8 | 64 | feasible (incumbent) | 0.0 s | 0.1 s | **no result in 7 min** |

Witnesses at `n = 6, 7, 8` from both MILP solvers: `VALID`, zero deficient
words. The reproduced incumbent `C0 ∪ (C0 + e1)` verifies with coverage profile
`2^192 3^64`.

The LP relaxation is exactly `2·2^n/(n+1)`; at `n = 8`, HiGHS returns
`56.888888888888899` against `512/9 = 56.888888888888886`, i.e. the uniform
solution `x_c = 2/9` is optimal and the root gap to the incumbent is `7.11`.

---

## 3. The measured pilot at `n = 8`

Hardware: 10-core Apple Silicon, 16 GB, **shared with other sessions**
(1-minute load average 11–17 throughout). Single-threaded runs. Wall-clock
figures below are therefore soft by up to ~2×; node counts and conflict counts
are not, and the extrapolation is built on those.

### 3.1 Infeasibility ladder — the load-bearing measurement

Rungs 57–62, all measured on one host in one session (see
[`logs/pilot_2026-08-28.md`](logs/pilot_2026-08-28.md) §"Session 2"). Rungs
57–59 were re-measured there; every node count reproduced the earlier run
exactly.

| `M` | excess `9M-512` | HiGHS status | HiGHS nodes | HiGHS s | SCIP status | SCIP nodes | SCIP s |
|---:|---:|---|---:|---:|---|---:|---:|
| 57 | 1 | Infeasible | 1 | 0.0 | infeasible | 1 | 0.1 |
| 58 | 10 | Infeasible | 28 | 2.4 | infeasible | 15 | 0.9 |
| 59 | 19 | Infeasible | 1 219 | 11.0 | infeasible | 197 | 3.0 |
| 60 | 28 | **Infeasible** | **15 246** | **112.6** | **infeasible** | **34 542** | **290.1** |
| 61 | 37 | *budget expired* | >3 181 569 | 21 600 | *budget expired* | >3 424 374 | 21 600 |
| 62 | 46 | *budget expired* | >3 659 704 | 21 600 | *budget expired* | >3 954 015 | 21 600 |
| 63 | 55 | not started | — | — | not started | — | — |

Two independently implemented branch-and-bound codes agree at every rung that
closed. **Rung 60 is confirmed by both.** Rungs 61 and 62 expired at 6 h in
both solvers without closing and without finding a witness; those rows are
lower bounds, not results.

**The `≥143×/rung` reading in the previous revision of this table was a
contention artifact and is withdrawn.** It rested on HiGHS taking 1312.2 s at
rung 60; the identical search — same 15 246 nodes — takes 112.6 s on an
uncontended core. Seconds per node are close to flat across the measured range:

| | rung 59 | rung 60 | rung 61 | rung 62 |
|---|---:|---:|---:|---:|
| HiGHS s/node | 0.0090 | 0.0074 | 0.0068 | 0.0059 |
| SCIP s/node | 0.0152 | 0.0084 | 0.0063 | 0.0055 |

So per-node cost is *not* the thing that is exploding, and node count converts
to wall-clock reliably. Node growth is:

| | 57→58 | 58→59 | 59→60 | 60→61 |
|---|---:|---:|---:|---:|
| HiGHS | 28× | 43.5× | 12.5× | **>208.7×** |
| SCIP | 15× | 13.1× | **175.3×** | >99.1× |

The rung-61 entries are lower bounds (both trees were cut off mid-search). The
two solvers put the blow-up at *different* rungs — SCIP at 60, HiGHS at 61 — so
no single per-rung node ratio is supported by both. What both establish is that
the ratio is not constant and is far above the 13–30× that rungs 57–59 alone
suggested.

**Rung 62's node count says nothing about rung 62's difficulty.** Rungs 61 and
62 were both truncated at the same 6 h with similar per-node cost, so their node
counts are necessarily similar (3.2M vs 3.7M). Reading that near-equality as
"rung 62 is barely harder than rung 61" would be a mistake.

### 3.2 What does not work, measured

- **CDCL on the direct CNF is the wrong tool.** With a totalizer cardinality
  constraint and sound symmetry breaking (`0 ∈ C`, weight-1 codewords a prefix),
  CaDiCaL did not close `n = 7, M = 31` in 9 minutes — an instance that is
  *infeasible by the sphere bound alone* (`8·31 = 248 < 512`). It did not close
  `n = 8, M = 57` (1 unit of excess) in 7 minutes. MILP does both in under
  2 seconds. Counting arguments live naturally in the LP relaxation and
  painfully in resolution; that gap is the whole story.
- **Prescribed automorphisms find nothing below 64 — and this is now
  exhaustive over the cyclic stratum.** Sweeping cyclic `G = <(π, t)> ≤
  Aut(Q_8)` — cycle types of `S_8` × translation classes modulo the image of
  `1 + π` — gives **746** `(π, t)` classes. All but one are now settled:

  | outcome | classes |
  |---|---:|
  | orbit-ILP optimum is exactly 64 | 439 |
  | infeasible at `<= 64` | 76 |
  | infeasible at `<= 63` (re-solved after timing out at 20 s) | 227 |
  | infeasible at `<= 63` (excluded by the orbit-count filter, solved separately) | 3 |
  | **not settled:** identity, `t = 0`, 256 orbits — the unrestricted problem | 1 |

  **745 of 746 cyclic classes admit no `G`-invariant double covering of size
  `<= 63`**, and no witness below 64 was found anywhere in the sweep. The single
  exception is the identity at `t = 0`, which is not a symmetry restriction at
  all — it *is* the rung-63 question.

  This corrects the earlier claim in two ways. The sweep as originally written
  gave each orbit-ILP 20 s and **silently discarded every non-optimal
  outcome**, conflating a genuine `Infeasible` with a mere timeout; 227 of 742
  instances (31%) were in fact undecided, and they were the largest-orbit,
  *least* symmetric ones — exactly where a small code would hide. Separately,
  the `8 <= K <= 140` orbit filter excluded 4 classes without saying so. Both
  holes are closed (`prescribed_followup.py`, `prescribed_filter_audit.py`,
  `prescribed_excluded.py`).

  So a `<= 63` witness, if one exists, has **trivial cyclic automorphism group**.
  Non-cyclic subgroups remain unswept.
- ~~**Our tabu implementation is not competitive.**~~ **RETRACTED 2026-09-01.**
  The original text read: *"It reproduces `n = 6` and `n = 7` (cost 0 within
  seconds), but at `n = 8, M = 64` — where a solution is known to exist — it
  stalls at cost 11 after 2 minutes. Matching Östergård's 1995 tabu search needs
  a C implementation with incremental cost updates."*

  The stall was **a bug, not a language or performance limit.** The tabu list
  was inert: a word was marked tabu at the moment it was *removed* from the
  code, but the tabu test ran only over words currently *in* the code, so the
  mark could never fire and nothing prevented re-adding the word just dropped.
  The search was a random walk wearing a tabu costume. With the mark moved to
  where it belongs — forbidding *re-addition* of a recently removed word — plus
  incremental cost updates and greedy choice at both ends of the swap, the same
  Python finds `n = 8, M = 64` in **461 iterations / 12.8 s**, and the full
  `n = 4..8` gate passes. No C rewrite was needed.

  This is a caution about the estimate's method, not just about one line: the
  "needs a C implementation" conclusion was inferred from a stall without first
  auditing the search for correctness.

### 3.3 Proof-object sizes, measured

DRAT proofs emitted by CaDiCaL for the genuine (non-sphere-bound) refutations:

| instance | conflicts | proof lines | proof bytes |
|---|---:|---:|---:|
| `n=5, M=11` | 636 | 713 | 13.7 kB |
| `n=6, M=19` | 67 423 | 147 870 | 6.33 MB |

Ratio ≈ **462× in bytes per unit of `n`**. Naively extrapolated, a DRAT proof of
a genuine `n = 8` refutation is `10^2`–`10^3` GB. This is the number that
decides the certification architecture (§5).

---

## 4. Why the obvious routes are dead

| Route | Why not |
|---|---|
| enumerate subsets | `C(256,59) = 6.18e58`; `C(256,63) = 6.32e60` |
| enumerate up to symmetry | `\|Aut(Q_8)\| = 2^8 · 8! = 10 321 920`, so `C(256,59)/\|Aut\| ≈ 6.0e51`. Dividing by ten million does nothing to `10^58` |
| pure CDCL | §3.2 — loses to MILP by >100× on instances both can do |
| LP bound | `512/9 = 56.89`; every unit of dual bound past `57` comes from cuts and branching |

What *is* exploitable is the excess `E(M) = 9M − 512`. At `M = 59` only 19 of
256 words may be covered more than twice; a hypothetical 59-word code is a
near-perfect double covering. That is exactly why rung 59 fell in seconds and
rung 63 (excess 55) is the hard one.

---

## 5. The one pilot outcome that would be new — and what it cost to certify

*Revised 2026-08-29: the certification costs below are measured, not estimated.*

**Both solvers report `M = 59` infeasible — and now `M = 60` as well.** The
published lower bound is `59`, so if these are correct then `K(8,1,2) >= 61` and
the `n = 8` row of the 1993 table moves for the first time since 2020, by two
rungs rather than one.

Rung 60 is the stronger of the two readings in one respect and the weaker in
another: it is a bigger increment, but it rests on a search two orders of
magnitude larger (15 246 / 34 542 nodes against 1 219 / 197), so there is
correspondingly more floating-point arithmetic to be wrong. Certification cost
scales with it.

**We are not claiming it.** Two floating-point branch-and-bound codes agreeing
is evidence, not a certificate — precisely the failure mode `AGENTS.md` §1 was
written about.

The rest of this section used to be an *estimate* of what closing that gap
would cost. **It has been built.** The estimated table is replaced by §5.1–§5.6
below, which are measurements; the estimate's own numbers are kept in §5.5 so
the forecast can be scored.

---

## 5.1 What now exists

[`CERTIFICATION.md`](CERTIFICATION.md) is the full build-and-recheck
instruction; [`certs/MANIFEST.md`](certs/MANIFEST.md) is the list of certified
statements; [`logs/certification_2026-08-29.md`](logs/certification_2026-08-29.md)
is the raw session record.

```
pb_encode.py   the instance, in OPB                      (new)
RoundingSat    a cutting-planes refutation, logged as a VeriPB v2.0 derivation
VeriPB 3.0.2   replays the derivation and accepts or rejects it
recheck.py     re-derives the instance from the definition of K(n,1,2),
               re-hashes both artifacts, re-runs VeriPB, and requires VeriPB
               to REJECT the same proof against a deliberately weaker instance
```

The proof is produced by one program and checked by a different program by
different authors, so a `VERIFIED` line does not rest on RoundingSat being
correct. `pb_audit.py` closes the encoding gap by *executing* `milp_model.py`
against a recording stand-in for `highspy.Highs` and comparing the rows HiGHS
would actually receive to a fresh parse of the `.opb` — 54 checks, all passing,
covering every instance the certificates use.

## 5.2 The known-answer gate — passed, and in a stronger form than required

`AGENTS.md` §1 asks for the published cases first. The `--opt` form certifies
the published **values**, not merely the lower bounds: the solver proves
matching bounds on `min |C|` and VeriPB reports `VERIFIED BOUNDS a <= obj <= b`.

| statement | conflicts | solve | proof (raw / gz) | VeriPB 3.0.2 | verdict |
|---|---:|---:|---|---:|---|
| `K(6,1,2) = 20` | 8 670 | 2.37 s | 20.1 MB / 3.5 MB | 0.25 s | VERIFIED |
| `K(7,1,2) = 32` | 1 | 0.02 s | 1 793 B / 473 B | 0.00 s | VERIFIED |
| `K(6,1,2) > 19` | 53 | 0.04 s | 503 kB / 47 kB | 0.01 s | VERIFIED |
| `K(7,1,2) > 31` | 1 | 0.01 s | 529 B / 173 B | 0.00 s | VERIFIED |

`K(6,1,2) = 20` is the load-bearing one: `n = 6` is the smallest case where the
lower bound is *not* the sphere bound (`7·19 = 133 >= 128`, so counting alone
permits 19), so it is the smallest instance that exercises the machinery rather
than a one-line argument. Both `n = 7` rows are one-line sphere-bound
arguments — `8·31 = 248 < 512` — which is why they are 7-line proofs, and why
they are a weak gate on their own.

## 5.3 The `n = 8` ladder — measured

| rung | conflicts | solve | proof raw / gz | VeriPB 3.0.2 | verdict |
|---:|---:|---:|---|---:|---|
| 57 | 2 011 | 2.6 s | 27.77 MB / 4.37 MB | 0.36 s | VERIFIED |
| 58 | 5 447 | 558.4 s | 58.84 MB / 11.13 MB | 1.03 s | VERIFIED |

Both are **weaker than the published lower bound of 59** and neither is news.
See [`certs/MANIFEST.md`](certs/MANIFEST.md) for hashes, regeneration commands,
and where the ladder stopped. Three facts about the shape of this:

- **The PB solver's difficulty does not track the MILP's.** HiGHS closes
  `M = 58` in 2.4 s and 28 nodes and needs 1 219 nodes at `M = 59`;
  RoundingSat finds `M = 57` nearly free and `M = 58` 215× more expensive. The
  reason is in §"Forced structure" of the README: the coverage excess is 1 at
  `M = 57` and 10 at `M = 58`. **Excess, not `M`, is what the PB search feels**,
  and excess jumps by 9 per rung.
- **What explodes is cost per conflict, not conflict count.** Conflicts grew
  2.7× from rung 57 to rung 58 while wall-clock grew 215×, so per-conflict cost
  grew ~80×. That is the opposite of §3.1's floating-point finding, where
  seconds per *node* were close to flat across rungs 59–62. The two routes'
  scaling laws are different and neither can be read off the other.
- **The measured proof sizes are at the bottom of the estimate's range**, not
  the top: tens of MB raw, ~10 MB compressed, against the predicted "MB–GB".
  Checking is cheap and stays cheap — about 1 s for an 11 MB artifact.

## 5.4 The tuning result that moved the ladder, and the one that would have killed it

Two solver settings, neither of which changes what is proved, change whether
the route is viable at all. Both are recorded because a reproducer will hit
them.

| setting | `n = 6, M = 19` | `n = 8, M = 57` |
|---|---|---|
| `soplex=OFF` | **did not close in 10 min**; 212 MB of proof and still running | not attempted |
| `soplex=ON`, `--lp=1` (default) | 3 099 conflicts, 0.22 s, 4.3 MB | 25 632 conflicts, 63 s, 227 MB |
| `soplex=ON`, `--lp=-1` | 53 conflicts, 0.04 s, 503 kB | **2 011 conflicts, 2.6 s, 27.8 MB** |

`--lp` is the cap on how often RoundingSat may call the LP, as a ratio of
pivots to conflicts; `-1` removes it. Lifting it is worth 24× in time and 8× in
artifact size at rung 57. Building without SoPlex at all costs more than three
orders of magnitude and takes the route from "works" to "does not reach the
gate" — which is §3.2's finding from the other side: counting arguments live in
the LP relaxation, and a PB solver without an LP is on the resolution side of
that line.

## 5.5 Estimate versus measurement

| the 2026-08-28 estimate said | measured |
|---|---|
| VeriPB route: **2–5 days engineering** | **one session.** Almost none of it was the pipeline: the encoder, the two drivers, the audit and the re-checker are ~1 340 lines of standard-library Python, most of it docstring. The cost was macOS/arm64 build friction — nine distinct blockers, itemised in [`logs/certification_2026-08-29.md`](logs/certification_2026-08-29.md) — plus the two tuning discoveries in §5.4, either of which would have made the route look dead if missed. On a Linux box with distribution packages the build half is an afternoon. |
| VeriPB route: proof **MB–GB, not TB** | **correct, at the optimistic end** — see §5.3 |
| DRAT + `drat-trim`: **rejected**, `10^2`–`10^3` GB | **still rejected**, and nothing measured here disturbs that |
| exact rational MILP: **1–3 days engineering** | the PyPI `pyscipopt` wheel is confirmed useless for this — `enableExactSolving(True)` returns `SCIP was compiled without exact solve support`, and the build exposes no `exact/*` parameters at all. A source build of SCIP 10.0.0 with `-DEXACTSOLVE=ON -DLPSEXACT=spx` needs arm64 GMP **and** MPFR **and** Boost built first, and SoPlex's exact-rational template instantiations dominate the compile. See §5.6. |
| independent re-derivation by a third code base: **~0.5 day** | superseded by something cheaper and stronger — a second *checker* (VeriPB 2.3.0, Python/C++, independent implementation of the same format) over the same artifacts, at zero engineering cost beyond its build |

**The recommendation stands and is now measured, not argued.** Cutting planes
is the proof system these constraints live in.

## 5.6 The second route works, and it is the faster one

Route 2 — exact-rational SCIP 10 emitting a VIPR certificate, completed by
`viprcomp` and checked by `viprchk` — is built, exercised end to end, and reads
**the same `.opb` file** as route 1. So the two routes certify one artifact
rather than two hopefully equal ones.

| rung | route 1 solve (RoundingSat + SoPlex) | route 2 solve (exact SCIP) |
|---:|---:|---:|
| `n=6, M=19` | 0.04 s | 0.42 s |
| `n=8, M=57` | 2.6 s | 0.37 s |
| `n=8, M=58` | 558.4 s | **6.30 s** |
| `n=8, M=59` | not closed in ~50 min at either LP setting | **2 394 s, closed** |

**This inverts the recommendation.** §5.5 above scores "recommended: the VeriPB
route" as vindicated on *proof size and checking cost*, and it is. But on
*solving* cost the exact MILP is 89× faster at rung 58 and pulling away, which
is what the pilot's own floating-point numbers implied all along: HiGHS closes
rung 58 in 28 nodes, and exact SCIP closes it in 175 — a factor of six for
exactness, against the PB solver's factor of hundreds. The right reading is
that the two routes are complementary rather than ranked:

| | route 1 (PB + VeriPB) | route 2 (exact MILP + VIPR) |
|---|---|---|
| solve, rung 58 | 558 s | 6.3 s |
| artifact, rung 58 | 58.8 MB raw / 11.1 MB gz | 88.7 MB raw / 34.0 MB gz |
| checking, rung 58 | 1.0 s | 3.6 s |
| second checker available | yes (VeriPB 2.3.0) | not attempted |
| tooling friction | high (see the log) | higher (three tools, see below) |

**Both routes independently certify `K(8,1,2) > 57` and `K(8,1,2) > 58`.**
Neither is a new bound; both are weaker than the published 59.

**Route 2 alone reached `M = 59`**, where `viprchk` accepted the completed
exact-rational certificate. That is one rung past the published lower bound and
it is *not claimed here*: it has one route, one checker, and a 6.47 GB artifact
that is not in the repository. `certs/MANIFEST.md` states the caveats at
length. Its measured cost is the number that matters for §6:

| stage | wall |
|---|---:|
| exact SCIP solve | 2 394 s |
| `viprcomp` | 710 s |
| `viprchk` | 1 665 s (peak RSS 6.75 GB) |
| **total, one rung** | **~79 min** |

Floating-point SCIP does the same instance in 3.0 s and 197 nodes (§3.1), so
**the exactness penalty is ~800×**, not the 10–100× this section estimated. The
certificate is 6.47 GB completed, against the "MB–GB" the VeriPB route was
predicted to need and did need. Certification is not free and its cost is
growing faster than the floating-point search it certifies — which is the
single most important correction this session makes to §6.

**Rung 60 is not reachable on this host, and what stops it is the artifact, not
the clock.** Route 2's cost is now known at three rungs — 0.37 s / 2.55 MB at
57, 6.30 s / 88.68 MB at 58, 2 394 s / 6 474 MB at 59 — i.e. 17.0× then 380× in
solve time and 34.8× then 73.0× in certificate size. Projecting rung 60 with
the *smaller* of each pair gives ~11 h of exact solving and a ~230 GB completed
certificate; with the `58 -> 59` pair, ~11 days and ~470 GB. `viprchk`'s peak
RSS tracked certificate size at 1.04× on rung 59, so the memory requirement
projects with the size. Against 16 GB of RAM and 20 GB of free disk, rung 60 is
over budget by more than an order of magnitude on two independent resources.
The corollary for §6 is that **the ladder's binding constraint has switched
from CPU-hours to bytes**, and the fix is not more patience: it is a host with
hundreds of GB of RAM and disk, a checker that streams instead of materialising
the derivation, or symmetry reduction applied *before* certification.

Three route-2 costs the estimate did not anticipate, all measured:

- the PyPI `pyscipopt` wheel cannot do exact solving at all
  (`enableExactSolving(True)` -> `SCIP was compiled without exact solve
  support`; no `exact/*` parameters exist in that build);
- the **archived** `ambros-gleixner/VIPR` checker predates the VIPR 1.1 format
  SCIP 10 writes and rejects valid certificates with a syntax error — the
  maintained `scipopt/vipr` is required;
- SCIP's certificates are **incomplete by design**, so `viprcomp` is a
  mandatory third stage, and it needs oneTBB built for arm64. Neither
  `separating/maxrounds 0` nor `exact/safedbmethod e` avoids this.

## 5.7 What is still trusted

Certification moves trust rather than removing it. What a `VERIFIED` line still
rests on: **the checker's correctness** — VeriPB for route 1, reduced but not
eliminated by a second independent implementation; `viprchk` for route 2, with
no second implementation attempted; **the encoding** saying what the English
says, which `pb_audit.py` and `recheck.py` attack from three directions but
which bottoms out in a human reading twelve lines; **the compilers and
libraries**; and **the machine**.

What it no longer rests on: HiGHS, floating-point arithmetic, RoundingSat's own
search, and — for route 1 — SCIP. Note that route 2 does trust SCIP's
*certificate emission*, though not its arithmetic or its search: a bug that made
SCIP write a certificate for a different problem than it solved would not be
caught by `viprchk`. Route 1 does not have that exposure, and this is a reason
to keep both.

---

## 6. Cost model

Unit: one core-hour. Planning price **$0.05/core-hour** (spot general-purpose
cloud); on-demand is roughly 2×. All figures single-threaded — every rung and
every prescribed-group instance is an independent job, so parallel efficiency is
~1 up to the number of jobs.

### 6.1 Path L — the infeasibility ladder

The previous revision declined to price rungs 61–63: rung 60 was open, only
three rungs had closed, and all three priced columns looked refuted. Rung 60 has
now closed in both solvers and rungs 61–62 have run 6 h each without closing.
That is a fourth measured rung plus two lower bounds, and it is enough to price
the ladder — and, more usefully, to discriminate between the three columns.

**The disambiguation the previous revision was waiting for has resolved the bad
way.** It flagged two opposite readings of a slow rung 60: either per-node cost
was climbing steeply, or rung 60 was *feasible* and the solvers were hunting a
witness. Neither held. Rung 60 is **infeasible** in both solvers, so the ladder
does not collapse; and per-node cost is **flat** (§3.1), so the slowness was
neither of the proposed causes — it was host contention plus genuine node
growth.

### Which priced column survives

Scoring the three columns against what is now measured. The anchor is rung 60's
measured time; the test is rung 61, which ran 6 h in both solvers without
closing.

| column | predicts rung 60 | measured rung 60 | predicts rung 61 | measured rung 61 | verdict |
|---|---|---|---|---|---|
| 13×/rung | 40 s | 112.6 s / 290.1 s | 9 min | **>6 h, open** | **refuted** |
| 30×/rung | 90 s | 112.6 s / 290.1 s | 45 min | **>6 h, open** | **refuted** |
| 100×/rung | 5 min | **290.1 s = 4.8 min (SCIP)** | 8 h | >6 h, open — consistent | **survives** |

**The 100×/rung column is the only survivor.** It is now supported by two
independent observations and contradicted by none: SCIP closed rung 60 in
4.8 min against its predicted 5 min, and rung 61 remains open at 6 h against a
predicted 8 h. The 13× and 30× columns are refuted outright by rung 61's expiry
— both predicted it would close inside an hour.

One caveat on the anchor. Anchoring 100×/rung on *HiGHS*'s rung-60 time
(112.6 s) predicts rung 61 at 3.1 h, which rung 61's 6 h expiry already refutes.
The surviving parameterisation is 100×/rung **anchored on SCIP's rung-60 time**,
which is also the slower and therefore conservative anchor.

### The projection

| rung | projected single-core time | basis |
|---:|---|---|
| 59 | **3.0 s** | measured |
| 60 | **290 s** | measured (SCIP; HiGHS 113 s) |
| 61 | ~8 h | 100× rung 60; **measured floor >6 h** |
| 62 | ~34 days | 100× rung 61; **measured floor >6 h** |
| 63 | ~9.2 years | 100× rung 62 |
| **ladder total** | **~9.3 core-years** | dominated entirely by rung 63 |
| **cost at $0.05/core-h** | **~$4 100** | ~$8 200 on-demand |

Rung 63 is ~99% of the bill, which is the same shape §1 predicted: the last rung
below the true value dominates. Rungs 61 and 62 together are ~34 days, about
$40 — cheap enough to be worth finishing on their own.

**What would move this.** The projection rests on a per-rung ratio that the two
solvers do not agree on (§3.1): SCIP's node count jumps 175× at rung 60, HiGHS's
jumps >209× at rung 61. A single closed reading at rung 61 would replace the
weakest link here — it is the highest-value next measurement, and at ~8 h it is
affordable. Until then the 100× column is the best-supported of three, not a
law.

**This prices compute, not a certificate.** Everything above is floating-point
branch-and-bound. §5's certification cost sits on top of it, and no bound in
this table is claimed as a result.

### 6.2 Path U — a witness at `<= 63`

| Attack | Cost | Status |
|---|---|---|
| prescribed automorphisms, all cyclic subgroups | **~6.4 core-hours, spent** (sweep 5792 s + follow-up 16 610 s + excluded 538 s) | **done, negative and exhaustive**: 745/746 classes admit nothing `<= 63` (§3.2) |
| prescribed automorphisms, non-cyclic subgroups of order 4–32 | 2–20 core-hours | not started — now the only unswept symmetry route |
| MILP feasibility at `M = 63` with a long budget | 12–200 core-hours | not started; rungs 61–62 expired at 6 h each without a witness |
| tabu search, C implementation, `10^9` moves × many restarts | ~~1–2 days engineering~~ + 100–1 000 core-hours | superseded — the Python search now passes the `n = 8` gate (§3.2, retraction); a C port buys throughput only |

If path L reaches rung 63 first and reports infeasible, path U is moot and
`K(8,1,2) = 64`.

### 6.3 Certification

| Item | Engineering | Compute |
|---|---:|---:|
| exact/VeriPB pipeline (§5), built once, reused for every rung | **measured: ~1 session**, most of it build friction (11 blockers, see the log) | — |
| re-running the settled rungs under it | — | **measured: ~800× the floating-point solve** at rung 59, not the 10–100× estimated |
| standalone checker + certificate archive | **measured: included in the above** | negligible in time, **not in bytes** — see below |

The compute row is the one that was wrong, and it was wrong in the expensive
direction. It is also no longer the binding constraint: at rung 59 the
completed certificate is 6.47 GB and the checker's peak RSS 6.75 GB, and both
project to ~230 GB at rung 60 (§5.6). **Any plan for rungs 60+ must be costed
in storage and memory first and CPU-hours second.**

---

## 7. Bottom line

| Scenario | Wall-clock to a defensible answer | Compute | Cash |
|---|---|---:|---:|
| ~~**Rung 60 is feasible** — ladder collapses~~ | **eliminated**: rung 60 is infeasible in both solvers | — | — |
| **Ratio settles ~100×** — the live reading (§6.1) | **2–5 months** | ~9 core-years | $4k–$8k |
| **Worst** — ratio blows up above rung 61; needs isomorph-free enumeration with canonical augmentation, in the shape of Östergård–Blass, *On the size of optimal binary codes of length 9 and covering radius 1*, IEEE-IT **47** (2001) 2556–2557 | **6–18 months** | 10–100 core-years | $5k–$50k |

The cheap row is gone. Rung 60 closed as **infeasible** in both solvers, so the
ladder does not collapse and the surviving scenario is the middle one.

**Partial results are worth having on their own.** `K(8,1,2) >= 60`, certified,
is a publishable increment by itself and costs a rounding error against the
table — the pilot already has the floating-point version of it in 3 seconds, and
now the floating-point version of `>= 61` in 113 s / 290 s as well. That
asymmetry is the reason to run this target: the first two increments are nearly
free, and each further rung can be abandoned without wasting the last. Neither
is claimed; both need §5's certification leg first.

### Go / no-go

**GO**, staged, with kill criteria:

1. **Stage 1 (days).** Finish rungs 60–61 in floating point; build the exact
   certification leg; certify rung 59. *Kill if* rung 60 does not close within
   24 core-hours in either solver — that puts §7's worst row live and means the
   floating-point ladder is not the right architecture.
   **Status: rung 60 closed in 113 s / 290 s, far inside the kill criterion —
   Stage 1 survives.** Rung 61 has had 6 core-hours in each solver and has not
   closed; it is projected at ~8 h, so it is not yet near any kill line.
2. **Stage 2 (weeks).** Rungs 62–63 plus path U in parallel. *Kill if* rung 62
   does not close within 200 core-hours.
   **Status: rung 62 has spent 6 core-hours per solver of that 200 — not
   triggered, 194 core-hours of budget remain before it fires.**
3. **Stage 3 (months, only if Stage 2 closes).** Canonical-augmentation
   architecture for the final rung; this is the only stage that needs the cloud
   fleet rather than a laptop.

**Do not start Stage 3 without re-running the prior-art gate.** Six years of
silence on this row is not a guarantee, and a 2026 preprint would make the whole
budget moot.

---

## 8. What would falsify this estimate

- ~~Rung 60 taking > 24 core-hours.~~ **Not realised**: rung 60 closed in 113 s
  (HiGHS) / 290 s (SCIP). The earlier "≥143×/rung, all three columns refuted"
  reading was a host-contention artifact and is withdrawn — see §3.1. The 100×
  column is now the survivor, not a casualty.
- The surviving 100×/rung column failing at rung 61. It predicts ~8 h; rung 61
  has had 6 h in each solver without closing, which is consistent so far but not
  yet a confirmation. A closed rung 61 materially above ~8 h would refute the
  last standing column and put §7's worst row live.
- The two solvers continuing to disagree about where the node blow-up sits
  (SCIP at rung 60, HiGHS at rung 61). The projection assumes one ratio governs
  both; that assumption is currently unsupported at rung 61 in either direction.
- The exact-arithmetic re-run costing ≫ 100× the floating-point run — plausible
  if the LP relaxations are numerically nasty; nothing measured yet says either
  way.
- A `<= 63` witness turning up, which invalidates every rung above it and
  *shortens* the project.
- `M = 59` failing to reproduce under exact arithmetic, which would mean two
  independent floating-point codes were both wrong, and would put the whole
  ladder back to zero.
