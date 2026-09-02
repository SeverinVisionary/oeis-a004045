import Mcov.Basic
namespace Mcov
open Finset

/-! Independent sanity checks on the FORMALISATION ITSELF, written separately
    from the development, to rule out a vacuous or degenerate statement. -/

-- 1. The ambient space really is F_2^8 (256 words).
example : Fintype.card V = 256 := card_V

-- 2. IsDoubleCover is SATISFIABLE: the whole cube is one.
--    Without this the main theorem could be vacuously true.
theorem univ_isDoubleCover : IsDoubleCover (univ : Finset V) := by
  intro v
  have h9 : cov (univ : Finset V) v = 9 := by
    have hb := card_ball v
    unfold cov
    rw [show (univ.filter (fun c : V => dist c v ≤ 1))
          = (univ.filter (fun c : V => dist v c ≤ 1)) from by
        apply Finset.filter_congr; intro x _; rw [dist_comm]]
    exact hb
  omega

-- 3. IsDoubleCover is NON-TRIVIAL: the empty code is not one.
theorem empty_not_isDoubleCover : ¬ IsDoubleCover (∅ : Finset V) := by
  intro h; have := h ∅; simp [cov] at this

#check @no_60_word_double_cover
#print axioms no_60_word_double_cover
#print axioms univ_isDoubleCover
#print axioms empty_not_isDoubleCover
end Mcov
