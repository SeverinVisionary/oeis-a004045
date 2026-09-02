# Twofold coverings of the Hamming cube

### A Lean-verified `K(8,1,2) ≥ 61`, and an even-`n` theorem improving five published bounds

## At a glance

| | before this work | after | how it is checked |
|---|---|---|---|
| **`K(8,1,2)`** — first unknown term of A004045 | `59 ≤ K ≤ 64` | **`61 ≤ K ≤ 64`** | **Lean 4, zero `sorry`s** |
| lower bound for **all even `n`** | Krotov–Potapov (2021) | `⌈3·2^(n+1)/(3n+2)⌉`, strictly better for every even `n ≥ 6` | half-page proof + script |
| `K(6,1,2)` | `= 20`, by integer programming | `= 20`, **by hand** | script, no search |
| symmetry of any `≤ 63` code | not addressed | must be **completely asymmetric** | 28 classes; 4 certified, 24 not |
| **upper bound** | `64` (1993) | **`64` — untouched** | — |

### The five published entries this improves

| `n` | published lower bound | this work | improvement |
|---:|---:|---:|---:|
| 8 | 59 | **60** | +1 |
| 10 | 188 | **192** | +4 |
| 12 | 640 | **647** | +7 |
| 14 | 2195 | **2235** | +40 |
| 16 | 7783 | **7865** | +82 |

The ratio to the old bound tends to 1, but the additive gap grows like
`(2/3)·2^n/n²` and is unbounded, so the improvement does not run out.

---

# What this deposit proves

Take the 256 binary strings of length 8. Choose a set `C` of them — call these
*sentinels* — so that **every** one of the 256 strings is within one bit-flip of
at least **two** sentinels. Two rather than one, so the system still works when a
sentinel fails. How few sentinels are enough?

That number is `K(8,1,2)`. It is the first unknown term of
[OEIS A004045](https://oeis.org/A004045), and the published record was

    59 ≤ K(8,1,2) ≤ 64

— the lower bound from Krotov and Potapov (2021), the upper bound already in the
1993 table of Hämäläinen, Honkala, Kaikkonen and Litsyn.

**This deposit raises the lower bound by two:**

    61 ≤ K(8,1,2) ≤ 64

so the answer is now known to be 61, 62, 63 or 64. Two of the six candidate
values are eliminated.

The first step, `K ≥ 60`, comes from a general theorem proved here for **every
even `n`**:

> **`K(n,1,2) ≥ ⌈ 3·2^(n+1) / (3n+2) ⌉`**

The second step, `K ≥ 61`, is a separate argument, and it is **checked by a proof
assistant**:

    le_card_of_isDoubleCover : ∀ (C : Finset V), IsDoubleCover C → 61 ≤ C.card
      depends on axioms: [propext, Classical.choice, Quot.sound]

Zero `sorry`s, no `native_decide`. Those three axioms are the ordinary
foundations of mathlib; what matters is that `sorryAx` is absent.

## What is new

**1. The even-`n` theorem improves five published table entries, and infinitely
many more.** It raises the Krotov–Potapov values at `n = 8, 10, 12, 14, 16` from
`59, 188, 640, 2195, 7783` to `60, 192, 647, 2235, 7865`. The ratio to the old
bound tends to 1, but the additive gap grows like `(2/3)·2^n/n²` and is
unbounded. The proof is half a page.

**2. It gives `K(6,1,2) = 20` with no computer search.** The value itself is
known; the published route to it was integer programming. Here it falls out of
the theorem plus a weight-parity split, by hand.

**3. `K(8,1,2) ≥ 61` is machine-verified.** This is the part we would most like
to be judged on. The literature for this table consists largely of uncertified
integer-programming runs. Here the headline inequality does not rest on a solver
log, or on the author's care: it reduces to Lean's kernel plus twelve short
definitions a reader can check by eye. Non-vacuity is checked separately — the
space really has 256 words, and the covering predicate is proved both
satisfiable and non-trivial, so the theorem is neither vacuous nor trivial.

**4. Every `≤ 63` solution must be completely asymmetric.** All 28 prime-order
conjugacy classes of `Aut(Q_8) = F_2^8 ⋊ S_8` are infeasible at `≤ 63`. So if a
63-word code exists, it has trivial automorphism group. Every classical
construction in this area is symmetric, which is a plausible reason the upper
bound has not moved since 1993 — and it tells a future search to break symmetry
rather than prescribe it.

## Nothing stronger is claimed

**The upper bound is untouched.** It remains 64. That value is older than it is
usually credited: it is in the 1993 HHKL table as the doubling
`K(8,1,2) ≤ 2·K(7,1,2) = 2·32`, a one-line argument. Östergård's 1995
tabu-search paper improves 27 upper bounds in that table; this is not one of
them. Closing the remaining gap is open.

**Novelty of the even-`n` theorem is not claimed.** We did not find it in the
primary sources we checked, and we can show *positively* that the standard
method cannot produce it — the parity term of HHKL's Theorem 6 vanishes
identically at even multiplicity, which is exactly where ours fires. But a
preprint, *W. Chen and D. Li, "Lower bounds for multiple covering codes"*, is
cited as forthcoming in HHKL and was never published; we could not locate it.
Separately, Krotov and Potapov already apply Delsarte nonnegativity to a
covering code's own distance distribution, so that ingredient is standard here.

**Result 4 is on a weaker footing than the rest.** Only 4 of its 28 classes are
machine-certified; the other 24, all of order 2, are floating-point solver
verdicts. Both certification routes blow up on them — one passed 850 MB of proof
on an instance a floating-point solver settles in seconds. The package says so
wherever the result is stated.

**No human has reviewed the proof or the Lean definitions.** The work was done
with heavy use of large language models — Anthropic Claude (Opus 5) and Fable
5.1, OpenAI GPT-5.6 (ChatGPT and Codex), and DeepSeek v4 — for literature
search, for proposing the `M = 60` argument, for most of the code and the Lean
development, and for adversarial review. That is why nothing here treats machine reasoning as
evidence. Every load-bearing claim is either short enough to check by hand, a
self-asserting script, a machine-checkable certificate, or a formal proof. The
archived review transcripts are provenance, not evidence.

## What is in the archive

`oeis-a004045.zip` contains the whole package:

| | |
|---|---|
| `PAPER.md` | the paper |
| `reproduce.sh` | one command, twelve self-asserting checks, ~1 minute |
| `lean/` | the Lean 4 development, zero `sorry`s |
| `certs/`, `certs_exact/`, `certs_symmetry/` | 119 machine-checkable proof objects |
| `verify.py` | standalone verifier, sharing no code with any search |
| `PRIOR_ART.md`, `PRIOR_ART_EXCESS.md` | what was checked, and what was not |
| `SYMMETRY_THEOREM.md` | result 4 and its certification status |

To check it yourself:

    unzip oeis-a004045.zip && cd oeis-a004045-*/
    ./reproduce.sh                     # exits non-zero if any check fails
    cd lean && lake exe cache get && lake build Mcov.Final

`reproduce.sh` needs only the Python standard library, apart from one step that
uses `scipy` for small LP control cases. The Lean build is separate and takes
about four minutes warm.

The deposit also carries the exact-rational certificate refuting `|C| = 59`
(`cert_n8_M59.vipr`, 3.6 GB, from SCIP 10.0 with SoPlex 7.1.6, completed by
`viprcomp` and accepted by `viprchk`). Note `viprchk` does not read gzip; the
uncompressed file is the checkable one.

Code is MIT; prose, tables and certificates are CC BY 4.0. Zenodo records one
licence field, which carries the code licence.

Source repository: <https://github.com/SeverinVisionary/oeis-a004045>
