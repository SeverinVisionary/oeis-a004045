# K(8,1,2) target. `make gate` must pass before any n = 8 statement is made.
PY ?= python3

.PHONY: gate incumbent lp clean audit certify-gate recheck

## known-answer gate. sat_model budgets are CONFLICT counts, not seconds.: reproduce every published term of A004045 with both models
gate:
	@echo "== incumbent =="
	$(PY) verify.py --incumbent
	@echo "== SAT model, known terms (SAT at a(n), UNSAT at a(n)-1) =="
	$(PY) sat_model.py --n 4 --M 8  --budget 100000
	$(PY) sat_model.py --n 4 --M 7  --budget 100000
	$(PY) sat_model.py --n 5 --M 12 --budget 100000
	$(PY) sat_model.py --n 5 --M 11 --budget 100000
	$(PY) sat_model.py --n 6 --M 20 --budget 2000000
	$(PY) sat_model.py --n 6 --M 19 --budget 2000000
	@echo "== MILP model (HiGHS), known terms =="
	$(PY) milp_model.py --n 6 --mode 19 --budget 60
	$(PY) milp_model.py --n 6 --mode 20 --budget 60
	@echo "== local search, known terms n=4..8 (witness side only) =="
	$(PY) local_search.py --gate
	$(PY) milp_model.py --n 7 --mode 31 --budget 60
	$(PY) milp_model.py --n 7 --mode 32 --budget 60
	@echo "== MILP model (SCIP), known terms =="
	$(PY) scip_model.py --n 6 --M 19 --budget 60
	$(PY) scip_model.py --n 6 --M 20 --budget 60
	$(PY) scip_model.py --n 7 --M 31 --budget 60
	$(PY) scip_model.py --n 7 --M 32 --budget 60
	@echo "== LP relaxation must be 2*2^n/(n+1) = 512/9 at n = 8 =="
	$(PY) milp_model.py --n 8 --mode lp --budget 60

incumbent:
	$(PY) verify.py --incumbent

lp:
	$(PY) milp_model.py --n 8 --mode lp --budget 60

## encoding audit: the PB instance and the MILP model must have the same feasible set
audit:
	$(PY) pb_audit.py

## certification known-answer gate: certify the published cases before any n = 8 run.
## The --opt runs certify the published VALUES K(6,1,2) = 20 and K(7,1,2) = 32,
## not merely the lower bounds. Needs $ROUNDINGSAT and $VERIPB; see CERTIFICATION.md.
certify-gate:
	$(PY) certify.py --n 6 --opt   --outdir certs --stream-gzip --solver-arg=--lp=-1 -o certs/cert_n6_opt.json
	$(PY) certify.py --n 7 --opt   --outdir certs --stream-gzip --solver-arg=--lp=-1 -o certs/cert_n7_opt.json
	$(PY) certify.py --n 6 --M 19  --outdir certs --stream-gzip --solver-arg=--lp=-1 -o certs/cert_n6_M19.json
	$(PY) certify.py --n 7 --M 31  --outdir certs --stream-gzip --solver-arg=--lp=-1 -o certs/cert_n7_M31.json

## re-verify every committed certificate from its artifacts.
## certs/ needs $VERIPB; certs_exact/ needs $VIPRCHK. See CERTIFICATION.md.
recheck:
	$(PY) recheck.py --certs certs
	$(PY) recheck.py --certs certs_exact

clean:
	rm -f *.pyc
