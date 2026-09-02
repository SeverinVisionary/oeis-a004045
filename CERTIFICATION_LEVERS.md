# What makes the M=60 refutation cheaper, and what does not

The obstacle to `K(8,1,2) >= 61` is not search, it is **proof size**. Floating
point solvers refute M=60 readily (HiGHS 15246 nodes; SCIP 290s), but the
VeriPB proof for M=59 already runs to 8.9 GB.

## The M=60 proof size is NOT predictable from what we have

A "~150x per rung, so ~1.3 TB at M=60" projection has been quoted in this
workstream, including by me. **It is unfounded**, and so is the alternative I
briefly reasoned to (scaling the 8.9 GB by the HiGHS node growth of 12.5x to get
~110 GB). Both misuse the data:

- Proof size does track conflicts: 27.77 MB / 2011 conflicts = 13.8 kB each at
  M=57, and 58.84 MB / 5447 = 10.8 kB each at M=58. So conflict growth is the
  right extrapolant, not wall-clock and not size-ratio-as-a-constant.
- But conflict growth on this route is wildly irregular: 2.7x from M=57 to M=58,
  then ~150x from M=58 to M=59. There is no constant to extrapolate.
- And `WORKLOAD_ESTIMATE` §5.3 says it outright: the PB solver's difficulty does
  not track the MILP's, "the two routes' scaling laws are different and neither
  can be read off the other." Using HiGHS node counts to predict RoundingSat
  proof size is precisely the error it warns about.

What the same section identifies as the real driver is **coverage excess**, not
M: excess is `9M - 512`, so 1 at M=57, 10 at M=58, 19 at M=59, 28 at M=60, and
"excess, not M, is what the PB search feels". That is a mechanism, not yet a
quantitative law.

**Conclusion: the only way to learn the M=60 proof size is to run it.** Any
number quoted before that run is a guess. VeriPB streams its check at ~32 MB
resident, so the constraint is disk, not RAM, and the run is cheap to attempt
and cheap to abandon.

### It was run, and the size projections were all wrong

A cloud run started 2026-09-01 05:10 UTC (`--lp=1`, solo on one core,
gzip-streamed) gives the first real series. Gzipped proof on disk:

| elapsed | size | interval rate |
|---:|---:|---:|
| 31 min | 476 MB | 15.3 MB/min |
| 61 min | 730 MB | 8.5 MB/min |
| 91 min | 973 MB | 8.1 MB/min |
| 121 min | 1149 MB | 5.9 MB/min |
| 152 min | 1329 MB | 6.0 MB/min |
| 182 min | 1479 MB | 5.0 MB/min |
| 212 min | 1616 MB | 4.6 MB/min |

**Growth decelerates throughout.** On this trend the artifact lands near ~2.2 GB
at six hours -- essentially M=59's 2.1 GB gzipped. Free disk moved from 27 GB to
26 GB across the whole run.

So **the wall at M=60 is TIME, not SIZE**, and every projection quoted in this
workstream -- 1.3 TB, 315 GB, and my own 110 GB -- was wrong in the direction
that mattered: each made the route look impossible when it is merely long. M=59
solved in 8206 s; if the PB route tracks the MILP's 12.5x node growth from M=59
to M=60, M=60 needs on the order of a day against the 6 h budget this run has.

### The six-hour run finished: NOT CLOSED, and here is what it cost

Final state of the `--lp=1` solo run (2026-09-01 05:10-11:10, one core):

    conflicts   2 697 000
    proof       2.35 GB gzipped
    verdict     budget expired, M=60 NOT refuted
    disk        27 GB free at start, 25 GB at the low point

Against the same six hours at `--lp=-1`: **18% more conflicts and a 34% smaller
proof**, so `--lp=1` is the better setting on both axes here, and the
bytes-per-conflict figures are 870 B (lp=1) against roughly 2.5 kB for the M=59
artifact.

**Extrapolation, stated as an extrapolation.** M=59's proof implies on the order
of 820 000 conflicts. M=60 has already burned 2.7 M -- 3.3x that -- without
closing. If the rung costs the MILP route's 12.5x node ratio, ~10 M conflicts,
then at the observed rate it needs roughly **22-24 hours** and lands near
**8-9 GB gzipped**. Both fit the 25 GB budget comfortably. This is a projection
from one run and the PB route's growth has been irregular before, so treat the
time as an order of magnitude, not a schedule.

**Actionable consequence:** an M=60 refutation looks reachable with a multi-day
budget and under 10 GB of disk, which would give `K(8,1,2) >= 61`. That is the
single most valuable open computation in this workstream, and nothing about it
requires new mathematics. A long-budget run is in flight.

### Upper bound: still nothing at M=63

The same run spent ~6.5 hours of three-core tabu/local search on M=63 plus
30-minute MILP and SCIP attempts. Best cost reached **7** (seven unsatisfied
coverage constraints), plateaued across 1120 restarts; `milp_model` and
`scip_model` both hit their time limits with no witness. No 63-word double
covering, consistent with the earlier finding that any code of size <= 63 must
have trivial automorphism group, which rules structured search out in principle.

So the question below is which reformulations shrink the *search tree*, node
count being the cheap proxy for proof size.

Node counts below are from `split_bench.py` and `cut_bench.py` on one machine;
absolute times are ~12x the logged historical runs, but node counts match the
logged values exactly (M=60 baseline: 15246 both here and in
`logs/highs_n8_M60.log`), so the instances are identical and the counts are
comparable.

## Does NOT help: restricting to the surviving weight split

The elementary argument reduces M=60 to the single balanced split (30,30) --
four of five splits die by hand. Adding `M_e = M_o = 30` as equalities:

| instance | status | nodes |
|---|---|---|
| M=60, no split | Infeasible | 15246 |
| M=60, reduced to (30,30) | Infeasible | **22737** |

Node count **rose**. The LP relaxation evidently already forces near-balance, so
the equalities prune nothing and merely perturb branching. **Case-splitting is
not a certification lever**, and the plan of certifying only the residual case
is dead. The reduction remains a mathematical result; it is not a computational
one.

## Does help: the Step-2 cuts

For even n, one cut per word:

    W(x) + (n/2) * x_x  >=  n+1,     W(x) = sum_{1 <= d(y,x) <= 2} x_y.

Valid on both branches of the ball identity: `x` not in `C` gives `2W >= 2(n+1)`
directly; `x` in `C` gives the ODD sum `>= 2(n+1)+1`, hence `W >= (n+2)/2`, and
`(n+2)/2 + n/2 = n+1`. It is **cutting-planes derivable from the original rows
in two steps** -- add the `n+1` ball rows of `B(x)`, subtract `x_x <= 1`, divide
by 2 -- so a VeriPB proof may use it and still be a proof about the unaugmented
OPB. Nothing here is a modelling assumption that would need separate
justification.

**The constants are n-dependent.** Hard-coding the n=8 values (4 and n+1 = 9)
makes the cut invalid at n=6, where it wrongly refutes the achievable M=20. The
n=6 M=20 control in `cut_bench.py` caught exactly that, and is kept as an
assertion so the error cannot recur silently.

Measured effect (full run in `logs/cut_bench.log`):

| M | nodes without | nodes with | time without | time with |
|---|---|---|---|---|
| 58 | 28 | 3 | 1.9 s | 2.5 s |
| 59 | 1219 | 992 | 20.5 s | 100.4 s |
| 60 | 15246 | 11604 | 1051 s | 1309 s |

**But the cuts are a net loss in time**, and probably in proof size too. M=59
takes 20.5 s without them and 100.4 s with -- fewer nodes, 5x slower -- because
256 extra rows of ~36 terms each make every LP call substantially more
expensive. Since a VeriPB proof records the LP-based derivations, a bigger LP at
every node plausibly *grows* the artifact even as the tree shrinks. The node
reduction also decays fast with M: 9.3x at M=58, only 1.23x at M=59.

On this evidence the cuts are **not** the lever either. They remain worth
recording because they are sound and CP-derivable, so they cost nothing to keep
available.

## Does NOT help: the SAT route

`sat_bench.py` runs the repository's own CNF model (`sat_model.build`, ball
constraints plus a totalizer cardinality encoding) through CaDiCaL, without
symmetry breaking, since a certificate must be about the unrestricted problem.

The n=6, M=20 control passes (SAT in 0.6 s). At n=8 the route is **hopeless**:
M=58, which HiGHS closes in 1.9 s and 28 nodes, did not finish in ~30 minutes of
CaDiCaL -- a factor of roughly 1000 against the MILP route at the easiest rung
that matters. The run was abandoned there rather than left to burn.

This matches `CERTIFICATION.md`'s own estimate, which put an `n = 8` DRAT proof
at 10^2-10^3 GB and set the SAT route aside. Recorded here as a measurement
rather than an estimate, so it does not get re-proposed.

## Summary: nothing tested shrinks the M=60 certification

| lever | effect |
|---|---|
| restrict to the surviving weight split | tree **grew**, 15246 -> 22737 nodes |
| Step-2 cuts | 1.3x fewer nodes, ~25% more time; likely a bigger proof |
| SAT + totalizer via CaDiCaL | ~1000x slower than MILP at M=58 |

The remaining path to `K >= 61` is to run the M=60 proof and measure it. No
available data predicts its size.
