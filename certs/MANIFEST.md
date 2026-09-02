# Certificate manifest

**What is in this directory, what each artifact certifies, what checked it, and
what is still trusted.** Build instructions for every tool named here are in
[`../CERTIFICATION.md`](../CERTIFICATION.md). Re-check everything with

```bash
VERIPB=/path/to/veripb python3 ../recheck.py --certs .
```

which re-derives each instance from the definition of `K(n,1,2)`, re-hashes both
artifacts, re-runs VeriPB, and requires VeriPB to *reject* the same proof
against a deliberately weaker instance.

**No bound in this directory is claimed as a new result.** Every line below is a
statement that a named checker accepted on a named artifact, and nothing more.

Most entries are already-published facts or *weaker* than the published lower
bound of 59: `K(6,1,2) = 20`, `K(7,1,2) = 32`, `K(8,1,2) > 57`, `K(8,1,2) > 58`.
**One is not.** `viprchk` accepted an exact-rational certificate for
`K(8,1,2) > 59`, which is one rung past the published bound. That single line
is the reason the caveats attached to it are longer than the line itself: it
rests on one route, one checker, and a 6.47 GB artifact that is not in this
repository. Read [`M = 59`](#m--59--route-2-only-and-it-is-the-one-statement-here-that-is-not-already-known)
before repeating it anywhere.

What would have to happen before anything here could be *claimed* is in
[`../WORKLOAD_ESTIMATE_2026-08-28.md`](../WORKLOAD_ESTIMATE_2026-08-28.md) §5.

---

## What the artifacts are

| file | role |
|---|---|
| `inst_*.opb` | the instance, in OPB. This is the object everything else is about. |
| `proof_*.pbp.gz` | RoundingSat's cutting-planes derivation, in VeriPB proof format 2.0, gzipped. **VeriPB reads the `.gz` directly** — no decompression step, and the compressed file is the checkable artifact. |
| `cert_*.json` | one record per statement: the exact statement, tool versions, the command run, per-stage wall-clock, machine and load, and sizes + SHA-256 of both artifacts. |
| `ladder.log` | the run order and outcome of the session, verbatim. |

An `inst_*.opb` present without a matching `proof_*.pbp.gz` and `cert_*.json`
means the rung was attempted and did not finish. **The tables below are the
authority on what closed**, not the file listing.

## Tools

| role | tool | version / commit |
|---|---|---|
| prover | RoundingSat 2 + SoPlex 7.1.6 | `d4edbf7908a9bb951fd181940919e0f3ac7ab1ee` (2026-03-03) |
| checker | VeriPB | 3.0.2, `e4ffda3b7b68bf0ffb42bc14f4170836ba4656e2` (2026-08-26) |
| second checker | VeriPB | 2.3.0, `b0d55dc87b5aaf55b14747be564a8e9060c081f3`, branch `version2` |
| encoder | `../pb_encode.py` | in-repo; audited by `../pb_audit.py` |
| re-checker | `../recheck.py` | in-repo; imports nothing else in the directory |

Solver invocation for every certificate here: `--lp=-1` (no cap on LP calls)
and `--stream-gzip`. Neither changes what is proved; see `CERTIFICATION.md` §3
for why they change whether it is affordable.

Machine: Apple M1 Pro, 10 cores, 16 GB, arm64, macOS 26.6.1. **Shared with other
sessions**; 1-minute load average 10–17 throughout, so wall-clock is soft by up
to ~2.7×. Conflict counts, proof sizes and hashes are not soft.

**On the `tools.encoder` hash in the records.** Each record pins the SHA-256 of
the `pb_encode.py` that produced its instance. `pb_encode.py` received a
cosmetic edit (a clearer `intsize` computation and a docstring) after some
records were written, so those records name an earlier file. The instances are
byte-identical either way — checked by regenerating all six and comparing to
the recorded `instance.sha256`, all matching. This is informational in any
case: `recheck.py` never imports the encoder, and re-derives each instance from
the definition of `K(n,1,2)` itself.

---

## Certified statements

### Known-answer gate — the published cases, certified first

These are facts already in the literature. The `--opt` rows certify the
published **values**, not merely the lower bounds: the solver proves matching
bounds on `min |C|` and VeriPB reports `VERIFIED BOUNDS a <= obj <= b`.

| statement | record | conflicts | solve | proof raw / gz | VeriPB 3.0.2 | VeriPB 2.3.0 |
|---|---|---:|---:|---|---:|---|
| `K(6,1,2) = 20` | `cert_n6_opt.json` | 8 670 | 2.37 s | 20.13 MB / 3.54 MB | 0.25 s, `VERIFIED BOUNDS 20 <= obj <= 20` | 6.97 s, agrees |
| `K(7,1,2) = 32` | `cert_n7_opt.json` | 1 | 0.02 s | 1 793 B / 473 B | 0.00 s, `VERIFIED BOUNDS 32 <= obj <= 32` | 0.09 s, agrees |
| `K(6,1,2) > 19` | `cert_n6_M19.json` | 53 | 0.04 s | 503 242 B / 46 968 B | 0.01 s, `VERIFIED UNSATISFIABLE` | 0.25 s, agrees |
| `K(7,1,2) > 31` | `cert_n7_M31.json` | 1 | 0.01 s | 529 B / 173 B | 0.00 s, `VERIFIED UNSATISFIABLE` | 0.08 s, agrees |

`K(6,1,2) = 20` is the load-bearing gate. `n = 6` is the smallest case whose
lower bound is *not* the sphere bound — `7·19 = 133 >= 128`, so counting alone
permits 19 — which makes it the smallest instance that exercises the machinery
rather than a one-line argument. Seuranen's 2011 dissertation source
distribution contains this run, so it is independently established. The two
`n = 7` rows are one-line sphere-bound arguments (`8·31 = 248 < 512`), which is
why their proofs are 7 and 8 lines; on their own they would be a weak gate.

### `n = 8`

| statement | record | conflicts | solve | proof raw / gz | VeriPB 3.0.2 | VeriPB 2.3.0 |
|---|---|---:|---:|---|---:|---|
| `K(8,1,2) > 57` | `cert_n8_M57.json` | 2 011 | 2.60 s | 27.77 MB / 4.37 MB | 0.36 s, `VERIFIED UNSATISFIABLE` | 528 s wall / 32 s CPU, agrees |
| `K(8,1,2) > 58` | `cert_n8_M58.json` | 5 447 | 558.42 s | 58.84 MB / 11.13 MB | 1.03 s, `VERIFIED UNSATISFIABLE` | 476 s wall, agrees |

**Both are weaker than the published lower bound of 59 and are not news.** They
are here because they are what the pipeline reached; the rung that would
*matter* is `M = 59`, and where that got to is in "Where this stopped" below.

The shape of the two rows is itself the interesting measurement. Conflicts grew
2.7× from `M = 57` to `M = 58`, but wall-clock grew **215×** — so the cost per
conflict grew ~80×, not the search. With `--lp=-1` every conflict may call the
LP, and it is the LP work per conflict that explodes. This is the opposite of
what the floating-point pilot saw (§3.1 of the estimate: seconds per *node*
close to flat across rungs 59–62), and it means the PB route's scaling cannot
be read off the MILP route's.

It also does not track difficulty as `M` grows in the way the MILP does: HiGHS
closes `M = 58` in 2.4 s and 28 nodes but needs 1 219 nodes at `M = 59`, while
RoundingSat finds `M = 57` trivial and `M = 58` two orders of magnitude harder.
The README's excess table explains why — at `M = 57` the coverage excess is 1
and propagation is nearly forced; at `M = 58` it is 10.

#### The re-checker was itself tested against a bad certificate

A copy of `cert_n6_M19` with **one bit flipped** inside the derivation was run
through `recheck.py`. Two independent steps caught it: the recorded SHA-256 no
longer matched, *and* VeriPB rejected the proof on its own merits. So the
verdict does not depend on the hash bookkeeping — a corrupted derivation fails
the mathematics too. The run reported `FAILED` and exited non-zero, which is
what a re-checker has to do to be worth running.

#### A caution worth recording

VeriPB 2.3.0 initially *rejected* the `M = 57` proof with
`Expected literal` at line 99987. That was not a bad proof: the ladder had been
restarted and had rewritten `proof_n8_M57.pbp.gz` while the checker was reading
it. An artifact replaced under a reader looks exactly like a corrupt proof.
Re-run against the stable artifact, the same checker returned
`s VERIFIED UNSATISFIABLE`. This is why every record carries a SHA-256 and why
`recheck.py` verifies it before running the checker.

### `M = 59` — route 2 only, and it is the one statement here that is not already known

`viprchk` reported **`Successfully verified infeasibility.`** on the completed
exact-rational certificate for the `n = 8, M = 59` instance. Trimmed checker
output: [`../logs/viprchk_n8_M59.log`](../logs/viprchk_n8_M59.log).

**What that certifies, exactly:** the OPB instance `inst_n8_M59.opb` — 256 0/1
variables, 256 ball constraints of degree 2, one row `sum_v x_v <= 59` — has no
0/1 solution. That is `K(8,1,2) > 59`.

**It is not claimed as a result, and it is weaker evidence than the rungs below
it.** Read the caveats before quoting the line:

| | |
|---|---|
| **one route, one checker** | rungs 57 and 58 are certified twice over, by two pipelines with nothing in common. Rung 59 has only route 2, and `viprchk` has no second implementation here. Route 1 did not reach it. |
| **it trusts SCIP's certificate emission** | not SCIP's arithmetic and not its search — `viprchk` replays those in exact rationals — but a bug that made SCIP write a certificate for a *different* problem than it solved would not be caught. Route 1 is not exposed to that, and route 1 does not cover this rung. |
| **the artifact is not committed** | 6.47 GB. Size, hash and the regeneration command are below. Nobody can re-check this from the repository alone. |
| **the driver did not produce a record** | the session harness killed `certify_exact.py`'s wrapper after `viprcomp` finished, so there is no `cert_n8_M59.json`. The stage timings below come from artifact timestamps and the checker was re-run standalone with full output captured. A hand-written JSON record would have implied a provenance the run does not have. |

Measured, on the shared host:

| stage | wall | product |
|---|---:|---|
| exact SCIP solve | 2 394 s (39.9 min) | `cert_n8_M59.vipr`, 3 594 514 707 B, sha256 `621fff24e30169057ca0a3f18561872ebba0bc5693fd55fd178832e81a50dbab` |
| `viprcomp` | 710 s (11.8 min) | `cert_n8_M59_complete.vipr`, 6 474 101 470 B, sha256 `2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf` |
| `viprchk` | 1 665 s wall / 1 270 s CPU, peak RSS 6.75 GB | `Successfully verified infeasibility.`, 688 858 derivations |

Total ≈ 79 minutes for one rung, against floating-point SCIP's 3.0 s and 197
nodes for the same instance (§3.1). **The exactness penalty here is ~800×**, not
the 10–100× §5 estimated.

Regenerate and re-check:

```bash
export SCIPEXACT=.../scipoptsuite-10.0.0/build/bin/scip
export VIPRCOMP=.../vipr2/code/build/viprcomp
export VIPRCHK=.../vipr2/code/build/viprchk
python3 certify_exact.py --n 8 --M 59 --outdir certs_exact --budget 14400 \
        -o certs_exact/cert_n8_M59.json      # ~80 min, needs ~11 GB free disk
```

Budget generously: the two intermediate files together peak above 10 GB, and
SCIP's working `.vipr_der` grows at roughly 100 MB/min during the solve.

### Where this stopped

| rung | route 1 (PB + VeriPB) | route 2 (exact MILP + VIPR) |
|---|---|---|
| `M = 57` | certified, both checkers | certified |
| `M = 58` | certified, both checkers | certified |
| `M = 59` | **not closed** — see below | **checker accepted**, single route, artifact not committed (above) |
| `M = 60` | not reached | not reached |

**Route 1 did not close `M = 59`**, so the rung has no second, independent
confirmation. Two runs, both terminated by the session's own wrapper rather
than by a solver budget:

| configuration | ran for | state when stopped |
|---|---|---|
| `--lp=-1` (the setting every committed certificate uses) | ~50 min | 63 MB of compressed proof, still running |
| `--lp=1` (RoundingSat's default) | ~50 min | 187 254 conflicts, still running |

Neither is a measurement of how long rung 59 *takes* — both were cut off — but
together they put a floor under it of roughly an hour at either setting, on a
contended host, against 558 s for rung 58. The partial proofs were discarded;
`inst_n8_M59.opb` is committed so the attempt is reproducible.

**`M = 60` was not attempted by either route, and the reason is measured, not
guessed.** Route 2's cost per rung is now known at three points:

| rung | exact SCIP solve | completed certificate | factor vs. previous rung |
|---|---:|---:|---|
| `M = 57` | 0.37 s | 2.55 MB | — |
| `M = 58` | 6.30 s | 88.68 MB | 17.0× solve, 34.8× size |
| `M = 59` | 2 394 s | 6 474 MB | 380× solve, 73.0× size |

Extrapolating `M = 60` with the **smaller** of the two observed factors — the
optimistic end — gives roughly 11 h of exact solving and a ~230 GB completed
certificate; with the `58 -> 59` factors it is ~11 days and ~470 GB. The
checker's footprint scales with the certificate: `viprchk` peaked at 6.75 GB of
RSS on the 6.47 GB `M = 59` certificate, about 1.04× its size, so a 230 GB
certificate implies ~230 GB of RAM.

This machine has 16 GB of RAM and had 20 GB of free disk at the end of the run.
The `M = 59` check already peaked at 6.75 GB — 42% of physical memory — so
`M = 60` is out of reach here by more than an order of magnitude on two
independent resources, and the blocker is the artifact, not the solving time. Route 1 is no help: it did not close `M = 59` in ~50 min at either LP
setting. Closing rung 60 needs a host with hundreds of GB of both, or a
certificate format that does not materialise the whole derivation — not more
patience on this one.

Nothing here is claimed as a result.

### Route 2 — exact-rational MILP, in `../certs_exact/`

**Working end to end, and much faster than route 1.** Exact-rational SCIP 10
solves the same `.opb`, writes a VIPR certificate, `viprcomp` completes it, and
`viprchk` verifies it in exact rational arithmetic. Re-check with

```bash
VIPRCHK=/path/to/viprchk python3 ../recheck.py --certs ../certs_exact
```

| statement | record | SCIP nodes | scip | viprcomp | viprchk | complete cert raw / gz |
|---|---|---:|---:|---:|---:|---|
| `K(6,1,2) > 19` | `cert_n6_M19.json` | 17 | 0.42 s | 0.21 s | 0.51 s | 13.43 MB / 4.67 MB |
| `K(7,1,2) > 31` | `cert_n7_M31.json` | 1 | 0.03 s | 0.02 s | 0.00 s | 18 537 B / 4 494 B |
| `K(8,1,2) > 57` | `cert_n8_M57.json` | 1 | 0.37 s | 0.07 s | 0.06 s | 2.55 MB / 468 kB |
| `K(8,1,2) > 58` | `cert_n8_M58.json` | 175 | 6.30 s | 1.24 s | 3.60 s | 88.68 MB / 34.00 MB |

**Two independent routes now certify `K(8,1,2) > 57` and `K(8,1,2) > 58`** —
different prover, different proof system, different checker, *the same
instance file*. That is a materially stronger position than either alone, and
it is still not a claim: both statements are weaker than the published 59.

The cost comparison is the useful part:

| rung | route 1 solve (RoundingSat) | route 2 solve (exact SCIP) |
|---:|---:|---:|
| 57 | 2.6 s | 0.37 s |
| 58 | 558.4 s | 6.30 s |
| 59 | did not close in ~50 min at either LP setting | 2 394 s |

Route 2 is **89× faster at rung 58** and its advantage grows with the rung.
That inverts the estimate's §5 recommendation, which put the PB route first;
see `../WORKLOAD_ESTIMATE_2026-08-28.md` §5.6. The trade is artifact size:
route 2's completed certificate for rung 58 is 88.68 MB raw against route 1's
58.84 MB, and it does not compress as well.

#### Not committed: `cert_n8_M58_complete.vipr.gz`

34 MB against a 66 MB repository, so it is `.gitignore`d rather than stored.
Everything needed to reproduce and verify it byte for byte:

| | |
|---|---|
| gzipped | 34 004 647 B, sha256 `4f08ed14e6d7a98961fbfcc0b43d400f48636491d5c1323bddb8e9f4315591e4` |
| expanded | 88 680 439 B, sha256 `166c25685dacc4fc1ad5af88fc5aaa8bf0ef8d88d71fdb41d824512837faaecb` |

```bash
export SCIPEXACT=.../scipoptsuite-10.0.0/build/bin/scip
export VIPRCOMP=.../vipr2/code/build/viprcomp
export VIPRCHK=.../vipr2/code/build/viprchk
python3 certify_exact.py --n 8 --M 58 --outdir certs_exact \
        --budget 7200 --compress -o certs_exact/cert_n8_M58.json
```

Drop the result in `../certs_exact/` and `recheck.py` will verify it. Until
then that one record re-checks as `INCOMPLETE (certificate not on disk)`, which
is the honest state and not a failure. The corresponding *route 1* proof of the
same statement **is** committed, so `K(8,1,2) > 58` remains checkable from this
repository alone.

#### Three things route 2 cost that the estimate did not anticipate

1. **The PyPI `pyscipopt` wheel cannot do this**, measured rather than assumed:
   `enableExactSolving(True)` returns `SCIP was compiled without exact solve
   support`, and the build registers no `exact/*` parameters at all.
2. **The archived VIPR repository's checker is too old.** SCIP 10 writes VIPR
   1.1; `ambros-gleixner/VIPR`'s `viprchk` rejects it with `Syntax Error in
   AggrRow_193: Expecting } but read instead {`, which reads exactly like a
   corrupt certificate. The maintained `scipopt/vipr` is required.
3. **The certificate is incomplete by design and `viprcomp` is mandatory.**
   SCIP's aggregation rows carry `{ lin weak { 0 } ... }` reasons whose
   multipliers are reconstructed later by an exact LP solve. Neither
   `set separating maxrounds 0` nor `set exact safedbmethod e` avoids this;
   both were tried. `viprcomp` in turn needs oneTBB built for arm64.

---

## What is still trusted

Certification moves trust; it does not remove it.

| still trusted | why it is not eliminated here |
|---|---|
| **VeriPB's correctness** | the checker is the last link. A second, independently implemented checker (VeriPB 2.3.0, Python + C++, versus 3.0.2 in Rust) is run over the same artifacts, which removes single-implementation risk but not the risk that both are wrong about the format. CakePB — formally verified in HOL4 — would reduce it further and was not attempted. |
| **The encoding** | `../pb_audit.py` executes `../milp_model.py` against a recording stand-in for `highspy.Highs` and compares the rows HiGHS would actually receive to a fresh parse of the `.opb`; `../recheck.py` independently re-derives the instance from the definition; the published 64-word incumbent and two deliberately broken codes are evaluated against the parsed constraints and cross-checked against `../verify.py`. That is three directions. It still bottoms out in a human reading twelve lines of `expected_constraints`. |
| **Compilers and libraries** | rustc 1.98.0, Apple clang, Boost 1.88.0, GMP 6.3.0, SoPlex 7.1.6. None is verified. |
| **The machine** | one host. The remedy is re-running elsewhere, which is what `../CERTIFICATION.md` exists for. |

**No longer trusted, and this is the point:** HiGHS, SCIP, floating-point
arithmetic, and RoundingSat's own search. A `VERIFIED` line would survive
RoundingSat being wrong.

---

## Where the large `M = 59` artifacts actually live (2026-08-29)

The two `M = 59` files total 9.4 GiB and are **not in this repository** and
**not on GitHub**. GitHub cannot host them: the in-repo file limit is 100 MB and
the release-asset limit is 2 GB per file, while `cert_n8_M59_complete.vipr`
is 6.47 GB and compresses only 2.51x (measured, gzip -6 on a 200 MB sample),
i.e. to ~2.6 GB. Splitting a certificate across release assets would trade a
checkable artifact for a fragile one.

They were moved off the boot volume on 2026-08-29 to:

```
<external-archive>/mcov_8_1_2/certs_exact/
```

**Verified before the originals were deleted**, against the SHA-256 values
recorded above:

```
OK   cert_n8_M59.vipr           621fff24e30169057ca0a3f18561872ebba0bc5693fd55fd178832e81a50dbab
OK   cert_n8_M59_complete.vipr  2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf
ALL SMALL FILES MATCH          (the other 19 files, hashed on both sides)
```

That volume is a single local disk, so this is **one copy, not a backup**. The
regeneration command in this manifest remains the authoritative recovery path
(~80 min, ~11 GB of free disk). If these artifacts are ever to be cited, the
right home is a Zenodo deposit with a DOI, not a local volume. They now have
one: DOI 10.5281/zenodo.22217672.
