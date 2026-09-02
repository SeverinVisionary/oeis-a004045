import Mcov.Basic
namespace Mcov
-- If any of these prints `sorryAx`, that theorem is NOT actually proved.
#print axioms sum_cov
#print axioms chi_mul
#print axioms a_even
#print axioms excess_eq
#print axioms sos_nonneg
#print axioms sos_eq_radial
#print axioms sum_chi_eq_f
#print axioms ball_sum_odd
#print axioms exists_excess_in_ball
#print axioms card_le_excess
#print axioms antipode_row
#print axioms second_moment
#print axioms layer_identity
#print axioms layer_identity_zero
-- expected to still depend on sorryAx:
#print axioms no_60_word_double_cover
end Mcov
