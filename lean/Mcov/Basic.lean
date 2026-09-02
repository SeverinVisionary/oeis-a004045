/-
Formalisation of:  K(8,1,2) >= 61,  i.e. no 60-word double covering of Q_8.

A word is a subset of Fin 8 (positions carrying a 1); symmetric difference is
XOR and Hamming distance is the card of the symmetric difference.

DESIGN NOTE.  The informal proof invokes Delsarte/MacWilliams nonnegativity.
Formalising the MacWilliams identity would be a large project, and it is not
needed: the only thing used is that a particular quadratic form is a SUM OF
SQUARES.  Concretely, for a set W of "frequencies",

    0 <= sum_{w in W} ( sum_{x in C} chi w x )^2 = sum_{x,z in C} f (dist x z)

where f d = sum_{w in W} chi w u for any u of weight d.  Nonnegativity is then
`Finset.sum_nonneg` applied to squares, and the whole Delsarte input reduces to
ONE finite computation: the values of f.  For W = {w : w.card in {1,2,7,8}},

    f = ![45, 13, 13, -3, -3, -3, -3, 13, 13].

Everything else in the argument is elementary counting and integrality.
-/
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

open Finset BigOperators

namespace Mcov

/-- A word of the cube `Q_8`. -/
abbrev V : Type := Finset (Fin 8)

/-- Hamming distance. -/
def dist (x y : V) : ℕ := (symmDiff x y).card

/-- Number of codewords in the closed radius-1 ball around `v`. -/
def cov (C : Finset V) (v : V) : ℕ := (C.filter (fun c => dist c v ≤ 1)).card

/-- `C` covers every word of the cube at least twice. -/
def IsDoubleCover (C : Finset V) : Prop := ∀ v : V, 2 ≤ cov C v

/-- Excess at a word. -/
def g (C : Finset V) (v : V) : ℕ := cov C v - 2

/-- Total excess. -/
def E (C : Finset V) : ℕ := ∑ v : V, g C v

/-- The over-covered set. -/
def S (C : Finset V) : Finset V := univ.filter (fun v => 2 < cov C v)

/-- Ordered distance distribution. -/
def a (C : Finset V) (d : ℕ) : ℕ :=
  ((C ×ˢ C).filter (fun p => dist p.1 p.2 = d)).card

/-- Character. -/
def chi (w x : V) : ℤ := (-1) ^ ((w ∩ x).card)

/-- The frequency set used by the certificate. -/
def W : Finset V := univ.filter (fun w => w.card = 1 ∨ w.card = 2 ∨ w.card = 7 ∨ w.card = 8)

/-- The radial function `f` induced by `W`. -/
def f : ℕ → ℤ
  | 0 => 45 | 1 => 13 | 2 => 13 | 3 => -3 | 4 => -3
  | 5 => -3 | 6 => -3 | 7 => 13 | 8 => 13 | _ => 0

/-! ### Step 0 — total excess is determined by the cardinality -/

/-- Every word lies in exactly `9` balls, so `sum_v cov C v = 9 * |C|`. -/
theorem sum_cov (C : Finset V) : ∑ v : V, cov C v = 9 * C.card := by
  sorry

theorem excess_eq (C : Finset V) (h : IsDoubleCover C) :
    E C + 2 * 512 = 9 * C.card + 512 := by
  sorry

/-! ### Step 1 — the parity step: every codeword sees an over-covered word -/

/-- For `x` in `C`, `sum_{y in B(x)} cov C y = 9 + 2 * N_2(x)` is ODD. -/
theorem ball_sum_odd (C : Finset V) (x : V) (hx : x ∈ C) :
    Odd (∑ y : V, if dist x y ≤ 1 then cov C y else 0) := by
  sorry

/-- Hence some `y` in the ball of `x` is covered at least three times. -/
theorem exists_excess_in_ball (C : Finset V) (h : IsDoubleCover C) (x : V) (hx : x ∈ C) :
    ∃ y, dist x y ≤ 1 ∧ y ∈ S C := by
  sorry

/-- Incidence count: `|C| <= E + 2|S|`. -/
theorem card_le_excess (C : Finset V) (h : IsDoubleCover C) :
    C.card ≤ E C + 2 * (S C).card := by
  sorry

/-! ### Step 2 — the sum-of-squares certificate -/

/-- `chi w x * chi w z = chi w (x ∆ z)`, because `|w∩x| + |w∩z| ≡ |w ∩ (x∆z)| [MOD 2]`. -/
theorem chi_mul (w x z : V) : chi w x * chi w z = chi w (symmDiff x z) := by
  sorry

/-- THE ONE FINITE COMPUTATION.  For every `u`, `sum_{w in W} chi w u = f u.card`.
    Decidable: 256 words times 256 frequencies. -/
theorem sum_chi_eq_f (u : V) : ∑ w ∈ W, chi w u = f u.card := by
  sorry

/-- Nonnegativity, by `Finset.sum_nonneg` on squares.  This is the entire
    Delsarte input, and it is trivial. -/
theorem sos_nonneg (C : Finset V) : 0 ≤ ∑ w ∈ W, (∑ x ∈ C, chi w x) ^ 2 :=
  Finset.sum_nonneg fun _ _ => sq_nonneg _

/-- Expanding the square and applying `sum_chi_eq_f`. -/
theorem sos_eq_radial (C : Finset V) :
    ∑ w ∈ W, (∑ x ∈ C, chi w x) ^ 2 = ∑ d ∈ range 9, (a C d : ℤ) * f d := by
  sorry

/-- The antipode row: antipodes of NON-codewords are still doubly covered. -/
theorem antipode_row (C : Finset V) (h : IsDoubleCover C) :
    (a C 7 : ℤ) + a C 8 ≤ 9 * C.card - 2 * (256 - C.card) := by
  sorry

/-- Step 2's conclusion at `|C| = 60`.  Combines `sos_nonneg`, `sos_eq_radial`,
    `sum_{d} a_d = |C|^2` and `antipode_row`, all linearly. -/
theorem a12_lower (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60) :
    347 ≤ a C 1 + a C 2 := by
  sorry

/-- `a_1` and `a_2` are even: `(x,z)` and `(z,x)` are distinct ordered pairs. -/
theorem a_even (C : Finset V) (d : ℕ) (hd : d ≠ 0) : Even (a C d) := by
  sorry

/-! ### Steps 3-4 — second moment and integrality force a full ball -/

theorem second_moment (C : Finset V) :
    ∑ v : V, (cov C v : ℤ) ^ 2 = 9 * C.card + 2 * (a C 1 + a C 2) := by
  sorry

/-- With `|C| = 60`: `Q >= 100`, and integrality then forces a word covered `9` times. -/
theorem exists_full_ball (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60) :
    ∃ y : V, cov C y = 9 := by
  sorry

/-! ### Step 5 — the layer count, with capacities -/

/-- Layer sizes of a code containing the full ball around `0`. -/
def m (C : Finset V) (i : ℕ) : ℕ := (C.filter (fun c => c.card = i)).card

/-- The layer identity, for `1 <= i <= 8`.

    NOTE: the `i = 0` case must be stated separately.  With `i : ℕ`, `i - 1`
    truncates to `0`, so the uniform statement would read
    `m 0 + 9 * m 0 + m 1` at `i = 0`, which is FALSE — the true value there is
    `m 0 + m 1`.  Caught by a review leg; the original statement was
    unprovable as written. -/
theorem layer_identity (C : Finset V) (i : ℕ) (hi1 : 1 ≤ i) (hi : i ≤ 8) :
    ∑ v ∈ univ.filter (fun v : V => v.card = i), cov C v
      = m C i + (9 - i) * m C (i - 1) + (i + 1) * m C (i + 1) := by
  sorry

/-- The `i = 0` case: the only weight-0 word is `∅`, covered by itself and by
    every weight-1 codeword. -/
theorem layer_identity_zero (C : Finset V) :
    ∑ v ∈ univ.filter (fun v : V => v.card = 0), cov C v = m C 0 + m C 1 := by
  sorry

/-- The Farkas certificate, with weights `w = (0,0,0,8,8,2,2,17,17)`:
    weighted demand is `2658`, but the nine words of the full ball contribute
    nothing and the remaining `51` contribute at most `50*48 + 153 = 2553`.
    The capacity `m 8 <= 1` is essential and is what makes `153` appear once. -/
theorem layer_contradiction (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60)
    (y : V) (hy : cov C y = 9) : False := by
  sorry

/-! ### Main theorem -/

theorem no_60_word_double_cover (C : Finset V) (h : IsDoubleCover C) : C.card ≠ 60 := by
  intro hc
  obtain ⟨y, hy⟩ := exists_full_ball C h hc
  exact layer_contradiction C h hc y hy

end Mcov
