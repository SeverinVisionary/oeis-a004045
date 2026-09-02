# Certification session, 2026-08-29

Raw record of the session that built the certification leg §5 of the workload
estimate called for. **No bound in this file is claimed as a result**; the
certified statements, with what checked them and what is still trusted, are in
[`../certs/MANIFEST.md`](../certs/MANIFEST.md).

## Machine

| | |
|---|---|
| host | Apple M1 Pro, 10 cores, 16 GB, arm64 |
| OS | macOS 26.6.1, Darwin 25.6.0 |
| contention | **shared with other sessions**; 1-minute load average 10–17 throughout, and a SCIP source build ran concurrently for part of it. Wall-clock is soft by up to ~2.7× (measured: the identical `n = 8, M = 57` search — same 25 632 conflicts — took 170.7 s and 63.4 s in two runs). Conflict counts and proof sizes are not soft. |
| driver Python | 3.12.8 |

## Toolchain, as built

| tool | version | commit | role |
|---|---|---|---|
| RoundingSat 2 | branch `master` | `d4edbf7` (2026-03-03) | PB solver; emits VeriPB v2.0 cutting-planes derivations |
| SoPlex | 7.1.6 | release-716 tarball | LP relaxation inside RoundingSat — **load-bearing, see below** |
| VeriPB | 3.0.2 | `e4ffda3b` (2026-08-26) | proof checker (Rust) |
| VeriPB | 2.3.0 | `b0d55dc8` (2025-06-05), branch `version2` | *second* proof checker (Python + C++), independent implementation |
| SCIP Optimization Suite | 10.0.0 | release tarball | exact-rational MILP, route 2 |
| VIPR `viprchk` / `viprcomp` | — | `scipopt/vipr` `30f2951d` (2025-10-29) | route 2 certificate completion and checking |
| oneTBB | v2022.0.0 | — | required by `viprcomp` |
| Boost | 1.88.0 | — | RoundingSat / SoPlex multiprecision |
| GMP | 6.3.0 | — | built from source, arm64, `--enable-cxx` |
| MPFR | 4.2.2 | — | built from source, arm64 |
| rustc / cargo | 1.98.0 | — | |
| CMake | 4.4.3 | — | |

## Build blockers hit, and the fix

Recorded because §5 of the estimate is supposed to be measured, and these are
most of what "2–5 days engineering" actually consists of.

| blocker | symptom | fix |
|---|---|---|
| macOS 26 ships no linkable `liblzma` | VeriPB 3.x fails to link: `Undefined symbols ... _lzma_code` | `LZMA_API_STATIC=1 cargo build --release`, so `lzma-sys` compiles its bundled C source |
| Homebrew on this host is **x86_64 under Rosetta** | every brew library is the wrong architecture for an arm64 binary; brew's Boost is 1.60 (2016) and does not compile under C++20 | build GMP and MPFR from source for arm64; install Boost 1.88 into a private prefix |
| CMake 4.x removed `FindBoost` | `find_package(Boost)` needs a `BoostConfig.cmake`, which a bare header tree does not have | install Boost with its own `b2`, which generates the CMake package config (~25 min, almost all of it copying headers) |
| `/usr/local/include` shadows the private Boost | RoundingSat compiled against brew's Boost 1.60 and failed on `std::binary_function` / `std::auto_ptr` | pass the private include as a real `-I` via `CMAKE_CXX_FLAGS`, not only as `-isystem` |
| CMake picks x86_64 under Rosetta | `-arch x86_64` in the compile flags on an M1 | `-DCMAKE_OSX_ARCHITECTURES=arm64`, and pass it through to the nested SoPlex build via `soplex_cmake_args` |
| python.org Python 3.12 builds `universal2` extensions | VeriPB 2.x's extension linked GMP for the x86_64 slice only, then failed at import with `symbol not found in flat namespace '...__mpz_struct'` | `ARCHFLAGS=-arch arm64`, `_PYTHON_HOST_PLATFORM=macosx-11.0-arm64`, `pip install --no-build-isolation` (build isolation drops the env), and GMP built `--enable-cxx` for `libgmpxx` |
| RoundingSat rejects a classic OPB header when proof logging | `Error: Invalid opb header.` | emit the PB competition 2024 header `* #variable= N #constraint= M #equal= 0 intsize= K`; the proof's `f` line needs the constraint count |
| CMake 4.x rejects VIPR's declared minimum | `Compatibility with CMake < 3.5 has been removed` | `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` |
| PyPI `pyscipopt` has no exact mode | `enableExactSolving(True)` -> `SCIP was compiled without exact solve support`; no `exact/*` parameters exist in that build at all | source build with `-DEXACTSOLVE=ON -DLPSEXACT=spx` (§5 of `CERTIFICATION.md`) |
| the archived VIPR repository's checker is too old | `ambros-gleixner/VIPR`'s `viprchk` rejects SCIP 10 certificates with `Syntax Error in AggrRow_193: Expecting } but read instead {` — which reads exactly like a corrupt certificate | use the maintained `github.com/scipopt/vipr`; the archived repo says so in its own README |
| SCIP 10 writes **incomplete** certificates | aggregation rows carry `{ lin weak { 0 } ... }` reasons whose multipliers are left to be reconstructed; `viprchk` alone cannot read them. Neither `set separating maxrounds 0` nor `set exact safedbmethod e` suppresses this — both were tried | run `viprcomp` first, which reconstructs them with an exact rational LP solve and writes `<name>_complete.vipr` |
| `viprcomp` needs oneTBB | `ld: symbol(s) not found ... tbb::detail::d1::task_arena` | build oneTBB v2022.0.0 for arm64 and pass `-DTBB_DIR`. Build the `viprchk` *target*, not `all`, if you only want the checker — `viprcomp` and `viprchk_parallel` drag TBB in |

## The measurement that decided the architecture: SoPlex is not optional

RoundingSat was first built with `-Dsoplex=OFF`. On the *easiest* genuine
known-answer instance:

| build | instance | outcome |
|---|---|---|
| RoundingSat, `soplex=OFF` | `n = 6, M = 19` | **did not close in 10 minutes**; 212 MB of proof emitted and still running when killed |
| RoundingSat, `soplex=ON` (SoPlex 7.1.6) | `n = 6, M = 19` | **UNSAT in 0.22 s**, 3 099 conflicts, 4.31 MB proof |

Three orders of magnitude, on the gate instance. The reason is visible in the
solver's own statistics: of the 3 099 conflicts, **109 valid Farkas
constraints** came from the LP, against 2 Gomory cuts. This is the same fact
§3.2 of the estimate recorded from the other side — "counting arguments live
naturally in the LP relaxation and painfully in resolution". A PB solver
without an LP is on the resolution side of that line. Anyone reproducing this
work who builds RoundingSat with the default `soplex=ON` will never see the
problem; anyone who turns it off will conclude the route is dead.

## The second tuning result: the LP call cap

`--lp` caps how often RoundingSat may call the LP, as a ratio of pivots to
conflicts (default 1); `-1` removes the cap. On instances whose refutations
*are* LP-shaped counting arguments, removing it is worth an order of magnitude:

| instance | `--lp=1` (default) | `--lp=-1` |
|---|---|---|
| `n = 6, M = 19` | 3 099 conflicts, 0.22 s, 4.31 MB | **53 conflicts, 0.04 s, 0.50 MB** |
| `n = 8, M = 57` | 25 632 conflicts, 63 s, 227 MB | **2 011 conflicts, 2.6 s, 27.8 MB** |

24× in time and 8× in artifact size at rung 57. Every committed certificate was
produced with `--lp=-1`. It changes the search and therefore the proof; it does
not change what the proof proves, and VeriPB checks the result either way.

The first ladder run had already been started at the default when this was
measured, and was restarted. **That restart caused the one alarming-looking
event of the session**: VeriPB 2.3.0 was mid-read of `proof_n8_M57.pbp.gz` when
the ladder rewrote it, and reported `Expected literal` at line 99987 — which is
indistinguishable at a glance from a bad proof. Re-run against the stable
artifact it returned `s VERIFIED UNSATISFIABLE`. Hashes in the records and the
hash check in `recheck.py` exist for exactly this.

## Results

See [`../certs/MANIFEST.md`](../certs/MANIFEST.md) for the certified
statements, with per-stage times, sizes and hashes, and
[`../certs/ladder.log`](../certs/ladder.log) for the raw run order.

Summary of what a checker accepted:

| statement | route | checked by |
|---|---|---|
| `K(6,1,2) = 20` | PB + cutting planes | VeriPB 3.0.2 **and** VeriPB 2.3.0 |
| `K(7,1,2) = 32` | PB + cutting planes | VeriPB 3.0.2 **and** VeriPB 2.3.0 |
| `K(6,1,2) > 19` | PB + cutting planes | VeriPB 3.0.2 **and** VeriPB 2.3.0 |
| `K(7,1,2) > 31` | PB + cutting planes | VeriPB 3.0.2 **and** VeriPB 2.3.0 |
| `K(8,1,2) > 57` | PB + cutting planes | VeriPB 3.0.2 **and** VeriPB 2.3.0 |
| `K(8,1,2) > 58` | PB + cutting planes | VeriPB 3.0.2 **and** VeriPB 2.3.0 |
| `K(6,1,2) > 19` | exact-rational MILP + VIPR | `viprchk` |
| `K(7,1,2) > 31` | exact-rational MILP + VIPR | `viprchk` |
| `K(8,1,2) > 57` | exact-rational MILP + VIPR | `viprchk` |
| `K(8,1,2) > 58` | exact-rational MILP + VIPR | `viprchk` |
| `K(8,1,2) > 59` | exact-rational MILP + VIPR | `viprchk` — **one route only**, see the manifest |

The gate cases are published facts, which is the point of running them first.
`K(8,1,2) > 57` and `K(8,1,2) > 58` are each certified twice, by two routes with
no prover, proof system or checker in common, over one and the same `.opb`
file — and both are weaker than the published lower bound of 59.

`K(8,1,2) > 59` is the exception and the one line that needs care: it is one
rung past the published bound, and it has **one route, one checker, and a
6.47 GB artifact that is not committed**. It is not claimed as a result. The
caveats, timings, hashes and regeneration command are in
`../certs/MANIFEST.md`; the checker output is in
[`viprchk_n8_M59.log`](viprchk_n8_M59.log).

`M = 60` was not attempted by either route. That is a resource limit, not a
choice: route 2's completed certificate grew 34.8× from rung 57 to 58 and 73.0×
from 58 to 59, reaching 6.47 GB, and `viprchk`'s peak RSS tracked it at 1.04×.
Rung 60 projects to ~230 GB of certificate and comparable RSS on the optimistic
extrapolation, against this host's 16 GB of RAM and 20 GB of free disk. The
arithmetic and the caveats are in `../certs/MANIFEST.md`.

Where the ladders stopped, and why, is in `../certs/MANIFEST.md`.

## The route comparison, which reversed the estimate's recommendation

| rung | route 1 solve (RoundingSat + SoPlex) | route 2 solve (exact SCIP 10) |
|---:|---:|---:|
| `n=6, M=19` | 0.04 s | 0.42 s |
| `n=8, M=57` | 2.6 s | 0.37 s |
| `n=8, M=58` | 558.4 s | **6.30 s** |
| `n=8, M=59` | not closed in ~50 min at `--lp=-1`, nor in ~50 min at `--lp=1` | **2 394 s, closed** |

§5 of the estimate recommended the PB route on the grounds that cutting planes
is the proof system these refutations live in. That reasoning is sound and the
proof sizes bear it out — but on *solving* cost the exact MILP wins by 89× at
rung 58 and is pulling away. The pilot's own floating-point numbers implied it:
HiGHS closes rung 58 in 28 nodes and exact SCIP in 175, a factor of six for
exactness, against the PB solver's factor of hundreds.

The routes are complementary rather than ranked. Route 1 has a second,
independent checker and smaller artifacts. Route 2 is far faster and reaches
further, but it trusts SCIP to emit a certificate for the problem it actually
solved — a class of bug `viprchk` cannot catch and route 1 is not exposed to.

## Encoding audit

`make audit` — 54 checks over every instance the certificates use (`n = 6, 7, 8`
decision rungs plus the three optimisation instances), all passing. The
load-bearing one compares the OPB constraint multiset against the rows
`milp_model.py` actually feeds HiGHS, captured by executing the model with a
recording stand-in for `highspy.Highs`. The behavioural ones evaluate the
published 64-word incumbent and two deliberately broken codes against the
parsed constraints and require agreement with `verify.py` on how many words are
deficient.

One bug in the audit itself is worth recording because it is the kind that
makes a test vacuous: the first version decided whether `verify.py` had passed
with `stdout.endswith("VALID")`, and `"INVALID".endswith("VALID")` is true, so
every broken code was scored as valid. The audit still reported PASS. It now
compares the whole last line and rejects anything that is not exactly `VALID`
or `INVALID`.
