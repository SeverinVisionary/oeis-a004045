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

/-! ### Elementary helpers: distance, the radius-1 ball, parity -/

lemma even_card_of_involution {α : Type*} (s : Finset α) (g : α → α)
    (hmem : ∀ x ∈ s, g x ∈ s) (hinv : ∀ x ∈ s, g (g x) = x) (hne : ∀ x ∈ s, g x ≠ x) :
    Even s.card := by
  have key : ∑ _x ∈ s, (1 : ZMod 2) = 0 :=
    Finset.sum_involution (fun x _ => g x) (fun _ _ => by decide)
      (fun x hx _ => hne x hx) (fun x hx => hmem x hx) (fun x hx => hinv x hx)
  rw [Finset.sum_const, nsmul_eq_mul, mul_one] at key
  exact ZMod.natCast_eq_zero_iff_even.mp key

lemma dist_self (x : V) : dist x x = 0 := by simp [dist]

lemma dist_comm (x y : V) : dist x y = dist y x := by
  simp [dist, symmDiff_comm]

lemma dist_le_eight (x y : V) : dist x y ≤ 8 := by
  have := Finset.card_le_univ (symmDiff x y)
  simpa [dist, Fintype.card_fin] using this

lemma dist_eq_zero_iff (x y : V) : dist x y = 0 ↔ x = y := by
  rw [dist, Finset.card_eq_zero]
  exact symmDiff_eq_bot

lemma card_V : Fintype.card V = 256 := by
  rw [Fintype.card_finset, Fintype.card_fin]; norm_num

def ballPt (c : V) : Option (Fin 8) → V
  | none => c
  | some k => symmDiff c {k}

@[simp] lemma ballPt_none (c : V) : ballPt c none = c := rfl
@[simp] lemma ballPt_some (c : V) (k : Fin 8) : ballPt c (some k) = symmDiff c {k} := rfl

lemma card_ball_filter (c : V) (P : V → Prop) [DecidablePred P] :
    (univ.filter (fun v : V => dist c v ≤ 1 ∧ P v)).card
      = (if P c then 1 else 0) + (univ.filter (fun k : Fin 8 => P (symmDiff c {k}))).card := by
  have hb : (univ.filter (fun o => P (ballPt c o))).card
      = (univ.filter (fun v : V => dist c v ≤ 1 ∧ P v)).card := by
    apply Finset.card_bij (fun o _ => ballPt c o)
    · intro o ho
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at ho ⊢
      refine ⟨?_, ho⟩
      cases o with
      | none => simp [dist]
      | some k => simp [dist]
    · intro o₁ _ o₂ _ h
      cases o₁ with
      | none =>
        cases o₂ with
        | none => rfl
        | some k =>
          exfalso
          simp only [ballPt_none, ballPt_some] at h
          have := symmDiff_eq_left.mp h.symm
          simp at this
      | some k =>
        cases o₂ with
        | none =>
          exfalso
          simp only [ballPt_none, ballPt_some] at h
          have := symmDiff_eq_left.mp h
          simp at this
        | some k' =>
          simp only [ballPt_some] at h
          rw [symmDiff_right_inj, Finset.singleton_inj] at h
          rw [h]
    · intro v hv
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hv
      obtain ⟨hd, hP⟩ := hv
      rw [dist] at hd
      have h01 : (symmDiff c v).card = 0 ∨ (symmDiff c v).card = 1 := by omega
      rcases h01 with h0 | h1
      · rw [Finset.card_eq_zero] at h0
        have hcv : c = v := symmDiff_eq_bot.mp h0
        subst hcv
        exact ⟨none, by simpa using hP, rfl⟩
      · obtain ⟨k, hk⟩ := Finset.card_eq_one.mp h1
        have hv' : v = symmDiff c {k} := by
          rw [← hk, symmDiff_symmDiff_cancel_left]
        subst hv'
        exact ⟨some k, by simpa using hP, rfl⟩
  rw [← hb, Finset.card_filter, Fintype.sum_option, Finset.card_filter]
  rfl

lemma card_ball (c : V) : (univ.filter (fun v : V => dist c v ≤ 1)).card = 9 := by
  have := card_ball_filter c (fun _ => True)
  simp only [and_true, if_true, Finset.filter_true, Finset.card_univ, Fintype.card_fin] at this
  exact this

lemma sum_cov_filter (C : Finset V) (P : V → Prop) [DecidablePred P] :
    ∑ v ∈ univ.filter P, cov C v
      = ∑ c ∈ C, (univ.filter (fun v : V => dist c v ≤ 1 ∧ P v)).card := by
  simp_rw [cov, Finset.card_filter]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro c _
  rw [← Finset.card_filter, Finset.filter_filter]
  have : univ.filter (fun v : V => P v ∧ dist c v ≤ 1)
      = univ.filter (fun v : V => dist c v ≤ 1 ∧ P v) :=
    Finset.filter_congr (fun v _ => and_comm)
  rw [this, Finset.card_filter]

lemma card_symmDiff_singleton (c : V) (k : Fin 8) :
    (symmDiff c {k}).card = if k ∈ c then c.card - 1 else c.card + 1 := by
  split_ifs with hk
  · have : symmDiff c {k} = c.erase k := by
      ext i; simp only [Finset.mem_symmDiff, Finset.mem_singleton, Finset.mem_erase]
      constructor
      · rintro (⟨hi, hne⟩ | ⟨rfl, hc⟩)
        · exact ⟨hne, hi⟩
        · exact absurd hk hc
      · rintro ⟨hne, hi⟩; exact Or.inl ⟨hi, hne⟩
    rw [this, Finset.card_erase_of_mem hk]
  · have : symmDiff c {k} = insert k c := by
      ext i; simp only [Finset.mem_symmDiff, Finset.mem_singleton, Finset.mem_insert]
      constructor
      · rintro (⟨hi, _⟩ | ⟨rfl, _⟩)
        · exact Or.inr hi
        · exact Or.inl rfl
      · rintro (rfl | hi)
        · exact Or.inr ⟨rfl, hk⟩
        · exact Or.inl ⟨hi, fun h => hk (h ▸ hi)⟩
    rw [this, Finset.card_insert_of_notMem hk]

lemma card_filter_symmDiff_singleton (c : V) (Q : ℕ → Prop) [DecidablePred Q] :
    (univ.filter (fun k : Fin 8 => Q (symmDiff c {k}).card)).card
      = (if Q (c.card - 1) then c.card else 0) + (if Q (c.card + 1) then 8 - c.card else 0) := by
  rw [Finset.card_filter, ← Finset.sum_add_sum_compl c]
  congr 1
  · rw [Finset.sum_congr rfl (fun k hk => by rw [card_symmDiff_singleton, if_pos hk])]
    split_ifs <;> simp
  · rw [Finset.sum_congr rfl (fun k hk => by
      rw [card_symmDiff_singleton, if_neg (Finset.mem_compl.mp hk)])]
    split_ifs <;> simp [Finset.card_compl, Fintype.card_fin]

lemma dist_compl (x z : V) : dist z xᶜ = 8 - dist x z := by
  have e : symmDiff z xᶜ = (symmDiff x z)ᶜ := by
    ext i; simp only [Finset.mem_symmDiff, Finset.mem_compl]; tauto
  rw [dist, dist, e, Finset.card_compl, Fintype.card_fin]

lemma card_le_eight (v : V) : v.card ≤ 8 := by
  have := Finset.card_le_univ v
  simpa [Fintype.card_fin] using this

lemma cov_le_nine (C : Finset V) (v : V) : cov C v ≤ 9 := by
  have hsub : C.filter (fun c => dist c v ≤ 1) ⊆ univ.filter (fun c : V => dist v c ≤ 1) := by
    intro c hc
    rw [Finset.mem_filter] at hc ⊢
    exact ⟨Finset.mem_univ _, by rw [dist_comm]; exact hc.2⟩
  have := Finset.card_le_card hsub
  rw [card_ball v] at this
  exact this

lemma dist_empty (c : V) : dist c ∅ = c.card := by
  have : symmDiff c ∅ = c := by ext i; simp [Finset.mem_symmDiff]
  rw [dist, this]

lemma dist_symmDiff_right (c v t : V) : dist (symmDiff c t) (symmDiff v t) = dist c v := by
  rw [dist, dist, symmDiff_symmDiff_symmDiff_comm, symmDiff_self, symmDiff_bot]

/-! ### Step 0 — total excess is determined by the cardinality -/

/-- Every word lies in exactly `9` balls, so `sum_v cov C v = 9 * |C|`. -/
theorem sum_cov (C : Finset V) : ∑ v : V, cov C v = 9 * C.card := by
  have h1 : ∀ v, cov C v = ∑ c ∈ C, if dist c v ≤ 1 then 1 else 0 := by
    intro v; rw [cov, Finset.card_filter]
  simp_rw [h1]
  rw [Finset.sum_comm]
  have h2 : ∀ c, (∑ v : V, if dist c v ≤ 1 then 1 else 0) = 9 := by
    intro c; rw [← Finset.card_filter]; exact card_ball c
  simp_rw [h2]
  rw [Finset.sum_const, smul_eq_mul, mul_comm]

theorem excess_eq (C : Finset V) (h : IsDoubleCover C) :
    E C + 2 * 512 = 9 * C.card + 512 := by
  have h1 : ∑ v : V, (cov C v - 2) + ∑ _v : V, (2 : ℕ) = ∑ v : V, cov C v := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro v _
    have := h v; omega
  have h2 : ∑ _v : V, (2 : ℕ) = 512 := by
    rw [Finset.sum_const, Finset.card_univ, card_V]; rfl
  rw [sum_cov, h2] at h1
  unfold E g
  omega

/-! ### Step 1 — the parity step: every codeword sees an over-covered word -/

/-- For `x` in `C`, `sum_{y in B(x)} cov C y = 9 + 2 * N_2(x)` is ODD. -/
theorem ball_sum_odd (C : Finset V) (x : V) (hx : x ∈ C) :
    Odd (∑ y : V, if dist x y ≤ 1 then cov C y else 0) := by
  rw [← Finset.sum_filter, sum_cov_filter, ← Finset.add_sum_erase C _ hx]
  have h9 : (univ.filter (fun y : V => dist x y ≤ 1 ∧ dist x y ≤ 1)).card = 9 := by
    simp only [and_self]; exact card_ball x
  rw [h9]
  apply Odd.add_even (by decide)
  apply Finset.even_sum
  intro c hc
  have hcx : c ≠ x := Finset.ne_of_mem_erase hc
  apply even_card_of_involution _ (fun y => symmDiff (symmDiff x c) y)
  · intro y hy
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hy ⊢
    have e1 : symmDiff c (symmDiff (symmDiff x c) y) = symmDiff x y := by
      rw [symmDiff_comm x c, symmDiff_assoc, symmDiff_symmDiff_cancel_left]
    have e2 : symmDiff x (symmDiff (symmDiff x c) y) = symmDiff c y := by
      rw [symmDiff_assoc, symmDiff_symmDiff_cancel_left]
    simp only [dist] at hy ⊢
    rw [e1, e2]
    exact ⟨hy.2, hy.1⟩
  · intro y _; exact symmDiff_symmDiff_cancel_left _ _
  · intro y _ h
    apply hcx
    exact (symmDiff_eq_bot.mp (symmDiff_eq_right.mp h)).symm

/-- Hence some `y` in the ball of `x` is covered at least three times. -/
theorem exists_excess_in_ball (C : Finset V) (h : IsDoubleCover C) (x : V) (hx : x ∈ C) :
    ∃ y, dist x y ≤ 1 ∧ y ∈ S C := by
  by_contra hcon
  have h2 : ∀ y, dist x y ≤ 1 → cov C y = 2 := by
    intro y hy
    have h1 := h y
    have h3 : y ∉ S C := fun hS => hcon ⟨y, hy, hS⟩
    simp only [S, Finset.mem_filter, Finset.mem_univ, true_and, not_lt] at h3
    omega
  have hodd := ball_sum_odd C x hx
  have h18 : (∑ y : V, if dist x y ≤ 1 then cov C y else 0) = 18 := by
    rw [← Finset.sum_filter,
      Finset.sum_congr rfl (fun y hy => h2 y (Finset.mem_filter.mp hy).2),
      Finset.sum_const, card_ball, smul_eq_mul]
  rw [h18, Nat.odd_iff] at hodd
  omega

/-- Incidence count: `|C| <= E + 2|S|`. -/
theorem card_le_excess (C : Finset V) (h : IsDoubleCover C) :
    C.card ≤ E C + 2 * (S C).card := by
  have h1 : C ⊆ (S C).biUnion (fun y => C.filter (fun c => dist c y ≤ 1)) := by
    intro x hx
    obtain ⟨y, hy, hyS⟩ := exists_excess_in_ball C h x hx
    rw [Finset.mem_biUnion]
    exact ⟨y, hyS, Finset.mem_filter.mpr ⟨hx, hy⟩⟩
  have h2 : C.card ≤ ∑ y ∈ S C, cov C y :=
    (Finset.card_le_card h1).trans Finset.card_biUnion_le
  have h3 : ∑ y ∈ S C, cov C y = ∑ y ∈ S C, g C y + 2 * (S C).card := by
    rw [Finset.sum_congr rfl (fun y _ => (show cov C y = g C y + 2 by
        unfold g; have := h y; omega)),
      Finset.sum_add_distrib, Finset.sum_const, smul_eq_mul, mul_comm]
  have h4 : ∑ y ∈ S C, g C y ≤ E C :=
    Finset.sum_le_sum_of_subset (Finset.subset_univ _)
  omega

/-! ### Step 2 — the sum-of-squares certificate -/

/-- `chi w x * chi w z = chi w (x ∆ z)`, because `|w∩x| + |w∩z| ≡ |w ∩ (x∆z)| [MOD 2]`. -/
theorem chi_mul (w x z : V) : chi w x * chi w z = chi w (symmDiff x z) := by
  unfold chi
  have h : w ∩ symmDiff x z = symmDiff (w ∩ x) (w ∩ z) := by
    ext i; simp only [Finset.mem_inter, Finset.mem_symmDiff]; tauto
  rw [h, ← pow_add]
  set s := w ∩ x
  set t := w ∩ z
  have h3 : symmDiff s t = s \ t ∪ t \ s := by
    ext i; simp only [Finset.mem_symmDiff, Finset.mem_union, Finset.mem_sdiff]
  have hcard : s.card + t.card = (symmDiff s t).card + 2 * (s ∩ t).card := by
    have h1 := Finset.card_sdiff_add_card_inter s t
    have h2 := Finset.card_sdiff_add_card_inter t s
    rw [Finset.inter_comm] at h2
    rw [h3, Finset.card_union_of_disjoint disjoint_sdiff_sdiff]
    omega
  rw [hcard, pow_add, pow_mul]
  simp

/-! #### The Krawtchouk computation behind `sum_chi_eq_f` -/

lemma card_fiber (u : V) (k i : ℕ) (hik : i ≤ k) :
    ((powersetCard k (univ : Finset (Fin 8))).filter (fun w => (w ∩ u).card = i)).card
      = u.card.choose i * (8 - u.card).choose (k - i) := by
  have hc : (uᶜ : Finset (Fin 8)).card = 8 - u.card := by
    rw [Finset.card_compl, Fintype.card_fin]
  rw [← hc, ← Finset.card_powersetCard, ← Finset.card_powersetCard, ← Finset.card_product]
  apply Finset.card_nbij' (fun w => (w ∩ u, w \ u)) (fun p => p.1 ∪ p.2)
  · intro w hw
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_powersetCard, Finset.subset_univ,
      true_and] at hw
    simp only [Finset.mem_coe, Finset.mem_product, Finset.mem_powersetCard]
    refine ⟨⟨Finset.inter_subset_right, hw.2⟩, ?_, ?_⟩
    · intro x hx; rw [Finset.mem_compl]; exact (Finset.mem_sdiff.mp hx).2
    · have := Finset.card_sdiff_add_card_inter w u; omega
  · intro p hp
    simp only [Finset.mem_coe, Finset.mem_product, Finset.mem_powersetCard] at hp
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_powersetCard, Finset.subset_univ,
      true_and]
    obtain ⟨⟨h1, h1c⟩, ⟨h2, h2c⟩⟩ := hp
    have hdisj : Disjoint p.1 p.2 := by
      rw [Finset.disjoint_left]; intro x hx1 hx2
      exact (Finset.mem_compl.mp (h2 hx2)) (h1 hx1)
    have hinter : (p.1 ∪ p.2) ∩ u = p.1 := by
      ext x; simp only [Finset.mem_inter, Finset.mem_union]
      constructor
      · rintro ⟨hx | hx, hxu⟩
        · exact hx
        · exact absurd hxu (Finset.mem_compl.mp (h2 hx))
      · intro hx; exact ⟨Or.inl hx, h1 hx⟩
    rw [Finset.card_union_of_disjoint hdisj, hinter]
    omega
  · intro w _
    ext x; simp only [Finset.mem_union, Finset.mem_inter, Finset.mem_sdiff]; tauto
  · intro p hp
    simp only [Finset.mem_coe, Finset.mem_product, Finset.mem_powersetCard] at hp
    obtain ⟨⟨h1, _⟩, ⟨h2, _⟩⟩ := hp
    have h2' : ∀ x ∈ p.2, x ∉ u := fun x hx => Finset.mem_compl.mp (h2 hx)
    ext1
    · ext x; simp only [Finset.mem_inter, Finset.mem_union]
      constructor
      · rintro ⟨hx | hx, hxu⟩
        · exact hx
        · exact absurd hxu (h2' x hx)
      · intro hx; exact ⟨Or.inl hx, h1 hx⟩
    · ext x; simp only [Finset.mem_sdiff, Finset.mem_union]
      constructor
      · rintro ⟨hx | hx, hxu⟩
        · exact absurd (h1 hx) hxu
        · exact hx
      · intro hx; exact ⟨Or.inr hx, h2' x hx⟩

lemma sum_powersetCard_chi (u : V) (k : ℕ) :
    ∑ w ∈ powersetCard k (univ : Finset (Fin 8)), chi w u
      = ∑ i ∈ range (k+1),
          ((u.card.choose i * (8 - u.card).choose (k - i) : ℕ) : ℤ) * (-1) ^ i := by
  rw [← Finset.sum_fiberwise_of_maps_to (g := fun w => (w ∩ u).card) (t := range (k+1))]
  · apply Finset.sum_congr rfl
    intro i hi
    rw [Finset.mem_range] at hi
    have : ∀ w ∈ (powersetCard k (univ : Finset (Fin 8))).filter (fun w => (w ∩ u).card = i),
        chi w u = (-1) ^ i := by
      intro w hw; rw [chi, (Finset.mem_filter.mp hw).2]
    rw [Finset.sum_congr rfl this, Finset.sum_const, card_fiber u k i (by omega), nsmul_eq_mul]
  · intro w hw
    rw [Finset.mem_range]
    have h1 := (Finset.mem_powersetCard.mp hw).2
    have h2 := Finset.card_le_card (Finset.inter_subset_left : w ∩ u ⊆ w)
    omega

lemma W_filter (k : ℕ) (hk : k = 1 ∨ k = 2 ∨ k = 7 ∨ k = 8) :
    W.filter (fun w => w.card = k) = powersetCard k univ := by
  ext w
  simp only [W, Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_powersetCard,
    Finset.subset_univ]
  constructor
  · rintro ⟨_, h⟩; exact h
  · intro h; exact ⟨by omega, h⟩

lemma krawtchouk_eval (j : ℕ) (hj : j ≤ 8) :
    ∑ k ∈ ({1, 2, 7, 8} : Finset ℕ), ∑ i ∈ range (k+1),
        ((j.choose i * (8 - j).choose (k - i) : ℕ) : ℤ) * (-1) ^ i = f j := by
  interval_cases j <;> simp [Finset.sum_range_succ, Nat.choose, f]

/-- THE ONE FINITE COMPUTATION.  For every `u`, `sum_{w in W} chi w u = f u.card`.
    Decidable: 256 words times 256 frequencies. -/
theorem sum_chi_eq_f (u : V) : ∑ w ∈ W, chi w u = f u.card := by
  have hu : u.card ≤ 8 := by
    have := Finset.card_le_univ u; simpa [Fintype.card_fin] using this
  rw [← Finset.sum_fiberwise_of_maps_to (g := fun w : V => w.card)
    (t := ({1, 2, 7, 8} : Finset ℕ)) ?_]
  · rw [Finset.sum_congr rfl (fun k hk => by
      rw [W_filter k (by simpa using hk), sum_powersetCard_chi])]
    exact krawtchouk_eval u.card hu
  · intro w hw
    simp only [W, Finset.mem_filter, Finset.mem_univ, true_and] at hw
    simp only [Finset.mem_insert, Finset.mem_singleton]
    exact hw

/-- Nonnegativity, by `Finset.sum_nonneg` on squares.  This is the entire
    Delsarte input, and it is trivial. -/
theorem sos_nonneg (C : Finset V) : 0 ≤ ∑ w ∈ W, (∑ x ∈ C, chi w x) ^ 2 :=
  Finset.sum_nonneg fun _ _ => sq_nonneg _

/-- Expanding the square and applying `sum_chi_eq_f`. -/
theorem sos_eq_radial (C : Finset V) :
    ∑ w ∈ W, (∑ x ∈ C, chi w x) ^ 2 = ∑ d ∈ range 9, (a C d : ℤ) * f d := by
  have h1 : ∀ w, (∑ x ∈ C, chi w x) ^ 2 = ∑ x ∈ C, ∑ z ∈ C, chi w (symmDiff x z) := by
    intro w; rw [sq, Finset.sum_mul_sum]; simp_rw [chi_mul]
  have h2 : ∑ w ∈ W, (∑ x ∈ C, chi w x) ^ 2 = ∑ p ∈ C ×ˢ C, f (dist p.1 p.2) := by
    simp_rw [h1]
    rw [Finset.sum_comm, Finset.sum_product]
    apply Finset.sum_congr rfl
    intro x _
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro z _
    rw [sum_chi_eq_f]; rfl
  rw [h2, ← Finset.sum_fiberwise_of_maps_to (g := fun p : V × V => dist p.1 p.2)
    (t := range 9) ?_]
  · apply Finset.sum_congr rfl
    intro d _
    rw [Finset.sum_congr rfl (fun p hp => by rw [(Finset.mem_filter.mp hp).2]),
      Finset.sum_const, nsmul_eq_mul, a]
  · intro p _
    rw [Finset.mem_range]
    have := dist_le_eight p.1 p.2
    omega

/-- The antipode row: antipodes of NON-codewords are still doubly covered. -/
theorem antipode_row (C : Finset V) (h : IsDoubleCover C) :
    (a C 7 : ℤ) + a C 8 ≤ 9 * C.card - 2 * (256 - C.card) := by
  have hA : a C 7 + a C 8 = ∑ x ∈ C, cov C xᶜ := by
    unfold a
    rw [← Finset.card_union_of_disjoint, ← Finset.filter_or, Finset.card_filter,
      Finset.sum_product]
    · apply Finset.sum_congr rfl
      intro x _
      rw [← Finset.card_filter, cov]
      congr 1
      apply Finset.filter_congr
      intro z _
      dsimp only
      rw [dist_compl x z]
      have := dist_le_eight x z
      omega
    · rw [Finset.disjoint_filter]; intro p _ h7 h8; omega
  have hinj : ∀ x ∈ C, ∀ y ∈ C, xᶜ = yᶜ → x = y := fun x _ y _ hxy => compl_injective hxy
  have hsum : ∑ x ∈ C, cov C xᶜ + ∑ v ∈ (C.image compl)ᶜ, cov C v = 9 * C.card := by
    rw [← sum_cov C, ← Finset.sum_add_sum_compl (C.image compl), Finset.sum_image hinj]
  have hcardA : ((C.image compl)ᶜ).card = 256 - C.card := by
    rw [Finset.card_compl, card_V, Finset.card_image_of_injective _ compl_injective]
  have hlow : 2 * (256 - C.card) ≤ ∑ v ∈ (C.image compl)ᶜ, cov C v := by
    have := Finset.sum_le_sum (fun v (_ : v ∈ (C.image compl)ᶜ) => h v)
    rw [Finset.sum_const, smul_eq_mul, hcardA] at this
    linarith
  have hC : C.card ≤ 256 := by
    have := Finset.card_le_univ C; rwa [card_V] at this
  omega

lemma a_zero (C : Finset V) : a C 0 = C.card := by
  unfold a
  apply Finset.card_nbij' (fun p => p.1) (fun c => (c, c))
  · intro p hp
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_product] at hp ⊢
    exact hp.1.1
  · intro c hc
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_product] at hc ⊢
    exact ⟨⟨hc, hc⟩, dist_self c⟩
  · intro p hp
    simp only [Finset.mem_coe, Finset.mem_filter, Finset.mem_product] at hp
    have := (dist_eq_zero_iff _ _).mp hp.2
    ext <;> simp [this]
  · intro c _; rfl

/-- The distance distribution sums to `|C|^2`: partition `C ×ˢ C` by distance. -/
lemma sum_a_eq_card_sq (C : Finset V) : ∑ d ∈ range 9, a C d = C.card * C.card := by
  symm
  rw [← Finset.card_product,
    Finset.card_eq_sum_card_fiberwise (f := fun p : V × V => dist p.1 p.2) (s := C ×ˢ C)
      (t := range 9) ?_]
  · rfl
  · intro p _
    simp only [Finset.mem_coe, Finset.mem_range]
    have := dist_le_eight p.1 p.2
    omega

/-- Step 2's conclusion at `|C| = 60`.  Combines `sos_nonneg`, `sos_eq_radial`,
    `sum_{d} a_d = |C|^2` and `antipode_row`, all linearly. -/
theorem a12_lower (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60) :
    347 ≤ a C 1 + a C 2 := by
  have h1 := sos_nonneg C
  rw [sos_eq_radial] at h1
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, f, zero_add] at h1
  have h2 : ((∑ d ∈ range 9, a C d : ℕ) : ℤ) = 3600 := by
    rw [sum_a_eq_card_sq, hc]; norm_num
  push_cast [Finset.sum_range_succ, Finset.sum_range_zero] at h2
  have h3 := antipode_row C h
  rw [hc] at h3
  norm_num at h3
  have h4' : a C 0 = 60 := by rw [a_zero, hc]
  have h4 : (a C 0 : ℤ) = 60 := by exact_mod_cast h4'
  have h5 : (347 : ℤ) ≤ a C 1 + a C 2 := by linarith
  exact_mod_cast h5

/-- `a_1` and `a_2` are even: `(x,z)` and `(z,x)` are distinct ordered pairs. -/
theorem a_even (C : Finset V) (d : ℕ) (hd : d ≠ 0) : Even (a C d) := by
  unfold a
  apply even_card_of_involution _ Prod.swap
  · intro p hp
    simp only [Finset.mem_filter, Finset.mem_product, Prod.fst_swap, Prod.snd_swap] at hp ⊢
    exact ⟨⟨hp.1.2, hp.1.1⟩, by rw [dist_comm]; exact hp.2⟩
  · intro p _; simp
  · intro p hp h
    simp only [Finset.mem_filter, Finset.mem_product] at hp
    have h1 : p.1 = p.2 := by
      have := congrArg Prod.fst h; simpa using this.symm
    apply hd
    rw [← hp.2, h1, dist_self]

/-! ### Steps 3-4 — second moment and integrality force a full ball -/

def hval (n : ℕ) : ℕ :=
  (if n ≤ 1 then 1 else 0) + ((if n - 1 ≤ 1 then n else 0) + (if n + 1 ≤ 1 then 8 - n else 0))

lemma cov_mul_cov (C : Finset V) (v : V) :
    cov C v * cov C v
      = ∑ p ∈ C ×ˢ C, if dist p.1 v ≤ 1 ∧ dist p.2 v ≤ 1 then 1 else 0 := by
  rw [cov, Finset.card_filter, Finset.sum_mul_sum, Finset.sum_product]
  apply Finset.sum_congr rfl; intro c _
  apply Finset.sum_congr rfl; intro c' _
  by_cases h1 : dist c v ≤ 1 <;> by_cases h2 : dist c' v ≤ 1 <;> simp [h1, h2]

lemma card_ball_inter (p : V × V) :
    (∑ v : V, if dist p.1 v ≤ 1 ∧ dist p.2 v ≤ 1 then 1 else 0) = hval (dist p.1 p.2) := by
  rw [← Finset.card_filter, card_ball_filter p.1 (fun v => dist p.2 v ≤ 1)]
  have e : ∀ k, dist p.2 (symmDiff p.1 {k}) = (symmDiff (symmDiff p.2 p.1) {k}).card := by
    intro k; rw [dist, symmDiff_assoc]
  simp_rw [e]
  rw [card_filter_symmDiff_singleton (symmDiff p.2 p.1) (fun n => n ≤ 1), dist_comm p.1 p.2]
  rfl

theorem second_moment_nat (C : Finset V) :
    ∑ v : V, cov C v * cov C v = 9 * C.card + 2 * (a C 1 + a C 2) := by
  simp_rw [cov_mul_cov]
  rw [Finset.sum_comm]
  simp_rw [card_ball_inter]
  rw [← Finset.sum_fiberwise_of_maps_to (g := fun p : V × V => dist p.1 p.2) (t := range 9)
    (fun p _ => by rw [Finset.mem_range]; have := dist_le_eight p.1 p.2; omega)]
  have hd : ∀ d ∈ range 9,
      ∑ p ∈ (C ×ˢ C).filter (fun p => dist p.1 p.2 = d), hval (dist p.1 p.2) = a C d * hval d := by
    intro d _
    rw [Finset.sum_congr rfl (fun p hp => by rw [(Finset.mem_filter.mp hp).2]),
      Finset.sum_const, smul_eq_mul, a]
  rw [Finset.sum_congr rfl hd]
  simp [Finset.sum_range_succ, hval, a_zero]
  ring

theorem second_moment (C : Finset V) :
    ∑ v : V, (cov C v : ℤ) ^ 2 = 9 * C.card + 2 * (a C 1 + a C 2) := by
  have h := second_moment_nat C
  have h2 : ∑ v : V, (cov C v : ℤ) ^ 2 = ((∑ v : V, cov C v * cov C v : ℕ) : ℤ) := by
    push_cast; simp [sq]
  rw [h2, h]; push_cast; ring

/-- Integer-valued excess `cov - 2` (no ℕ-truncation). -/
def gz (C : Finset V) (v : V) : ℤ := (cov C v : ℤ) - 2

lemma gz_sum (C : Finset V) : ∑ v : V, gz C v = 9 * C.card - 512 := by
  unfold gz
  rw [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, card_V, nsmul_eq_mul]
  have h2 : ∑ v : V, (cov C v : ℤ) = 9 * C.card := by exact_mod_cast sum_cov C
  rw [h2]; push_cast; ring

lemma gz_sq_sum (C : Finset V) :
    ∑ v : V, gz C v ^ 2 = 2 * (a C 1 + a C 2) - 27 * C.card + 1024 := by
  have h1 : ∀ v, gz C v ^ 2 = (cov C v : ℤ) ^ 2 - 4 * (cov C v : ℤ) + 4 := fun v => by
    unfold gz; ring
  simp_rw [h1]
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_const,
    Finset.card_univ, card_V, nsmul_eq_mul, second_moment]
  have h2 : ∑ v : V, (cov C v : ℤ) = 9 * C.card := by exact_mod_cast sum_cov C
  rw [h2]; push_cast; ring

/-- With `|C| = 60`: `Q >= 100`, and integrality then forces a word covered `9` times. -/
theorem exists_full_ball (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60) :
    ∃ y : V, cov C y = 9 := by
  by_contra hcon
  have hcon' : ∀ y, cov C y ≠ 9 := fun y hy => hcon ⟨y, hy⟩
  have hle : ∀ v, cov C v ≤ 8 := fun v => by
    have h1 := cov_le_nine C v; have h2 := hcon' v; omega
  have hE : E C = 28 := by have := excess_eq C h; omega
  have hs : 16 ≤ (S C).card := by have := card_le_excess C h; omega
  have ha : 348 ≤ a C 1 + a C 2 := by
    have h1 := a12_lower C h hc
    obtain ⟨k1, hk1⟩ := a_even C 1 one_ne_zero
    obtain ⟨k2, hk2⟩ := a_even C 2 two_ne_zero
    omega
  have hgz_zero : ∀ v, v ∉ S C → gz C v = 0 := fun v hv => by
    simp only [S, Finset.mem_filter, Finset.mem_univ, true_and, not_lt] at hv
    have := h v; unfold gz; omega
  have hgz_pos : ∀ v ∈ S C, 1 ≤ gz C v := fun v hv => by
    simp only [S, Finset.mem_filter, Finset.mem_univ, true_and] at hv
    unfold gz; omega
  have hgz_le : ∀ v, gz C v ≤ 6 := fun v => by have := hle v; unfold gz; omega
  have hS1 : ∑ v ∈ S C, gz C v = 28 := by
    rw [Finset.sum_subset (Finset.subset_univ _) (fun v _ hv => hgz_zero v hv), gz_sum, hc]
    norm_num
  have hS2 : 100 ≤ ∑ v ∈ S C, gz C v ^ 2 := by
    rw [Finset.sum_subset (Finset.subset_univ _) (fun v _ hv => by rw [hgz_zero v hv]; norm_num),
      gz_sq_sum, hc]
    have : (348 : ℤ) ≤ a C 1 + a C 2 := by exact_mod_cast ha
    push_cast
    linarith
  have hnn : ∀ v ∈ S C, 0 ≤ (gz C v - 1) * (6 - gz C v) := fun v hv =>
    mul_nonneg (by linarith [hgz_pos v hv]) (by linarith [hgz_le v])
  have hT : 0 ≤ ∑ v ∈ S C, (gz C v - 1) * (6 - gz C v) := Finset.sum_nonneg hnn
  have hT_eq : ∑ v ∈ S C, (gz C v - 1) * (6 - gz C v)
      = 7 * ∑ v ∈ S C, gz C v - ∑ v ∈ S C, gz C v ^ 2 - 6 * (S C).card := by
    rw [Finset.mul_sum, ← Finset.sum_sub_distrib,
      show (6 : ℤ) * (S C).card = ∑ v ∈ S C, (6 : ℤ) by
        rw [Finset.sum_const, nsmul_eq_mul, mul_comm],
      ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro v _; ring
  have hs' : (16 : ℤ) ≤ (S C).card := by exact_mod_cast hs
  have hT0 : ∑ v ∈ S C, (gz C v - 1) * (6 - gz C v) = 0 := by linarith
  have hs16 : ((S C).card : ℤ) = 16 := by linarith
  have hall := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hT0
  have hdvd : ∀ v ∈ S C, (5 : ℤ) ∣ (gz C v - 1) := fun v hv => by
    rcases mul_eq_zero.mp (hall v hv) with h1 | h1
    · rw [h1]; exact dvd_zero 5
    · have h6 : gz C v - 1 = 5 := by linarith
      rw [h6]
  have hdvd_sum : (5 : ℤ) ∣ ∑ v ∈ S C, (gz C v - 1) := Finset.dvd_sum hdvd
  rw [Finset.sum_sub_distrib, hS1, Finset.sum_const, nsmul_eq_mul, mul_one, hs16] at hdvd_sum
  omega

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
  rw [sum_cov_filter]
  have hc : ∀ c : V, (univ.filter (fun v : V => dist c v ≤ 1 ∧ v.card = i)).card
      = (if c.card = i then 1 else 0)
        + ((if c.card - 1 = i then c.card else 0) + (if c.card + 1 = i then 8 - c.card else 0)) := by
    intro c
    rw [card_ball_filter c (fun v => v.card = i), card_filter_symmDiff_singleton c (fun n => n = i)]
  simp_rw [hc]
  have hA : ∑ c ∈ C, (if c.card - 1 = i then c.card else 0) = (i + 1) * m C (i + 1) := by
    rw [m, Finset.card_filter, Finset.mul_sum]
    apply Finset.sum_congr rfl; intro c _
    split_ifs <;> omega
  have hB : ∑ c ∈ C, (if c.card + 1 = i then 8 - c.card else 0) = (9 - i) * m C (i - 1) := by
    rw [m, Finset.card_filter, Finset.mul_sum]
    apply Finset.sum_congr rfl; intro c _
    split_ifs <;> omega
  have hM : ∑ c ∈ C, (if c.card = i then 1 else 0) = m C i := by
    rw [m, Finset.card_filter]
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, hA, hB, hM]
  ring

/-- The `i = 0` case: the only weight-0 word is `∅`, covered by itself and by
    every weight-1 codeword. -/
theorem layer_identity_zero (C : Finset V) :
    ∑ v ∈ univ.filter (fun v : V => v.card = 0), cov C v = m C 0 + m C 1 := by
  have h0 : univ.filter (fun v : V => v.card = 0) = {∅} := by
    ext v; simp [Finset.card_eq_zero]
  have hd : ∀ c : V, dist c ∅ = c.card := by
    intro c
    have : symmDiff c ∅ = c := by ext i; simp [Finset.mem_symmDiff]
    rw [dist, this]
  rw [h0, Finset.sum_singleton, cov, m, m, ← Finset.card_union_of_disjoint, ← Finset.filter_or]
  · congr 1
    apply Finset.filter_congr
    intro c _
    rw [hd c]
    omega
  · rw [Finset.disjoint_filter]; intro c _ h0 h1; omega

lemma card_layer (i : ℕ) : (univ.filter (fun v : V => v.card = i)).card = Nat.choose 8 i := by
  have : univ.filter (fun v : V => v.card = i) = powersetCard i (univ : Finset (Fin 8)) := by
    ext v; simp [Finset.mem_powersetCard]
  rw [this, Finset.card_powersetCard, Finset.card_univ, Fintype.card_fin]

/-- Capacity of layer `i`. -/
lemma m_le (C : Finset V) (i : ℕ) : m C i ≤ Nat.choose 8 i := by
  rw [← card_layer i, m]
  exact Finset.card_le_card (Finset.filter_subset_filter _ (Finset.subset_univ C))

lemma m_nine (C : Finset V) : m C 9 = 0 := by
  have := m_le C 9
  rw [Nat.choose_eq_zero_of_lt (by norm_num)] at this
  omega

/-- The layers partition `C`. -/
lemma sum_m (C : Finset V) : ∑ i ∈ range 9, m C i = C.card := by
  symm
  rw [Finset.card_eq_sum_card_fiberwise (f := fun c : V => c.card) (s := C) (t := range 9) ?_]
  · rfl
  · intro c _
    simp only [Finset.mem_coe, Finset.mem_range]
    have := card_le_eight c
    omega

/-- A full ball at `∅` means every word of weight `≤ 1` is a codeword. -/
lemma mem_of_full_ball (C : Finset V) (h0 : cov C ∅ = 9) (v : V) (hv : v.card ≤ 1) :
    v ∈ C := by
  have hsub : C.filter (fun c => dist c ∅ ≤ 1) ⊆ univ.filter (fun c : V => dist ∅ c ≤ 1) := by
    intro c hc
    rw [Finset.mem_filter] at hc ⊢
    exact ⟨Finset.mem_univ _, by rw [dist_comm]; exact hc.2⟩
  have heq : C.filter (fun c => dist c ∅ ≤ 1) = univ.filter (fun c : V => dist ∅ c ≤ 1) := by
    apply Finset.eq_of_subset_of_card_le hsub
    rw [card_ball]
    show 9 ≤ cov C ∅
    omega
  have hv' : v ∈ univ.filter (fun c : V => dist ∅ c ≤ 1) := by
    rw [Finset.mem_filter, dist_comm, dist_empty]
    exact ⟨Finset.mem_univ _, hv⟩
  rw [← heq, Finset.mem_filter] at hv'
  exact hv'.1

lemma m_zero_of_full (C : Finset V) (h0 : cov C ∅ = 9) : m C 0 = 1 := by
  have : C.filter (fun c => c.card = 0) = {∅} := by
    ext c
    simp only [Finset.mem_filter, Finset.mem_singleton, Finset.card_eq_zero]
    constructor
    · exact fun h => h.2
    · rintro rfl
      exact ⟨mem_of_full_ball C h0 ∅ (by simp), rfl⟩
  rw [m, this, Finset.card_singleton]

lemma m_one_of_full (C : Finset V) (h0 : cov C ∅ = 9) : m C 1 = 8 := by
  have : C.filter (fun c => c.card = 1) = univ.filter (fun v : V => v.card = 1) := by
    ext c
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    exact ⟨fun h => h.2, fun h => ⟨mem_of_full_ball C h0 c (by omega), h⟩⟩
  rw [m, this, card_layer, Nat.choose_one_right]

/-- Translation by `t` is a distance-preserving bijection of `V`. -/
lemma cov_image_symmDiff (C : Finset V) (t v : V) :
    cov (C.image (fun c => symmDiff c t)) (symmDiff v t) = cov C v := by
  have hinj : Function.Injective (fun c : V => symmDiff c t) :=
    fun a b hab => symmDiff_left_inj.mp hab
  unfold cov
  rw [Finset.filter_image, Finset.card_image_of_injective _ hinj]
  congr 1
  apply Finset.filter_congr
  intro c _
  show dist (symmDiff c t) (symmDiff v t) ≤ 1 ↔ dist c v ≤ 1
  rw [dist_symmDiff_right]

lemma isDoubleCover_image (C : Finset V) (h : IsDoubleCover C) (t : V) :
    IsDoubleCover (C.image (fun c => symmDiff c t)) := by
  intro v
  have := cov_image_symmDiff C t (symmDiff v t)
  rw [symmDiff_symmDiff_cancel_right] at this
  rw [this]
  exact h _

/-- The Farkas step, for a code whose full ball sits at `∅`. -/
lemma layer_contradiction_zero (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60)
    (h0 : cov C ∅ = 9) : False := by
  have hm0 := m_zero_of_full C h0
  have hm1 := m_one_of_full C h0
  have hm8 := m_le C 8
  have hm9 := m_nine C
  have hsum := sum_m C
  rw [hc] at hsum
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add] at hsum
  have hL : ∀ i, 2 * Nat.choose 8 i ≤ ∑ v ∈ univ.filter (fun v : V => v.card = i), cov C v := by
    intro i
    have := Finset.sum_le_sum (fun v (_ : v ∈ univ.filter (fun v : V => v.card = i)) => h v)
    rw [Finset.sum_const, smul_eq_mul, card_layer] at this
    omega
  have h0' := hL 0
  rw [layer_identity_zero] at h0'
  have h1' := hL 1
  rw [layer_identity C 1 (by norm_num) (by norm_num)] at h1'
  have h2' := hL 2
  rw [layer_identity C 2 (by norm_num) (by norm_num)] at h2'
  have h3' := hL 3
  rw [layer_identity C 3 (by norm_num) (by norm_num)] at h3'
  have h4' := hL 4
  rw [layer_identity C 4 (by norm_num) (by norm_num)] at h4'
  have h5' := hL 5
  rw [layer_identity C 5 (by norm_num) (by norm_num)] at h5'
  have h6' := hL 6
  rw [layer_identity C 6 (by norm_num) (by norm_num)] at h6'
  have h7' := hL 7
  rw [layer_identity C 7 (by norm_num) (by norm_num)] at h7'
  have h8' := hL 8
  rw [layer_identity C 8 (by norm_num) (by norm_num)] at h8'
  norm_num [Nat.choose] at h0' h1' h2' h3' h4' h5' h6' h7' h8' hm8
  omega

/-- The Farkas certificate, with weights `w = (0,0,0,8,8,2,2,17,17)`:
    weighted demand is `2658`, but the nine words of the full ball contribute
    nothing and the remaining `51` contribute at most `50*48 + 153 = 2553`.
    The capacity `m 8 <= 1` is essential and is what makes `153` appear once. -/
theorem layer_contradiction (C : Finset V) (h : IsDoubleCover C) (hc : C.card = 60)
    (y : V) (hy : cov C y = 9) : False := by
  have hinj : Function.Injective (fun c : V => symmDiff c y) :=
    fun a b hab => symmDiff_left_inj.mp hab
  apply layer_contradiction_zero (C.image (fun c => symmDiff c y)) (isDoubleCover_image C h y)
  · rw [Finset.card_image_of_injective _ hinj, hc]
  · have := cov_image_symmDiff C y y
    rw [symmDiff_self, Finset.bot_eq_empty] at this
    exact this.trans hy

/-! ### Main theorem -/

theorem no_60_word_double_cover (C : Finset V) (h : IsDoubleCover C) : C.card ≠ 60 := by
  intro hc
  obtain ⟨y, hy⟩ := exists_full_ball C h hc
  exact layer_contradiction C h hc y hy

/-! ### Monotonicity and the final bound `K(8,1,2) >= 61` -/

/-- Coverage is monotone in the code. -/
theorem cov_mono {C D : Finset V} (h : C ⊆ D) (v : V) : cov C v ≤ cov D v := by
  unfold cov
  exact Finset.card_le_card (Finset.filter_subset_filter _ h)

/-- A double cover stays one when codewords are added. -/
theorem isDoubleCover_mono {C D : Finset V} (h : C ⊆ D)
    (hC : IsDoubleCover C) : IsDoubleCover D :=
  fun v => (hC v).trans (cov_mono h v)

/-- No double cover of Q_8 has 60 or fewer words: K(8,1,2) ≥ 61. -/
theorem le_card_of_isDoubleCover (C : Finset V) (h : IsDoubleCover C) :
    61 ≤ C.card := by
  by_contra hlt
  have hle : C.card ≤ 60 := by omega
  have h60 : 60 ≤ (univ : Finset V).card := by
    rw [Finset.card_univ, card_V]; norm_num
  obtain ⟨D, hCD, -, hD⟩ :=
    Finset.exists_subsuperset_card_eq (Finset.subset_univ C) hle h60
  exact no_60_word_double_cover D (isDoubleCover_mono hCD h) hD

end Mcov
