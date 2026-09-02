# External tool versions

None of these is needed to check the **theorem** — the eight core scripts are
standard library only. They are needed only to reproduce the *certification*
leg (the machine-checkable refutation of `|C| = 59`) and the solver-backed
search models.

## Pinned versions

| tool | version | role |
|---|---|---|
| Python | 3.9+ | all scripts; 3.12 used for the recorded runs |
| SCIP | **10.0** (scipoptsuite-10.0.0) | exact-rational branch and bound, emits VIPR |
| SoPlex | **7.1.6** | exact rational LP inside SCIP; built by scipoptsuite |
| VIPR | **1.1** (`viprcomp`, `viprchk`) | completes and checks SCIP's certificate |
| VeriPB | **3.0.2** (Rust) | checks RoundingSat's cutting-planes proof |
| VeriPB | **2.3.0** (Python/C++) | second, independently implemented checker |
| RoundingSat | see `CERTIFICATION.md` §2.5 | pseudo-Boolean prover, route 1 |
| GMP | with `--enable-cxx` | required by VeriPB 2.x and exact arithmetic |
| Boost | 1.88 headers | `multiprecision/cpp_int.hpp` for RoundingSat |
| Rust | stable | to build VeriPB 3.x |
| Lean | **4.33.1** | formalisation (`lean/`) |
| mathlib | rev **v4.33.1** | pinned in `lean/lakefile.toml` |

Python packages are pinned in `requirements-research.txt`.

## Build

Full build instructions, in the order that works, are in
[`CERTIFICATION.md`](CERTIFICATION.md) §2 — it records eleven distinct build
blockers hit while assembling this pipeline, with the fix for each. Read it
before attempting the certification leg; it will save a day.

Notable gotchas already documented there:

- `scipoptsuite` builds SoPlex 7.1.6 itself; budget ~15 minutes for that alone.
- GMP **must** be configured with `--enable-cxx` or the VeriPB 2.x extension
  fails to compile.
- `viprchk` does **not** read `.gz`; route 1's VeriPB does. The compressed
  artifact is checkable only by route 1.

## Lean

```
cd lean
lake exe cache get        # ~7.4 GB of prebuilt mathlib
lake build                # ~4 minutes once cached
```

On macOS 15+/Darwin 25, Lean 4.14's prebuilt mathlib `cache` binary will not
run (`dyld: __DATA_CONST segment missing SG_READ_ONLY flag`); 4.33.1 works.
The build currently reports **16 `sorry`s** — statements elaborate, proofs are
unfinished. See `lean/README.md`.

## What is reproducible without any of this

`./reproduce.sh` runs ten self-asserting checks using only the standard library
plus `scipy` (for LP controls), in about a minute, and exits non-zero on any
failure. That covers every **established** claim in this package.
