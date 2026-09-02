# Certifying infeasibility for `K(n,1,2)`

**What this file is.** Everything needed to rebuild the pipeline and re-check
every certificate in [`certs/`](certs/) from scratch, on a machine that has
never seen this repository. A certificate nobody else can check is not a
certificate.

**What this file is not.** A claim. See [`certs/MANIFEST.md`](certs/MANIFEST.md)
for what has actually been certified and what is still trusted; see
[`WORKLOAD_ESTIMATE_2026-08-28.md`](WORKLOAD_ESTIMATE_2026-08-28.md) §5 for the
measured costs. No bound is stated as a result anywhere in this directory.

---

## 1. The architecture, and why this one

The search models (`milp_model.py`, `scip_model.py`) are floating-point
branch-and-bound. Two of them agreeing that an instance is infeasible is
evidence, not a proof: both could be wrong in the same way, and neither emits
anything a third party can replay.

The refutations here are **counting arguments** over 0/1 variables with integer
coefficients, so the proof system they live in is **cutting planes**, not
resolution. §3.3 of the estimate measured DRAT proof growth at ≈462× in bytes
per unit of `n` and put an `n = 8` DRAT proof at 10²–10³ GB; that route is
dead on size alone. Cutting planes expresses "add up all 2^n ball constraints,
divide by `n+1`, round" in a handful of lines.

So:

```
  pb_encode.py      the instance, as OPB                 (this repo)
       |
  RoundingSat       constructs a cutting-planes refutation, logs it as
       |            a VeriPB v2.0 derivation              (Elffers/Devriendt/Nordström)
  VeriPB            replays the derivation against the OPB and accepts
       |            or rejects it                         (Oertel et al.)
  recheck.py        re-derives the OPB from the definition of K(n,1,2),
                    re-hashes the artifacts, re-runs VeriPB (this repo)
```

The proof is *produced* by one program and *checked* by a different program by
different authors. A `VERIFIED` record therefore does not depend on RoundingSat
being correct.

### What remains trusted

Listed honestly, because certification moves trust rather than removing it:

| Trusted | Why it is not eliminated here |
|---|---|
| **VeriPB's correctness** | the checker is the last link; a second, independently implemented checker (VeriPB 2.x, Python/C++ rather than Rust) is run over the same artifacts to reduce this, and CakePB — formally verified in HOL4 — would reduce it further |
| **The encoding** | `pb_audit.py` and `recheck.py` attack this from three directions (§4), but "the OPB says what the English says" is ultimately a human reading of twelve lines |
| **Compilers and libraries** | rustc, clang, Boost, GMP; no attempt is made to verify these |
| **The machine** | single host, no ECC assumption stated; re-running elsewhere is the remedy and is what these instructions are for |
| **`verify.py`** | used as the independent cross-check in the audit; itself unverified, but it is 96 lines of standard library and shares no code with anything else here |

Not trusted, and this is the point: **HiGHS, SCIP, floating-point arithmetic,
and RoundingSat's own search.**

---

## 2. Build

Measured on: macOS 26.6.1 (Darwin 25.6.0), Apple M1 Pro, 10 cores, 16 GB,
arm64. Exact versions are what the certificates were produced with; anything
newer should work but has not been measured here.

Everything below installs into a scratch prefix and touches nothing system-wide.

```bash
export CERT=$PWD/cert && mkdir -p "$CERT" && cd "$CERT"
```

### 2.1 Rust (for VeriPB 3.x)

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- \
    -y --no-modify-path --default-toolchain stable --profile minimal
export PATH="$HOME/.cargo/bin:$PATH"
# measured with: rustc 1.98.0 (88d9e12ae 2026-08-18), cargo 1.98.0
```

### 2.2 VeriPB 3.0.2 — the checker

```bash
git clone https://gitlab.com/MIAOresearch/software/VeriPB.git veripb
cd veripb && git checkout e4ffda3b7b68bf0ffb42bc14f4170836ba4656e2   # 2026-08-26
LZMA_API_STATIC=1 cargo build --release        # ~2.5 min
./target/release/veripb --version              # -> veripb 3.0.2
cd ..
```

`LZMA_API_STATIC=1` is **required on macOS**: the `xz2` crate links the system
`liblzma`, and macOS 26 ships no linkable `liblzma` stub in the SDK, so the
default build fails at link time with `Undefined symbols ... _lzma_code`. The
variable makes `lzma-sys` compile its bundled C source instead. On Linux with
`liblzma-dev` present it is unnecessary.

### 2.3 Boost 1.88 headers (for RoundingSat)

RoundingSat needs `boost/multiprecision/cpp_int.hpp` and a `BoostConfig.cmake`.
CMake 4.x removed the old `FindBoost` module, so a bare header tree is not
enough — Boost must be installed by its own `b2`, which generates the CMake
package config.

```bash
curl -sL -o boost.tar.gz \
  https://archives.boost.io/release/1.88.0/source/boost_1_88_0.tar.gz
tar xzf boost.tar.gz && cd boost_1_88_0
./bootstrap.sh --prefix="$CERT/boost-install" --with-libraries=iostreams
./b2 install -j10 --prefix="$CERT/boost-install" --with-iostreams \
     -sNO_BZIP2=1 -sNO_LZMA=1 -sNO_ZSTD=1 link=static      # ~25 min, mostly header copying
cd ..
```

### 2.4 GMP 6.3.0 (arm64)

Needed by VeriPB 2.x's C++ extension (§5) and by any exact-arithmetic MILP
attempt. Homebrew on this host is an **x86_64** installation running under
Rosetta, so its `gmp` cannot be linked into an arm64 binary — hence a source
build.

```bash
curl -sL -o gmp.tar.xz https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz
tar xf gmp.tar.xz && cd gmp-6.3.0
./configure --prefix="$CERT/gmp-install" --enable-cxx --with-pic
make -j10 && make install && cd ..
```

`--enable-cxx` is required: without `libgmpxx` the VeriPB 2.x extension fails
to load with `symbol not found in flat namespace '...__mpz_struct'`.

### 2.5 RoundingSat — the prover

```bash
git clone https://gitlab.com/MIAOresearch/software/roundingsat.git roundingsat
cd roundingsat
git checkout d4edbf7908a9bb951fd181940919e0f3ac7ab1ee     # 2026-03-03
cd build
cmake -DCMAKE_BUILD_TYPE=Release \
      -Dsoplex=ON \
      -DCMAKE_OSX_ARCHITECTURES=arm64 \
      -DBoost_DIR="$CERT/boost-install/lib/cmake/Boost-1.88.0" \
      -DCMAKE_CXX_FLAGS="-I$CERT/boost-install/include" \
      "-Dsoplex_cmake_args=-DCMAKE_OSX_ARCHITECTURES=arm64;-DBoost_DIR=$CERT/boost-install/lib/cmake/Boost-1.88.0;-DCMAKE_CXX_FLAGS=-I$CERT/boost-install/include" \
      ..
make -j10          # SoPlex 7.1.6 is downloaded and built first; ~15 min for it alone
./roundingsat --help | head -1
```

Three of those flags exist only because of this host and are worth
understanding before dropping them:

* `-DCMAKE_OSX_ARCHITECTURES=arm64` — CMake here runs under Rosetta and
  otherwise emits `-arch x86_64` on an M1;
* `-DCMAKE_CXX_FLAGS="-I..."` — `Boost_DIR` alone puts the private Boost on
  `-isystem`, and `/usr/local/include` (Homebrew's Boost 1.60, from 2016) wins,
  which fails on `std::binary_function` and `std::auto_ptr` under C++20;
* `-Dsoplex_cmake_args=...` — the nested SoPlex build does **not** inherit the
  outer cache, so both of the above have to be handed to it explicitly.

**`-Dsoplex=ON` is not optional here.** It is the default, but turning it off
looks harmless and is not: see `logs/certification_2026-08-29.md`, where
`soplex=OFF` failed to close the *easiest* gate instance in 10 minutes while
`soplex=ON` closed it in 0.22 s. Whether SoPlex is linked changes the search
and therefore the proof, but never what the proof proves.

---

## 3. Produce a certificate

```bash
export ROUNDINGSAT=$CERT/roundingsat/build/roundingsat
export VERIPB=$CERT/veripb/target/release/veripb

# exactly what produced the committed artifacts
python3 certify.py --n 8 --M 57 --outdir certs --budget 43200 \
        --stream-gzip --solver-arg=--lp=-1 -o certs/cert_n8_M57.json
```

`certify.py` encodes, proves, checks, and writes one JSON record holding the
exact statement certified, both tools' versions, the wall-clock of each stage,
the machine, and the sizes and SHA-256 of the instance and the proof.

**Run the known-answer gate first.** `make certify-gate` certifies the
published *values* `K(6,1,2) = 20` and `K(7,1,2) = 32` — via `--opt`, which
proves matching bounds on `min |C|` — and the corresponding single rungs
`K(6,1,2) > 19` and `K(7,1,2) > 31`. All four are already in the literature. A
pipeline that cannot reproduce them cannot be trusted at `n = 8`.

Two flags matter for the larger runs:

* `--stream-gzip` pipes the proof through `gzip` as RoundingSat writes it, so
  the raw form never lands on disk. VeriPB reads the `.gz` directly, so the
  compressed file is itself the checkable artifact.
* `--solver-arg=--lp=-1` removes RoundingSat's default cap on how often it may
  call the LP. On `n = 8, M = 57` that is the difference between 25 632
  conflicts / 63 s / 227 MB and **2 011 conflicts / 2.6 s / 27.8 MB** — a 24×
  speedup and an 8× smaller artifact, for a problem whose refutations are
  LP-shaped counting arguments. It changes the search, not the statement.

---

## 4. Re-check a certificate — the part that matters

```bash
VERIPB=/path/to/veripb python3 recheck.py --certs certs
```

`recheck.py` is standard library only and imports nothing else in this
directory. Per certificate it does four things:

1. **re-derives** the instance from the definition of `K(n,1,2)` in twelve
   lines of its own, parses the committed `.opb`, and requires the two
   constraint multisets to be equal — so the proof is about the right formula
   and not merely about *a* formula;
2. re-hashes the `.opb` and `.pbp` against the record;
3. re-runs VeriPB and requires the verdict the record claims;
4. re-runs VeriPB against a deliberately *weaker* instance built from the same
   twelve lines — `M + 1` for a rung, `mu = 1` for a value — and requires it to
   be **rejected**. A checker that accepted everything would pass step 3
   silently; this is what catches it.

All four must pass. Any one failing prints `FAILED` and exits non-zero.

The encoding is separately attacked by `pb_audit.py`, which executes
`milp_model.py` with a recording stand-in for `highspy.Highs`, captures the
rows the MILP model *actually* builds, and compares them to a fresh parse of
the `.opb`; and which checks the published 64-word incumbent against the OPB
along with two deliberately broken codes, cross-checking the violation counts
against `verify.py`. Run it with `make audit`.

Proofs too large to commit are described in `certs/MANIFEST.md` by size, hash
and the exact command that regenerates them.

---

## 5. Route 2 — exact-rational MILP with a VIPR certificate

A second route over **the same `.opb` file**, with a different prover, a
different proof system and a different checker:

```
  SCIP 10 (exact rational mode)  ->  VIPR certificate  ->  viprchk
```

SCIP reads OPB natively, so route 2 needs no second encoder — which is the
whole point: the two routes certify one artifact rather than two hopefully
equal ones. Driver: `certify_exact.py`.

### 5.1 The PyPI wheel cannot do this — measured, not assumed

`pyscipopt==6.2.1` (the wheel `pyscipopt-6.2.1-cp312-cp312-macosx_11_0_arm64`,
SCIP 10.0) ships the `constraints/exactlinear` and `constraints/exactsol`
handlers, which makes it look like exact solving is available. It is not:

```
>>> m = pyscipopt.Model(); m.enableExactSolving(True)
[scip_exact.c:161] ERROR: SCIP was compiled without exact solve support:
                          cannot enable exact solving mode.
```

There is no `exact/*` parameter namespace at all in that build (3082
parameters, none under `exact/`). A source build is unavoidable.

### 5.2 Source build

```bash
curl -sL -o scipopt.tgz https://scipopt.org/download/release/scipoptsuite-10.0.0.tgz
tar xzf scipopt.tgz && mkdir -p scipoptsuite-10.0.0/build && cd scipoptsuite-10.0.0/build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES=arm64 \
      -DEXACTSOLVE=ON -DLPSEXACT=spx \
      -DGMP=ON  -DGMP_INCLUDE_DIR="$CERT/gmp-install/include" \
                -DGMP_LIBRARY="$CERT/gmp-install/lib/libgmp.dylib" \
      -DMPFR_INCLUDE_DIR="$CERT/mpfr-install/include" \
                -DMPFR_LIBRARY="$CERT/mpfr-install/lib/libmpfr.dylib" \
      -DBoost_DIR="$CERT/boost-install/lib/cmake/Boost-1.88.0" \
      -DPAPILO=OFF -DZIMPL=OFF -DIPOPT=OFF -DAMPL=OFF -DREADLINE=OFF \
      -DLAPACK=OFF -DBUILD_TESTING=OFF -DTPI=none ..
make -j6
```

MPFR 4.2.2 is an additional dependency of `EXACTSOLVE` and, like GMP, must be
built for arm64 from source on this host:

```bash
curl -sL -o mpfr.tar.xz https://www.mpfr.org/mpfr-current/mpfr-4.2.2.tar.xz
tar xf mpfr.tar.xz && cd mpfr-4.2.2
./configure --prefix="$CERT/mpfr-install" --with-gmp="$CERT/gmp-install"
make -j10 && make install && cd ..
```

### 5.3 The VIPR tools — **use the maintained repository**

`github.com/ambros-gleixner/VIPR` is **archived** and its `viprchk` predates
the VIPR 1.1 incomplete format that SCIP 10 emits. Against a SCIP 10
certificate it fails with

```
Syntax Error in AggrRow_193: Expecting } but read instead {
```

which looks like a corrupt certificate and is not. Use the maintained fork:

```bash
git clone https://github.com/scipopt/vipr.git vipr2   # 30f2951d, 2025-10-29
mkdir -p vipr2/code/build && cd vipr2/code/build
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_OSX_ARCHITECTURES=arm64 \
      -DGMP_LIBRARY="$CERT/gmp-install/lib/libgmp.dylib" \
      -DGMPXX_LIBRARY="$CERT/gmp-install/lib/libgmpxx.dylib" \
      -DBoost_DIR="$CERT/boost-install/lib/cmake/Boost-1.88.0" \
      -DCMAKE_CXX_FLAGS="-I$CERT/boost-install/include" ..
make viprchk -j4
```

Build the *target*, not `all`: `viprchk_parallel` needs TBB and will fail the
whole build without it.

### 5.4 `viprcomp`, which is not optional

SCIP 10 writes an **incomplete** certificate. Its aggregation rows carry
reasons of the form `{ lin weak { 0 } ... }` — the linear combination only
weakly dominates the constraint, and the dominating multipliers are left to be
reconstructed. `viprchk` alone cannot read them. Neither
`set separating maxrounds 0` nor `set exact safedbmethod e` suppresses the
incomplete form; both were tried and neither did.

`viprcomp` reconstructs the multipliers with an exact rational LP solve. It
needs SoPlex (already built inside scipoptsuite) **and** oneTBB:

```bash
git clone --depth 1 --branch v2022.0.0 https://github.com/uxlfoundation/oneTBB.git
mkdir -p oneTBB/build && cd oneTBB/build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES=arm64 \
      -DCMAKE_INSTALL_PREFIX="$CERT/tbb-install" \
      -DTBB_TEST=OFF -DTBB_EXAMPLES=OFF -DTBB_STRICT=OFF ..
make -j4 && make install && cd "$CERT/vipr2/code/build"

cmake -DVIPRCOMP=ON \
      -DTBB_DIR="$CERT/tbb-install/lib/cmake/TBB" \
      -DCMAKE_PREFIX_PATH="$CERT/tbb-install;$CERT/scipoptsuite-10.0.0/build;$CERT/boost-install" \
      -DGMP_LIBRARY="$CERT/gmp-install/lib/libgmp.dylib" \
      -DGMPXX_LIBRARY="$CERT/gmp-install/lib/libgmpxx.dylib" \
      -DCMAKE_CXX_FLAGS="-I$CERT/boost-install/include -I$CERT/gmp-install/include" ..
make viprcomp -j4
```

`viprcomp cert.vipr` writes `cert_complete.vipr`, and **that** is what
`viprchk` verifies.

### 5.5 Running route 2

```bash
export SCIPEXACT=$CERT/scipoptsuite-10.0.0/build/bin/scip
export VIPRCOMP=$CERT/vipr2/code/build/viprcomp
export VIPRCHK=$CERT/vipr2/code/build/viprchk
python3 certify_exact.py --n 6 --M 19 --outdir certs_exact
```

Status and measurements for this route are in `certs/MANIFEST.md`.

## 6. Second checker

The same artifacts are re-checked by **VeriPB 2.x**, an independent
implementation (Python + a C++ extension, on the `version2` branch) of the same
proof format. It shares the format and part of the author list with VeriPB 3.x
but not the code.

```bash
git clone -b version2 https://gitlab.com/MIAOresearch/software/VeriPB.git veripb2
#   b0d55dc8, 2025-06-05 -> VeriPB 2.3.0
python3 -m venv venv2
CPPFLAGS="-I$CERT/gmp-install/include" LDFLAGS="-L$CERT/gmp-install/lib" \
    ./venv2/bin/pip install ./veripb2
./venv2/bin/veripb --version
```

Results are recorded in `certs/MANIFEST.md`. Agreement between two checkers
does not make either correct, but it removes single-implementation risk, which
is the failure mode this whole exercise exists to address.
