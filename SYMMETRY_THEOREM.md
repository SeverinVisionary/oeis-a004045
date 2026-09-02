# Every `<= 63` double covering of `Q_8` is asymmetric, and 64 is sharp

**Status: 4 of 28 classes machine-checked, 24 remain floating-point only.**
The 24 open classes have since been *narrowed* -- 20 of them collapse from an
inequality over three sizes to a single equality `= 62` with the weight split
pinned to one or two values (see "Narrowing what is left to certify"). None is
thereby closed: the count is still 4 of 28.
Every "Infeasible" in the sweep below is a floating-point HiGHS
branch-and-bound status, not a proof object, by itself. Independent
certification (`certs_symmetry/`, see "Certification status" below) has since
replayed 4 of the 28 -- the order-3, -5 and -7 classes -- as machine-checked
cutting-planes or exact-rational refutations, agreeing with every HiGHS
verdict it reached. The 24 order-2 classes are **not certified**: two
independent certification routes, given up to an hour per class, did not
close any of them, for reasons that look like a genuine property of the
problem rather than a tooling gap (see below). **No statement about
`K(8,1,2)` itself is made anywhere in this file** -- certification only
strengthens the symmetry claim, which is about symmetric codes.

## Statement

Let `K_sym(8,1,2) = min { |C| : C a double covering of Q_8, Aut(C) != 1 }`.

> **`K_sym(8,1,2) = 64`.** No double covering of `Q_8` with `|C| <= 63` admits a
> non-identity automorphism, and a 64-word one does.

Equivalently: any code witnessing `K(8,1,2) <= 63`, if one exists, is
**asymmetric**. That constrains where a better upper bound can live -- and it
explains why every prescribed-automorphism search in this directory came back
empty. Those searches were not underpowered; the object they looked for cannot
exist.

## Why 28 classes suffice (and 746 was never necessary)

If `Aut(C) != 1` then some non-identity `g` fixes `C`, and some power of `g` has
**prime order** and also fixes `C`. So it is enough to rule out invariance under
prime-order automorphisms. Conjugate elements give isomorphic orbit-ILPs, so one
representative per conjugacy class suffices.

`Aut(Q_8) = F_2^8 : S_8` is the hyperoctahedral group `B_8`; its classes are
indexed by signed cycle types (bipartitions of 8). A positive `L`-cycle has
order `L`, a negative `L`-cycle order `2L`, so the prime orders available are
`2, 3, 5, 7` and the prime-order classes are

| order | condition | count |
|---|---|---:|
| 2 | `2a + b + c = 8`, `a + c > 0` (a positive 2-cycles, b positive 1-cycles, c negative 1-cycles) | 24 |
| 3 | `3a + b = 8`, `a >= 1` | 2 |
| 5 | `5a + b = 8`, `a >= 1` | 1 |
| 7 | `7a + b = 8`, `a >= 1` | 1 |
| | | **28** |

This was **not assumed**. `symmetry_prime.py --selftest` checks the orders of
all 28 representatives and confirms they have 28 distinct signed cycle types;
separately, enumerating *all* bipartitions of 8 gives 185 total signed cycle
types (the known class count of `B_8`) of which exactly 28 have prime order,
with breakdown `{2: 24, 3: 2, 5: 1, 7: 1}`, and that set equals the set realised
by our representatives -- nothing missing, nothing extra.

## The sweep

One binary variable per orbit of `<g>` (an invariant code is a union of orbits),
coverage `>= 2` at every vertex, `sum |O| y_O <= 63`. All 28 came back
`Infeasible`. Full log:
[`logs/symmetry_prime_sweep_2026-08-30.log`](logs/symmetry_prime_sweep_2026-08-30.log).

Total 35 606 s of solver time. Cost is governed by orbit count, i.e. by how
*weak* the symmetry is -- the two worst are the ones closest to the unrestricted
256-variable problem:

| class | order | orbits | seconds |
|---|---:|---:|---:|
| `p2_a2_b4_c0` | 2 | 160 | 13 230 |
| `p2_a1_b6_c0` (bare transposition) | 2 | 192 | 12 088 |
| `p2_a3_b2_c0` | 2 | 144 | 2 115 |
| `p7_a1` (7-cycle) | 7 | 40 | 0.49 |

## Sharpness

`C = ker H` with `H`'s eight columns `00,01,01,10,10,11,11,11` is linear of
dimension 6, so `|C| = 64` and every translation by a codeword is an
automorphism. The syndrome multiplicities are `2,2,2,3`, so every word is
covered at least twice. `verify.py` (standard library only, shares no code with
any solver) accepts it:

```
{"n": 8, "mu": 2, "size": 64, "sphere_bound": 57, "excess": 64,
 "coverage_profile": {"2": 192, "3": 64}, "deficient_words": 0}
VALID
```

Witness: [`code64_linear_sharp.json`](code64_linear_sharp.json).

## Controls -- why "Infeasible" here means something

An over-constrained model returns `Infeasible` for free, which would make the
whole sweep worthless. So the same model was run at `ub = 64` on the two
**hardest** classes; both must be feasible, and are:

| class | orbits | `ub=64` | `g`-invariant | `verify.py` |
|---|---:|---|---|---|
| `p2_a1_b6_c0` | 192 | Feasible, 64 | yes | `VALID` |
| `p2_a2_b4_c0` | 160 | Feasible, 64 | yes | `VALID` |

Codes: [`logs/control_inv64_192orbits.json`](logs/control_inv64_192orbits.json),
[`logs/control_inv64_160orbits.json`](logs/control_inv64_160orbits.json).

## Independent corroboration, and a caveat about it

The earlier 746-class cyclic sweep (`prescribed.py`, plus its follow-up rounds
and `prescribed_excluded.py`) is a **separate implementation** and agrees on
every verdict, including the three high-orbit classes that the main sweep's
`8 <= K <= 140` orbit filter excluded and `prescribed_excluded_ub63.log` picked
up (144, 160, 192 orbits -- all `Infeasible`).

**The runtimes do not agree.** `prescribed_excluded.py` settled the 192-orbit
class in 538 s and the 160-orbit class in 298 s; this sweep took 12 088 s and
13 230 s for the same two. Same answers, 22-44x apart, so the two formulations
are materially different. That difference is unexplained and is the reason the
`ub = 64` controls above exist rather than being assumed unnecessary.

## Certification status (2026-08-30)

Independent of `symmetry_prime.py`: the orbit/representative computation was
rewritten from scratch in `symcert_reps.py` (never imports
`symmetry_prime.py`), and its orbit counts agree with the table above for all
28 classes -- a genuine cross-check, since a shared bug in one derivation
would not show up by comparing against itself. `symcert_encode.py` emits the
OPB instance (one variable per orbit, coverage `>= 2` at all 256 vertices as
256 explicit rows, `sum |O| y_O <= 63`) from that independent orbit data.

Two certification routes, mirroring `CERTIFICATION.md`'s architecture for the
main `K(8,1,2)` ladder:

| route | prover | proof system | checker |
|---|---|---|---|
| 1 | RoundingSat 2 (`d4edbf7`, SoPlex 7.1.6) | cutting planes | VeriPB 3.0.2 (`e4ffda3b`), `-c` (forced checked deletion) on every run |
| 2 | SCIP 11.0.0 (source build, `-DEXACTSOLVE=ON -DLPSEXACT=spx`) | exact-rational MILP | `viprcomp` + `viprchk` (`scipopt/vipr`, `30f2951d`), plus `vipr_bind.py` binding the certificate's own header to the committed `.opb` by variable name and constraint multiset -- `viprchk` alone never sees the `.opb`, so without this a certificate could verify a different problem than the one claimed |

Built and run on this session's Linux container (Ubuntu 24.04, x86_64, 4
cores, 15 GB RAM); a second, separate session independently rebuilt and ran
route 2 on the same branch and reached matching `VERIFIED` verdicts for the
classes it re-ran (`p7_a1`, `p5_a1`, `p3_a2`, `p3_a1`), which is corroboration
from a materially different host, not just a repeated run.

### Certified: 4 of 28

| class | order | orbits | route | verbatim checker verdict | wall-clock |
|---|---:|---:|---|---|---:|
| `p7_a1` | 7 | 40 | 1 | `s VERIFIED UNSATISFIABLE` (VeriPB) | 0.37 s solve, <0.1 s check |
| `p5_a1` | 5 | 64 | 1 | `s VERIFIED UNSATISFIABLE` (VeriPB) | 2.74 s solve, <0.1 s check |
| `p3_a2` | 3 | 96 | 2 | `Successfully verified infeasibility.` (`viprchk`), binding `bound=true` | 991.8 s solve, 60.4 s complete, 127.4 s check (this session: 181.6/60.4/127.4 s on a lighter-loaded host) |
| `p3_a1` | 3 | 128 | 2 | `Successfully verified infeasibility.` (`viprchk`), binding `bound=true` | 2 042.5 s solve+complete+check (this session: 740.9 s on a lighter-loaded host) |

All four agree with the floating-point sweep's `Infeasible` verdict for the
same class. Records: `certs_symmetry/cert_p7_a1_ub63.json`,
`cert_p5_a1_ub63.json`, `cert_exact_p3_a2_ub63.json`,
`cert_exact_p3_a1_ub63.json` (each carries tool versions, commit hashes,
per-stage wall-clock, and sha256 + size of the instance and proof).

### Not certified: 24 of 28 -- all order-2 classes, and this looks like a real pattern

Every one of the 24 order-2 classes was attempted by route 2 (route 1 was
also tried on several and abandoned first -- see below); none closed within
budgets ranging from 600 s to 3 600 s (one class, `p2_a0_b7_c1`, was given
3 600 s twice, under two sessions, and still did not close). This is not "we
ran out of time on all 24 by chance": every order-3/5/7 class certified in
under 15 minutes, and no order-2 class certified at any budget tried,
regardless of its internal `(a,b,c)` structure (tested: all-translation
classes with `a=0`, single-2-cycle classes, and all-2-cycle classes up to
`a=4`). Order-2 automorphisms give orbits of size at most 2 -- the weakest
possible symmetry constraint -- so their orbit-ILPs sit much closer in
difficulty to the general, still-open `K(8,1,2) <= 63` problem (see
`certs/MANIFEST.md`'s account of rung 59-60) than the higher-order classes
do. That is a plausible mechanism, not a proof of hardness.

Two things were learned about *why* this is expensive, not just *that* it is:

- **Route 1 (RoundingSat) does not merely run slow on these -- its proof size
  blows up.** `p3_a2` (96 orbits, order 3) certifies via route 1-shaped
  reasoning in seconds; `p2_a0_b7_c1` (128 orbits, order 2) passed 850 MB of
  uncompressed proof and was still climbing after 4 minutes, for an instance
  HiGHS itself solves in 6.5 s. This is the same route-divergence
  `CERTIFICATION.md` documents for the main ladder (§ "the runtimes do not
  agree" above), now seen inside a single class.
- **Route 2 (exact SCIP) is faster but not fast enough, and its uncommitted
  certificate is a real disk hazard.** A killed or timed-out exact solve can
  leave a partial `.vipr` + SCIP's working `.vipr_der` behind at 7-8 GB (one
  attempt reached ~20 GB before an external safety kill); `symcert_certify_exact.py`
  now polls the certificate's on-disk size during the solve and aborts past
  4 GB, and deletes any leftover partial certificate on every non-`VERIFIED`
  exit, recording its size before doing so.

### Narrowing what is left to certify (2026-09-02)

The 24 open classes do not all need the instance they were given. Two facts
shrink the target, one free and one now machine-checked.

**The parity fact.** An order-2 `g = (pi, t)` acts *freely* exactly when its
signed cycle type has `c > 0`. If `c > 0` then `t` is supported on a coordinate
`pi` fixes, so `t` is not in `im(1 + pi)`, so `x xor pi(x) = t` has no solution
and `g` has no fixed point. Every orbit then has size 2, and a `g`-invariant
code -- a disjoint union of orbits -- has **even cardinality**. That covers
**20 of the 24**; the remaining four are exactly the `c = 0` classes, whose
fixed sets are `ker(1 + pi)` of size `2^(8-a)`.

**The bound.** `K(8,1,2) >= 61` is proved in `m61_refutation.py` and formalised
in `lean/` with zero `sorry`s.

Together, for a freely-acting `g`: `|C|` even and `61 <= |C| <= 63` force
`|C| = 62` **exactly**. So for those 20 classes the certification target is not
`sum |O| y_O <= 63` -- an inequality spanning three sizes -- but the single
equality `sum |O| y_O = 62`.

A third fact splits them further. `wt(pi(x) xor t) = wt(x) + wt(t) (mod 2)` and
`wt(t) = c`, so `g` swaps the even- and odd-weight halves exactly when `c` is
odd. At `|C| = 62` the excess rows and the half-excess inequality of
`half_excess.py` leave five splits `(M_e, M_o)`, namely `(29,33)` through
`(33,29)`. Symmetry cuts that to:

| classes | `c` | orbits | surviving `(M_e, M_o)` |
|---|---|---|---|
| 10 | odd | one even + one odd word | `(31,31)` -- **one** |
| 10 | even | both words same parity | `(30,32)`, `(32,30)` -- **two** |
| 4 | `c = 0` | mixed (has fixed points) | sizes `{61, 62, 63}`, splits unrestricted |

`symmetry_parity.py` checks all of this from the orbit structure rather than
from the argument above -- it recomputes each class's orbits and asserts that
free-ness matches `c > 0`, that the fixed sets have size `2^(8-a)`, that every
orbit is parity-mixed iff `c` is odd, and that the surviving split lists are
what the table says. Standard library only, and it shares no code with
`symmetry_prime.py`.

**This certifies nothing new, and it changes a dependency.** The count stands at
4 of 28. What changed is the size of the remaining obligation: 20 instances go
from a three-size inequality to a one-size equality with the weight split fixed
to one or two values, which is a materially smaller search than the one that
defeated both routes. Whether that is small *enough* is untested -- the
certification toolchain is a Linux build and was not re-run here, so the honest
claim is a smaller target, not a closed one.

The dependency matters and is worth stating plainly. This file previously made
**no** use of any bound on `K(8,1,2)`, which is why it could assert `K_sym = 64`
independently of the main ladder. The narrowed `= 62` instances **do** depend on
`K(8,1,2) >= 61`. So there are now two routes, and they are not interchangeable:
the original `<= 63` instances remain unconditional and are what a reader
should use if they want `K_sym = 64` to stand on its own; the `= 62` instances
are cheaper but inherit whatever the `M = 60` refutation rests on. A certificate
should record which of the two it closed.

The **mandatory over-constraint control** was run on the three hardest
classes precisely because a systematically-unrefuted family is the scenario
where an encoding bug would hide: same instance, `ub = 64` instead of 63.
All three came back feasible, `g`-invariant, and `verify.py`-valid:

| class | orbits | `ub=64` | selected orbits | `g`-invariant | `verify.py` |
|---|---:|---|---:|---|---|
| `p2_a1_b6_c0` | 192 | Feasible, size 64 | 48 | yes | `VALID` |
| `p2_a2_b4_c0` | 160 | Feasible, size 64 | 32 | yes | `VALID` |
| `p2_a3_b2_c0` | 144 | Feasible, size 64 | 36 | yes | `VALID` |

Verbatim `verify.py` output for all three:
```
{"n": 8, "mu": 2, "size": 64, "sphere_bound": 57, "excess": 64,
 "coverage_profile": {"2": 192, "3": 64}, "deficient_words": 0}
VALID
```
So the encoding is not over-constrained -- the 24 unresolved classes are
genuinely hard for both routes at `ub = 63`, not an artifact of a bug that
would also have made `ub = 64` infeasible. Codes:
`logs/control_inv64_192orbits_p2_a1_b6_c0.json`,
`logs/control_inv64_160orbits_p2_a2_b4_c0.json`,
`logs/control_inv64_144orbits_p2_a3_b2_c0.json`. Driver: `symcert_control.py`
(solves via `scipy.optimize.milp`/HiGHS -- independent of both
`symmetry_prime.py`'s raw `highspy` call and of the certification routes --
then checks the result with `verify.py`, sharing no solver code with
anything else here).

Every attempt, closed or not, is recorded honestly in `certs_symmetry/` with
its wall-clock and the exact reason it stopped (`BUDGET EXPIRED`, a disk
safety kill, or `VERIFIED`); see `logs/symcert_exact_batch*.log` and
`logs/symcert_triage60.log` for the run order. No verdict disagreement
between the independent encoder and `logs/symmetry_prime_sweep_2026-08-30.log`
was found on any class the independent encoder actually reached a verdict
for -- every closed class agrees with the sweep.

### Update 2026-08-31: budget vs. contention was tested, and turned out not to be the question

The wording above ("this looks like a real pattern") was written from records
produced at a 600-3600 s budget, run either alone or three-at-a-time on a
shared machine -- so it could not distinguish "genuinely hard" from "never
given a fair, uncontended shot." That gap was tested directly: `p2_a0_b7_c1`,
`p2_a4_b0_c0`, and `p2_a1_b6_c0` were each re-run **solo** (nothing else on
the machine) at a **21 600 s (6 h)** budget, 20-35x the budgets above.

A genuine driver bug was found and fixed in the process -- `run_scip()`
captured SCIP's stdout through a `subprocess.PIPE`, which has a fixed 64 KB
kernel buffer, and never drained it while polling; long enough output
deadlocks the child in `write()` with the parent none the wiser until its own
timeout fires. Confirmed directly on the first attempt (SCIP process at 0%
CPU, blocked in `anon_pipe_write`, ~30-45 min in). Fixed by writing stdout to
a file instead (commit `f0b788c`); re-verified against `p3_a2` before
re-running. Any earlier long-running record produced through the unpatched
code should be read with this in mind.

With the fix in place, **all three runs hit the existing disk-safety valve in
`run_scip` (certificate size > 4000 MB) within 715-840 seconds** -- 2-3% of
the 6 h budget, dual bound still 0 in every case. So for these three classes,
neither the original 600-3600 s budget nor contention was ever the binding
constraint, and 6 h solo does not change the reading, because none of the
three runs got remotely close to needing it: **disk is the resource these
classes are actually short of.** Whether more search would close them if
`max_cert_mb` were raised (this host had 30 GB free and used at most 3 GB of
it across all three runs) is a real, still-open question -- deliberately not
answered unilaterally here, since raising a disk-safety threshold is a risk
tradeoff, not a bug fix. Full numbers: `certs_symmetry/MANIFEST.md`'s
"Solo, uncontended, 6h-budget follow-up" section.

## What this does NOT say

- It says nothing about whether `K(8,1,2) <= 63` -- only that any such code is
  asymmetric. **No bound on `K(8,1,2)` itself is stated anywhere in this
  file, or claimed by the certification work above.**
- 4 of the 28 orbit-ILPs are now machine-checked (`certs_symmetry/`); the
  remaining 24 -- all order-2 -- are still floating-point-only HiGHS
  statuses, not proof objects, despite a genuine attempt at certifying them
  with two independent routes and budgets up to an hour per class.
