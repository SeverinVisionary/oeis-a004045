# Certificate manifest -- prime-order symmetry orbit-ILPs

What is in this directory, what each artifact certifies, what checked it, and
what remains uncertified. Full narrative and the mandatory over-constraint
control are in [`../SYMMETRY_THEOREM.md`](../SYMMETRY_THEOREM.md); this file
is the index of artifacts.

**No bound on `K(8,1,2)` is claimed anywhere here.** Every line below is a
statement that a named checker accepted (or did not accept) a named artifact
about SYMMETRIC codes, and nothing more.

## Independence from `symmetry_prime.py`

`symcert_reps.py` re-derives the 28 prime-order conjugacy-class
representatives and their orbits from scratch and never imports
`symmetry_prime.py`. Its orbit counts agree with
[`logs/symmetry_prime_sweep_2026-08-30.log`](../logs/symmetry_prime_sweep_2026-08-30.log)
on all 28 classes -- run `python3 symcert_reps.py` to reproduce. `symcert_encode.py`
builds the OPB instance from that independent data.

## Tools

| role | tool | version / commit |
|---|---|---|
| route 1 prover | RoundingSat 2 + SoPlex 7.1.6 | `d4edbf7908a9bb951fd181940919e0f3ac7ab1ee` |
| route 1 checker | VeriPB | 3.0.2, `e4ffda3b7b68bf0ffb42bc14f4170836ba4656e2`, run with `-c` (forced checked deletion) |
| route 2 prover | SCIP | 11.0.0, source build, `-DEXACTSOLVE=ON -DLPSEXACT=spx`, SoPlex 7.1.6 built with GMP+MPFR+Boost |
| route 2 completion/checker | `viprcomp` / `viprchk` | `scipopt/vipr` `30f2951d1e90e47afa821bdd1b12b82246656c42` |
| route 2 binding check | `../vipr_bind.py` | in-repo; binds the VIPR certificate's own header to the committed `.opb` by variable name and constraint multiset, since `viprchk cert.vipr` never reads the `.opb` on its own |
| encoder | `../symcert_encode.py` + `../symcert_reps.py` | in-repo, independent of `symmetry_prime.py` |
| control | `../symcert_control.py` | in-repo; solves the `ub=64` control via `scipy.optimize.milp`, checks with `../verify.py` |

Machine (this session): Ubuntu 24.04, x86_64, 4 cores, 15 GB RAM, cloud
container. A second, independent session rebuilt the same route-2 toolchain
on a different host and reproduced `VERIFIED` for `p7_a1`, `p5_a1`, `p3_a2`,
`p3_a1`. (The per-session commits predate a history squash and are no longer
individually addressable; the artifacts themselves are committed here.)

## Certified: 4 of 28

| class | order | orbits | route | record | verbatim verdict |
|---|---:|---:|---|---|---|
| `p7_a1` | 7 | 40 | 1 | `cert_p7_a1_ub63.json` | `s VERIFIED UNSATISFIABLE` |
| `p5_a1` | 5 | 64 | 1 | `cert_p5_a1_ub63.json` | `s VERIFIED UNSATISFIABLE` |
| `p3_a2` | 3 | 96 | 2 | `cert_exact_p3_a2_ub63.json` | `Successfully verified infeasibility.`, binding `bound=true` |
| `p3_a1` | 3 | 128 | 2 | `cert_exact_p3_a1_ub63.json` | `Successfully verified infeasibility.`, binding `bound=true` |

`inst_p7_a1_ub63.opb` and `inst_p5_a1_ub63.opb` and their route-1 `.pbp`
proofs are committed directly (small). Route-2 VIPR certificates for `p3_a1`
and `p3_a2` are **not committed** -- they ran from hundreds of MB to
low-single-digit GB, over the 50 MB limit; sha256 and size of every stage are
in the `.json` records, and the exact command to regenerate each is in
`rec["solve"]["command"]` / `rec["complete"]["command"]` inside those files.

## Not certified: 24 of 28 (all order-2)

Every `p2_a*_b*_c*` class was attempted (route 2 for all; route 1 also, on
several, before it was abandoned for that route -- see
`../SYMMETRY_THEOREM.md`). None closed within 600-3600 s per class. Records
are all present as `cert_exact_p2_*_ub63.json` (or `cert_p2_*_ub63.json` for
the route-1 attempts), each stating honestly `"certified": false` and the
exact reason (`BUDGET EXPIRED`, a SCIP-reported time-limit interruption, or a
disk-safety abort) -- an `inst_*.opb` with no corresponding `VERIFIED` record
is exactly what "attempted, not closed" looks like here, not a missing run.

The three hardest of these (`p2_a1_b6_c0` 192 orbits, `p2_a2_b4_c0` 160
orbits, `p2_a3_b2_c0` 144 orbits) additionally have `ub=64` control records
under `../logs/control_inv64_*orbits_*.json`, each `verify.py`-`VALID` and
`g`-invariant -- the mandatory check that "not certified" here means
"genuinely hard," not "the encoding is broken."

### Solo, uncontended, 6h-budget follow-up on three classes (2026-08-31)

Prior order-2 attempts ran either at a 600 s budget, or three-at-a-time on a
shared machine, or both, so a "budget expired" record never distinguished
genuine hardness from contention noise. This session re-ran three classes
solo (nothing else on the machine), one at a time, at a 21 600 s (6 h)
budget: `p2_a0_b7_c1` (128 orbits), `p2_a4_b0_c0` (136 orbits, previously the
worst case at 795 279 nodes / 3623 s), and `p2_a1_b6_c0` (192 orbits,
previously given only 620 s).

**A real bug was found and fixed first.** `run_scip()` in
`../symcert_certify_exact.py` captured SCIP's stdout via `subprocess.PIPE`
and only ever read it after `p.wait()` succeeded. A Linux pipe has a fixed
64 KB kernel buffer; nothing in that loop drained it while polling, so once
SCIP's cumulative display output passed 64 KB the child blocked forever in
`write()` -- confirmed directly on the first `p2_a0_b7_c1` attempt via
`/proc/<pid>/stack` (`anon_pipe_write`) and 0% CPU for the SCIP process,
roughly 30-45 minutes in, certificate size frozen. Wall clock kept advancing
toward the external budget+grace kill with zero further search happening in
between, so any long run through the unpatched code understates real search
time and its node/time numbers cannot be trusted at face value. Fixed by
writing SCIP's stdout to a plain file instead; re-verified
against `p3_a2` (VERIFIED, binding bound, solve 136.8 s solo, consistent with
the previously recorded ~183 s solo figure) before re-running the three
classes from scratch.

With the fix in place, **all three runs ended the same way: the built-in
disk-safety valve in `run_scip` (certificate > 4000 MB) fired, not the time
budget or SCIP's own limit**:

| class | orbits | seconds | nodes at cutoff | cutoff reason |
|---|---:|---:|---:|---|
| `p2_a0_b7_c1` | 128 | 715.1 | 210 500 | disk-safety (4207 MB written) |
| `p2_a4_b0_c0` | 136 | 840.1 | 216 400 | disk-safety (4200 MB written) |
| `p2_a1_b6_c0` | 192 | 745.1 | 113 900 | disk-safety (4200 MB written) |

None of the three used more than 840 of the allotted 21 600 seconds, and the
dual bound stayed at 0 (gap infinite) throughout -- no useful bound was
established before the disk cap ended the run. So for these three classes
the original question (does 6 h solo beat a contended 600-3600 s budget?)
turns out to be moot: **disk, not time or contention, is what stops the
search.** Whether more time would help is genuinely still unanswered, since
none of the runs got anywhere near their time budget; answering it would
require deliberately raising `max_cert_mb` past 4000 (this machine had 30 GB
free and never dropped below 27 GB across all three runs, so there is
headroom to do that) -- a tradeoff against disk risk that was left to a
human decision rather than made unilaterally here. Records:
`cert_exact_p2_a0_b7_c1_ub63.json`, `cert_exact_p2_a4_b0_c0_ub63.json`,
`cert_exact_p2_a1_b6_c0_ub63.json`; solo run logs and PIDs under
`../logs_solo/`.

## What is still trusted

Certification moves trust; it does not remove it -- see
`../CERTIFICATION.md` §1 for the general list (VeriPB's correctness, the
encoding, compilers, the machine). Specific to this directory: `vipr_bind.py`
checks that the certificate's header describes our instance, but is itself
unverified 200-line Python, and `symcert_reps.py`'s orbit computation is
cross-checked against `symmetry_prime.py` only by agreement of derived
numbers, not by a third, independently-authored derivation.
