# OEIS A004045: bounds on `K(8,1,2)` — binary twofold covering codes, verified in Lean 4

A machine-checked lower bound for **binary multiple covering codes** (twofold
coverings, double coverings, μ-fold coverings of radius 1 in the Hamming cube),
with a new elementary theorem for all even `n` and a **Lean 4 formalisation with
zero `sorry`s**. Every claim is reproducible from this repository.

`K(n,R,mu)` is the minimum size of a binary code `C` in `F_2^n` such that every
word of `F_2^n` has at least `mu` codewords within Hamming distance `R`.
`K(8,1,2)` is the first unknown term of [OEIS A004045](https://oeis.org/A004045).

**Published record: `59 <= K(8,1,2) <= 64`.** The lower bound 59 is
Krotov–Potapov 2021. The upper bound 64 is *older than usually credited*: it is
already the doubling `K(8,1,2) <= 2*K(7,1,2) = 64` in the 1993 table of
Hämäläinen, Honkala, Kaikkonen and Litsyn. Östergård's 1995 tabu-search paper
improves 27 upper bounds in that table, but `n = 8`, `mu = 2` is **not** among
them — see [`PRIOR_ART.md`](PRIOR_ART.md).

**This repository establishes `61 <= K(8,1,2) <= 64`.**

## Start here

| file | what it is |
|---|---|
| [`PAPER.md`](PAPER.md) | **the paper** — statements, full proofs, references |
| [`./reproduce.sh`](reproduce.sh) | one command, twelve self-asserting checks, ~1 min |
| [`TOOLS.md`](TOOLS.md) | pinned external tool versions and build notes |
| [`SHA256SUMS`](SHA256SUMS) | integrity manifest for the 119 in-repo certificate files |

## Results

### 1. An elementary lower bound for all even `n` — ESTABLISHED

For **even** `n`, every binary code whose closed radius-1 balls cover each point
at least twice satisfies

```
|C| >= ceil( 3 * 2^(n+1) / (3n+2) )
```

Half a page, by a parity/excess argument. It **strictly improves the best
published lower bound at five table positions**, and reproves one exact value
without any search:

| `n` | best published | this bound | |
|---:|---:|---:|---|
| 6 | 20 (Seuranen 2007, exhaustive) | **20** | matched, but search-free |
| 8 | 59 (Krotov–Potapov 2021) | **60** | +1 |
| 10 | 188 | **192** | +4 |
| 12 | 640 | **647** | +7 |
| 14 | 2195 | **2235** | +40 |
| 16 | 7783 | **7865** | +82 |

Proved in `dominance.py` to strictly beat Krotov–Potapov Theorem 6 at `mu=2`
for **every even `n >= 6`**, ceiling included — the real gap is below 1 at
`n=6` (8/15) and `n=8` (16/39), so those need separate treatment, and a uniform
`2^n/(16 n^2)` bound closes the rest. The additive gap grows like
`(2/3) 2^n / n^2` even though the ratio of the two bounds tends to 1.

`K(8,1,2) >= 60` holds by **three independent routes**: this theorem; an
exact-rational SCIP → VIPR certificate refuting `M=59` accepted by `viprchk`;
and agreement of two independent floating-point solvers (evidence, not a
certificate).

### 2. `K(8,1,2) >= 61` — MACHINE-VERIFIED

`m61_refutation.py` refutes `M=60`, and the argument is **fully formalised in
Lean 4** with zero `sorry`s:

```
le_card_of_isDoubleCover : forall (C : Finset V), IsDoubleCover C -> 61 <= C.card
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

So the interval is **`[61, 64]`**, two above the published lower bound. The
trusted base is Lean's kernel plus four short definitions; non-vacuity is
checked separately (`lean/Mcov/Sanity.lean`), and every declaration's axiom
trace is printed by `lake build Mcov.Audit`.

The formalisation is what establishes it; no other provenance is offered. **No
human has read the proofs**, which rest on Lean's kernel. A reader wanting to
check this should read the four definitions the theorem statement mentions —
`V`, `dist`, `cov`, `IsDoubleCover`, at the top of `lean/Mcov/Basic.lean` — and
satisfy themselves they encode `K(8,1,2)`; everything after that is the kernel's
problem, not a matter of judgement. The other definitions in that file are proof
machinery and do not occur in the statement, so they are outside the trust
boundary. **The author read the four on 2026-09-03**, cross-checked by
transliterating them and reproducing the published `K(4,1,2) = 8` exhaustively.

### Upper bound — unchanged at 64

Local search stalls at cost 2 at `M=63` across six independent designs. That is
**not** evidence of infeasibility.

What is known is where a better code cannot live. Any non-identity automorphism
has a power of prime order, so it is enough to rule out prime-order ones, and
all 28 prime-order classes of `Aut(Q_8) = F_2^8 : S_8` come back infeasible at
`<= 63`: **any `<= 63` code is asymmetric** (`SYMMETRY_THEOREM.md`). An
independent 746-class cyclic sweep (`prescribed.py`) agrees on every verdict,
and its accounting closes exactly -- 742 swept plus 3 the orbit filter dropped
is all 745 non-identity classes, of which 439 have minimum exactly 64, 76 are
infeasible outright, and the 227 that timed out were resolved in two follow-up
rounds, every one infeasible, with no covering of size `<= 63` found anywhere.

The caveat is that only **4 of the 28** are machine-checked; the other 24, all
order 2, are floating-point solver verdicts. `symmetry_parity.py` narrows what
is left: an order-2 element acts freely exactly when its signed type has
`c > 0`, so an invariant code has even size, and with `K(8,1,2) >= 61` that
pins 20 of the 24 to `|C| = 62` exactly, with the weight split forced to one
value (`c` odd) or two (`c` even). Smaller target, still not closed.

## Reproduce

```
./reproduce.sh          # core claims, ~1 minute, exits non-zero on any failure
./reproduce.sh --full   # also the solver-backed models (see requirements)
```

Every script is self-asserting: it fails loudly rather than printing a wrong
number. **The eight core scripts are standard library only** — checking the
theorem needs no dependencies at all. `scipy` is used only for LP controls.

```
python3 excess_theorem.py       # the theorem, exhaustively at n=4,6,8
python3 dominance.py            # dominance over Krotov-Potapov + ceiling lemma + table audit
python3 hhkl_theorem6.py        # why HHKL 1993 cannot produce this bound
python3 mu_generalization.py    # the even-mu generalisation, brute-forced
python3 m61_refutation.py       # the M=60 refutation and its discriminating test
python3 local_search.py --gate  # known-answer gate, n=4..8
python3 verify.py --incumbent   # independent verifier, rebuilds the 64-word code
```

## Prior art

Closed on **primary sources**, not inference — see `PRIOR_ART_EXCESS.md`.

The novelty argument is positive rather than an absence: Hämäläinen–Honkala–
Kaikkonen–Litsyn's excess term `eps` provably **vanishes at even `mu`**, so
their method cannot produce this bound, which is why their Corollary 2 is
stated only for odd `mu` — and no `mu=2` entry in their own table is marked as
coming from it. `hhkl_theorem6.py` checks this as exact rational equality.

**One acknowledged gap.** A preprint *Chen, W. and Li, D., "Lower bounds for
multiple covering codes"* is cited as forthcoming in HHKL 1993 (ref [2]) and was
never located. Disclosed as a priority risk, never cited. Separately,
Krotov–Potapov already use Delsarte nonnegativity on a covering code's own
distance distribution to obtain the published 59, so that ingredient is standard
for this table and is not claimed as new.

## Artifacts outside this repository

The two large certificates do not fit sensibly in git. They are archived openly
and citably:

> **Cite: DOI [10.5281/zenodo.22217672](https://doi.org/10.5281/zenodo.22217672)**
> — *Machine-checked bounds on K(8,1,2), the first unknown term of OEIS A004045*.
> This is the **concept DOI** and always resolves to the current version; use it
> in preference to a version DOI, which pins readers to a snapshot. Current
> version 2.1. v1.0 was *Machine-checkable certificates for K(8,1,2) >= 60*.
> Code MIT, prose CC BY 4.0.

| file | bytes | md5 |
|---|---:|---|
| `cert_n8_M59.vipr` | 3,594,514,707 | `0612e943473044f252388e09695b05da` |
| `cert_n8_M59_complete.vipr.gz` | 2,276,345,927 | `8d8c51b7f1732aa88eb5b81a778a37bc` |
| `inst_n8_M59.opb` | 21,472 | `2db3705e97ced2616dc509051d6768c3` |
| `viprchk_n8_M59.log` | 774 | `b35cf23ddf1adc2c02dc1f65b8ec336e` |
| `cert_n8_M59_route1.json` | 4,214 | `2e2e5e94ebddefef71d5c74a9972ff76` |

The record also carries the package itself — `oeis-a004045.tar.gz` (the
repository at the released commit) and `PAPER.md` — whose sizes change each
release; read those off the record. See [`DEPOSIT.md`](DEPOSIT.md).

Uncompressed `cert_n8_M59_complete.vipr`: md5
`34c48df67d0bfa6d2296856beba63a5a`, sha256
`2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf`.
Note `viprchk` does **not** read gzip; the uncompressed file is the checkable
one. `SHA256SUMS` covers the 119 certificate files under `certs/`,
`certs_exact/` and `certs_symmetry/` -- the artefacts whose bytes a checker
consumes. It is **not** a manifest of the whole repository: for source and prose
the authority is git, which hashes every tracked file anyway. `./reproduce.sh`
verifies the manifest.

`K(8,1,2) >= 60` does not depend on these: it also follows from the half-page
theorem with no computation at all, and is corroborated by two independent
floating-point solvers.

## Formalisation

`lean/` holds a Lean 4 + mathlib formalisation of the `M=60` refutation, and it
is now **complete with zero `sorry`s**:

    no_60_word_double_cover : forall (C : Finset V), IsDoubleCover C -> #C != 60
      depends on axioms: [propext, Classical.choice, Quot.sound]

Non-vacuity is checked separately in `lean/Mcov/Sanity.lean` (the space has 256
words; the predicate is both satisfiable and non-trivial), and every lemma's
axiom trace is printed by `lake build Mcov.Audit`. The step from `#C != 60` to
`K(8,1,2) >= 61` is monotonicity, and it is formalised too (`cov_mono`,
`isDoubleCover_mono`, `le_card_of_isDoubleCover`); nothing in the chain is left
informal.

## Layout

| path | role |
|---|---|
| `EXCESS_THEOREM.md` | the theorem, the weight split, the half-excess inequality |
| `PRIOR_ART_EXCESS.md` | the prior-art gate, closed on primary sources |
| `PRIOR_ART.md` | the original admission gate for the target |
| `PAPER_DRAFT.md` | claim ladder in confidence order |
| `RESEARCH_LOG.md` | the working notes this began as |
| `dominance.py`, `hhkl_theorem6.py`, `mu_generalization.py` | the bound and its context |
| `m61_refutation.py` | the `M=60` refutation, giving `K >= 61` (formalised in `lean/`) |
| `verify.py` | standalone verifier, shares no code with any search |
| `certs/`, `certs_exact/`, `certs_symmetry/` | machine-checkable proof objects |
| `lean/` | Lean 4 formalisation of `K >= 61` — complete, zero `sorry`s |
| `reviews/` | archived independent review transcripts (provenance only) |
| `DEPOSIT.md` | Zenodo deposit manifest and checksums |

## Claim discipline

Statements here are graded. "Established" means independently reproduced and
machine-checked; "established, partly certified" means reproduced but with some
sub-cases resting on floating-point solver verdicts (this is the status of the
asymmetry result: 4 of its 28 classes are certified, 24 are not); "candidate"
means reviewed but unconfirmed by a human;
negative results are recorded with the measurements that produced them, and
retractions are kept in place rather than deleted. Machine reviews are recorded
as provenance and are **not** offered as evidence of correctness.

## Licence

Software (`*.py`, `Makefile`, `reproduce.sh`, `lean/`, including `lean/*.md`)
under the MIT Licence (`LICENSE`). All other documentation, proofs, tables and
certificates under CC BY 4.0 (`LICENSE-DOCS`). Where a file could fall under
both — `lean/README.md`, `certs*/MANIFEST.md` — MIT governs files under
`lean/` and CC BY 4.0 governs the rest.

The Zenodo deposit is recorded as MIT because Zenodo takes a single licence
field; the dual split above is the authoritative one and is reproduced in the
deposit description.

Third-party tools that produced committed artifacts (SCIP, SoPlex, HiGHS,
PySCIPOpt, RoundingSat, VeriPB, Lean/mathlib) are Apache-2.0 or MIT and are
**not** redistributed here — only their output. VIPR (`scipopt/vipr`, used for
`viprcomp`/`viprchk`) carries no licence file upstream; that affects anyone
cloning it per `CERTIFICATION.md`, not the artifacts here.

## Cite

See `CITATION.cff`. Author: Hanyu Yang,
ORCID [0009-0005-0419-4070](https://orcid.org/0009-0005-0419-4070).
