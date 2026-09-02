#!/usr/bin/env bash
# One-command reproduction. Exits non-zero if ANY check fails.
#
#   ./reproduce.sh          core claims, standard library only, ~1 minute
#   ./reproduce.sh --full   also the solver-backed models (needs requirements)
#
# Every script below is self-asserting: it raises rather than printing a wrong
# number, so a zero exit status is the whole result.
set -u
PY=${PY:-python3}
FULL=0
[ "${1:-}" = "--full" ] && FULL=1
pass=0; fail=0; failed=()

run () {  # run <label> <cmd...>
  local label="$1"; shift
  printf '  %-34s ' "$label"
  if "$@" >/tmp/_repro.$$ 2>&1; then
    echo "PASS"; pass=$((pass+1))
  else
    echo "FAIL"; fail=$((fail+1)); failed+=("$label")
    sed 's/^/      | /' /tmp/_repro.$$ | tail -12
  fi
  rm -f /tmp/_repro.$$
}

echo "=== Core claims (standard library only) ==="
run "excess theorem"            $PY excess_theorem.py
run "weight-parity split"       $PY bipartite_split.py
run "half-excess inequality"    $PY half_excess.py
run "counting route is dead"    $PY e2_bound.py
run "odd-n counterexample"      $PY odd_n_witness.py
run "incumbent verifies"        $PY verify.py --incumbent
run "HHKL Thm 6 collapses"      $PY hhkl_theorem6.py
run "even-mu generalisation"    $PY mu_generalization.py

echo
echo "=== Dominance over Krotov-Potapov (needs scipy for controls) ==="
run "dominance + ceiling lemma" $PY dominance.py

echo
echo "=== CANDIDATE, not an established claim ==="
run "M=60 refutation (K>=61)"   $PY m61_refutation.py

if [ "$FULL" = "1" ]; then
  echo
  echo "=== Solver-backed models (requirements-research.txt) ==="
  run "known-answer gate n=4..8" $PY local_search.py --gate
  run "MILP n=6 M=19"            $PY milp_model.py --n 6 --mode 19 --budget 60
  run "MILP n=6 M=20"            $PY milp_model.py --n 6 --mode 20 --budget 60
fi

echo
echo "-------------------------------------------------"
printf '  %d passed, %d failed\n' "$pass" "$fail"
if [ "$fail" -ne 0 ]; then
  printf '  failed: %s\n' "${failed[*]}"
  exit 1
fi
echo "  ALL CHECKS PASSED"
echo
echo "  Established: K(8,1,2) >= 60, and the bound"
echo "      |C| >= ceil(3*2^(n+1)/(3n+2))   for even n"
echo "  improves the published lower bound at n = 8, 10, 12, 14, 16."
echo "  K(8,1,2) >= 61 is a CANDIDATE: no human review. See README.md."
exit 0
