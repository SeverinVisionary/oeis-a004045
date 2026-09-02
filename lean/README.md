# Lean formalisation of `K(8,1,2) >= 61`

**Status: 14 lemmas fully proved and axiom-audited. 3 `sorry`s remain.**

`lake build` succeeds. **Fourteen lemmas — including the entire Delsarte input —
are machine-verified**, each depending on only the three standard Lean axioms
`propext`, `Classical.choice`, `Quot.sound`, with **no `sorryAx`**. Verify this
yourself:

    lake build Mcov.Audit      # prints the axiom trace of every proved lemma

Proved: `sum_cov`, `chi_mul`, `a_even`, `excess_eq`, `sos_nonneg`,
`sos_eq_radial`, **`sum_chi_eq_f`**, `ball_sum_odd`, `exists_excess_in_ball`,
`card_le_excess`, `antipode_row`, `second_moment`, `layer_identity`,
`layer_identity_zero`.

Remaining (`no_60_word_double_cover` correctly still reports `sorryAx`):
`a12_lower`, `exists_full_ball`, `layer_contradiction` — the three deep steps.
Everything they need upstream is now proved, so they reduce to linear
arithmetic and integrality over `sum_d a_d = |C|^2`.

`sum_chi_eq_f` was proved by the **general Krawtchouk identity**, not by
computation and not by a 9-representative fallback: each `w` of card `k` splits
uniquely as `(w INTER u)` and `(w \ u)`, giving
`sum_j (-1)^j C(|u|,j) C(8-|u|,k-j)` via `Finset.card_nbij'`. So the design goal
holds — no MacWilliams duality or inversion is used anywhere.

`lake build` succeeds (3008 jobs): every definition and every theorem STATEMENT
elaborates, and the top-level derivation
`exists_full_ball -> layer_contradiction -> False` typechecks. So the shape of
the argument is machine-checked. Every leaf is still `sorry`, so the content is
not.

Toolchain note: Lean **4.33.1**. On 4.14 the prebuilt mathlib `cache` binary
will not run on macOS 15+/Darwin 25 (`dyld: __DATA_CONST segment missing
SG_READ_ONLY flag`). Also `Mathlib.Algebra.BigOperators.Basic` no longer exists;
it is now `Mathlib.Algebra.BigOperators.Group.Finset.Basic`.

## Why formalise this rather than send it for human review

The M=60 refutation has no slack anywhere. Step 2's value `347` is one unit
from collapse, and step 4 has `need = cap = 60` exactly, closed only by the
fact that 5 does not divide 12. Two independent machine reviews called it
sound, but between them they made four errors on this very argument (see the
git log) and caught *disjoint* defects — so their agreement is two partial
passes, not two confirmations. A referee will skim the arithmetic exactly as
they did. A proof assistant will not.

Formalisation settles **correctness**. It says nothing about **priority**, which
still needs a human who knows the literature.

## The design decision that makes this tractable

The informal proof invokes Delsarte/MacWilliams nonnegativity. Formalising
MacWilliams would be a large project on its own — and it is unnecessary. The
argument only ever uses that a particular quadratic form is a **sum of
squares**:

    0 <= sum_{w in W} ( sum_{x in C} chi_w(x) )^2 = sum_{x,z in C} f(d(x,z))

The left inequality is `Finset.sum_nonneg` applied to `sq_nonneg` — trivial.
The right equality needs only that `sum_{w in W} chi_w(u)` depends solely on
`|u|`, which is ONE finite computation. For `W = {w : |w| in {1,2,7,8}}`,

    f = [45, 13, 13, -3, -3, -3, -3, 13, 13]

verified combinatorially (`sum over w of (-1)^{|w cap u|}`) and against the
Krawtchouk expression. So the entire Delsarte input collapses to a `decide`.

The rest of step 2 is linear arithmetic:

    SOS >= 0          :  45a0 + 13(a1+a2) - 3(a3+..+a6) + 13(a7+a8) >= 0
    + 3 * (sum a_d = M^2 = 3600)
                      :  48a0 + 16(a1+a2) + 16(a7+a8) >= 10800
    /16               :   3a0 +   (a1+a2) +   (a7+a8) >= 675
    antipode row      :   a7+a8 <= 148
                      :   3a0 +   (a1+a2) >= 527
    a0 = 60           :          a1+a2    >= 347   (and even, so >= 348)

## MEASURED: `decide` is not viable for `sum_chi_eq_f` (2026-09-02)

The original plan was to discharge `sum_chi_eq_f` as one finite computation.
Measured on this machine, Lean 4.33.1:

| file | content | wall |
|---|---|---|
| `Probe3` | the same mathlib imports, `1 + 1 = 2` by `rfl` | **10 s** |
| `Probe` | one 256-term character sum, `Finset (Fin 8)`, by `decide` | **157 s** |
| `Probe2` | the same sum with a leaner `Fin 256` + bitwise encoding | **146 s** |

So the imports cost 10 s and a SINGLE `decide` costs ~136 s. The encoding is not
the bottleneck. `sum_chi_eq_f` quantifies over all 256 words, so brute force is
roughly **10 hours of kernel time** — not a proof anyone will re-run, and not
viable. Restricting to 9 weight-class representatives via a symmetry argument
would still be ~22 minutes and would need an `Equiv` for permutations of
`Fin 8` acting on `Finset (Fin 8)`.

**DONE — this is what was implemented, and it worked.** Note the measurement is
even stronger than first recorded: `decide` also fails on the NINE tiny
Krawtchouk cases (`interval_cases j <;> decide` exceeded a 10-minute cap),
because kernel evaluation of `Finset.sum` goes through `Multiset` quotients.
The rule is therefore: avoid kernel `decide` on ANY `Finset.sum`, not merely
large ones. `simp [Finset.sum_range_succ, Nat.choose, f]` closes all nine in
seconds.

**Plan that was executed: prove the Krawtchouk identity combinatorially.**

    sum_{|w| = k} (-1)^{|w cap u|}  =  sum_j (-1)^j C(|u|, j) C(n - |u|, k - j)
                                    =  K_k(|u|)

by splitting each `w` into `w cap u` (choose `j` from `u`) and `w \ u` (choose
`k - j` from the complement). This is one standard `Finset.sum` manipulation,
it is cheap for the kernel, and it gives the general statement rather than nine
special cases.

Note this does NOT reintroduce MacWilliams: we still never need duality or
inversion, only this single counting identity. The "avoid MacWilliams" design
survives; only the "one big `decide`" shortcut does not.

## Remaining obligations

Ordered by expected difficulty, hardest first:

| # | lemma | note |
|---|---|---|
| 1 | `sos_eq_radial` | expand the square, swap sums, apply `chi_mul` and `sum_chi_eq_f` |
| 2 | `layer_contradiction` | the Farkas certificate; needs the capacity `m 8 <= 1` |
| 3 | `exists_full_ball` | second moment + the integrality case split at `s = 16` |
| 4 | `ball_sum_odd` | ball-intersection sizes 9 / 2 / 2 / 0, then parity |
| 5 | `sum_chi_eq_f` | `decide` MEASURED NOT VIABLE (~10 h); prove the Krawtchouk identity by the split above |
| 6 | `antipode_row` | `u -> complement u` is a bijection |
| 7 | `layer_identity`, `sum_cov`, `chi_mul`, `a_even`, ... | routine counting |

## Build

    lake exe cache get && lake build
