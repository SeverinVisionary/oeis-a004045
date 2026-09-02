# OEIS A004045: bounds on `K(8,1,2)`

Artifacts for a lower-bound result on binary multiple covering codes.

`K(n,R,mu)` is the minimum size of a binary code `C` in `F_2^n` such that every
word of `F_2^n` has at least `mu` codewords within Hamming distance `R`.
`K(8,1,2)` is the first unknown term of [OEIS A004045](https://oeis.org/A004045).

**Published record: `59 <= K(8,1,2) <= 64`** (lower: Krotov–Potapov 2021;
upper: Östergård 1995).

## Start here

| file | what it is |
|---|---|
| [`PAPER.md`](PAPER.md) | **the paper** — statements, full proofs, references |
| [`./reproduce.sh`](reproduce.sh) | one command, ten self-asserting checks, ~1 min |
| [`TOOLS.md`](TOOLS.md) | pinned external tool versions and build notes |
| [`SHA256SUMS`](SHA256SUMS) | integrity manifest for the in-repo certificates |

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
and exhaustive numerical verification.

### 2. `K(8,1,2) >= 61` — MACHINE-VERIFIED

`m61_refutation.py` refutes `M=60`, and the argument is **fully formalised in
Lean 4** with zero `sorry`s:

```
le_card_of_isDoubleCover : forall (C : Finset V), IsDoubleCover C -> 61 <= C.card
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

So the interval is **`[61, 64]`**, two above the published lower bound. The
trusted base is Lean's kernel plus twelve short definitions; non-vacuity is
checked separately (`lean/Mcov/Sanity.lean`), and every declaration's axiom
trace is printed by `lake build Mcov.Audit`.

It also has four independent machine reviews, all approving — but those are
provenance, not evidence: the formalisation is what establishes it. **No human
has read the proof or the Lean definitions.** A reader wanting to check this
should read the twelve definitions at the top of `lean/Mcov/Basic.lean` and
satisfy themselves they encode `K(8,1,2)`; everything after that is the kernel's
problem, not a matter of judgement.

### Upper bound — unchanged at 64

Local search stalls at cost 2 at `M=63` across six independent designs. That is
**not** evidence of infeasibility. The cyclic prescribed-automorphism sweep is
exhaustive and negative, so any `<= 63` code has trivial cyclic automorphism
group.

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

> **DOI [10.5281/zenodo.22217673](https://doi.org/10.5281/zenodo.22217673)** — *Machine-checkable certificates for
> K(8,1,2) >= 60 (binary twofold covering codes, OEIS A004045)*, CC BY 4.0.

| file | bytes | md5 |
|---|---:|---|
| `cert_n8_M59.vipr` | 3,594,514,707 | `0612e943473044f252388e09695b05da` |
| `cert_n8_M59_complete.vipr.gz` | 2,276,345,927 | `8d8c51b7f1732aa88eb5b81a778a37bc` |
| `inst_n8_M59.opb` | 21,472 | `2db3705e97ced2616dc509051d6768c3` |
| `viprchk_n8_M59.log` | 774 | `b35cf23ddf1adc2c02dc1f65b8ec336e` |
| `cert_n8_M59_route1.json` | 4,214 | `2e2e5e94ebddefef71d5c74a9972ff76` |

Uncompressed `cert_n8_M59_complete.vipr`: md5
`34c48df67d0bfa6d2296856beba63a5a`, sha256
`2f2a335f883e4b88630cebbaa3d47ce2ea30986b722df54084dcc4926d2d6ddf`.
Note `viprchk` does **not** read gzip; the uncompressed file is the checkable
one. Everything **in** this repository is covered by `SHA256SUMS`.

`K(8,1,2) >= 60` does not depend on these: it also follows from the half-page
theorem with no computation at all, and from exhaustive numerical verification.

## Formalisation

`lean/` holds a Lean 4 + mathlib formalisation of the `M=60` refutation, and it
is now **complete with zero `sorry`s**:

    no_60_word_double_cover : forall (C : Finset V), IsDoubleCover C -> #C != 60
      depends on axioms: [propext, Classical.choice, Quot.sound]

Non-vacuity is checked separately in `lean/Mcov/Sanity.lean` (the space has 256
words; the predicate is both satisfiable and non-trivial), and every lemma's
axiom trace is printed by `lake build Mcov.Audit`. One step is still informal:
going from `#C != 60` to `K(8,1,2) >= 61` needs monotonicity, which `PAPER.md`
states but Lean does not yet.

## Layout

| path | role |
|---|---|
| `EXCESS_THEOREM.md` | the theorem, the weight split, the half-excess inequality |
| `PRIOR_ART_EXCESS.md` | the prior-art gate, closed on primary sources |
| `PRIOR_ART.md` | the original admission gate for the target |
| `PAPER_DRAFT.md` | claim ladder in confidence order |
| `RESEARCH_LOG.md` | the working notes this began as |
| `dominance.py`, `hhkl_theorem6.py`, `mu_generalization.py` | the bound and its context |
| `m61_refutation.py` | the `M=60` refutation (candidate) |
| `verify.py` | standalone verifier, shares no code with any search |
| `certs/`, `certs_exact/`, `certs_symmetry/` | machine-checkable proof objects |
| `lean/` | Lean 4 formalisation (skeleton) |
| `reviews/` | archived independent review transcripts (provenance only) |
| `DEPOSIT.md` | Zenodo deposit manifest and checksums |

## Claim discipline

Statements here are graded. "Established" means independently reproduced and
machine-checked; "candidate" means reviewed but unconfirmed by a human;
negative results are recorded with the measurements that produced them, and
retractions are kept in place rather than deleted. Machine reviews are recorded
as provenance and are **not** offered as evidence of correctness.

## Licence

Software (`*.py`, `Makefile`, `reproduce.sh`, `lean/`) under the MIT Licence
(`LICENSE`). Documentation, proofs, tables and certificates under CC BY 4.0
(`LICENSE-DOCS`).

## Cite

See `CITATION.cff`. Author: Hanyu Yang,
ORCID [0009-0005-0419-4070](https://orcid.org/0009-0005-0419-4070).
