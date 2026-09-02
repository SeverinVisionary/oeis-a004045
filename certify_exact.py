#!/usr/bin/env python3
"""Second certification route: exact-rational MILP with a VIPR certificate.

Independent of `certify.py` in prover, proof system and checker:

    certify.py       RoundingSat  -> VeriPB v2 cutting-planes derivation -> VeriPB
    certify_exact.py SCIP (exact) -> VIPR certificate -> viprcomp -> viprchk

Both consume **the same .opb file**, which is the point. SCIP reads OPB
natively, so route 2 needs no second encoder and no second encoding audit: if
the two routes agree, they agree about one artifact, not about two hopefully
equal ones.

    ./certify_exact.py --n 6 --M 19 --outdir certs_exact
    ./certify_exact.py --n 8 --M 57 --outdir certs_exact --budget 86400

Why three tools and not two: SCIP 10 writes an *incomplete* VIPR 1.1
certificate. Its aggregation derivations carry `{ lin weak { ... } ... }`
reasons, which record that a linear combination only weakly dominates the
constraint and leave the dominating multipliers to be filled in later.
`viprchk` alone rejects these with `Syntax Error in AggrRow_N: Expecting }
but read instead {` -- which looks like a broken certificate and is not.
`viprcomp` reconstructs the missing multipliers with an exact rational LP
solve and emits `<name>_complete.vipr`, and *that* is what `viprchk` verifies.
Neither `separating/maxrounds 0` nor `exact/safedbmethod e` avoids the
incomplete form; the completion step is not optional.

Requires a SCIP built with `-DEXACTSOLVE=ON -DLPSEXACT=spx` -- the PyPI
`pyscipopt` wheel is **not** such a build (`enableExactSolving` there returns
"SCIP was compiled without exact solve support") -- and the *maintained* VIPR
at github.com/scipopt/vipr, not the archived ambros-gleixner one, whose
checker predates the 1.1 incomplete format. See CERTIFICATION.md §5. Paths
default to $SCIPEXACT, $VIPRCOMP and $VIPRCHK.

What a record certifies
-----------------------
The same single statement as route 1 -- `K(n,1,2) > M`, i.e. the OPB instance
has no 0/1 solution -- established in exact rational arithmetic throughout,
with an infeasibility certificate that `viprchk` replays independently.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pb_encode  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def machine():
    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True, text=True).stdout.strip() or platform.processor(),
        "cpu_count": os.cpu_count(),
        "loadavg_1min_at_start": os.getloadavg()[0],
    }


def run_scip(scip, opb, vipr, budget, threads=1):
    """Solve the OPB in exact rational mode, writing a VIPR certificate."""
    script = [
        "set exact enable TRUE",
        "set certificate filename %s" % vipr,
        "set limits time %d" % int(budget),
        "set parallel maxnthreads %d" % threads,
        "read %s" % opb,
        "optimize",
        "quit",
    ]
    cmd = [scip]
    for line in script:
        cmd += ["-c", line]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=budget + 600)
    dt = time.time() - t0
    out = p.stdout + p.stderr
    status = None
    for line in out.splitlines():
        if line.startswith("SCIP Status"):
            status = line.split(":", 1)[1].strip()
    return {
        "command": " ".join('"%s"' % c if " " in c else c for c in cmd),
        "exit_code": p.returncode,
        "seconds": round(dt, 2),
        "scip_status": status,
        "stdout_tail": out.strip().splitlines()[-30:],
    }, status


def run_viprcomp(viprcomp, vipr, budget):
    """Fill in the multipliers SCIP left out of its `weak` derivations."""
    t0 = time.time()
    p = subprocess.run([viprcomp, vipr], capture_output=True, text=True, timeout=budget)
    dt = time.time() - t0
    out = (p.stdout + p.stderr).strip()
    done = vipr[:-len(".vipr")] + "_complete.vipr"
    return {
        "command": "%s %s" % (viprcomp, vipr),
        "exit_code": p.returncode,
        "seconds": round(dt, 2),
        "output": out.splitlines()[-10:],
        "completed_path": done if os.path.exists(done) else None,
    }, done


def run_viprchk(viprchk, vipr, budget):
    t0 = time.time()
    p = subprocess.run([viprchk, vipr], capture_output=True, text=True, timeout=budget)
    dt = time.time() - t0
    out = (p.stdout + p.stderr).strip()
    low = out.lower()
    return {
        "command": "%s %s" % (viprchk, vipr),
        "exit_code": p.returncode,
        "seconds": round(dt, 2),
        "output": out.splitlines()[-10:],
        "accepted": p.returncode == 0 and "verified infeasibility" in low,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--M", type=int, required=True)
    ap.add_argument("--outdir", default=os.path.join(HERE, "certs_exact"))
    ap.add_argument("--scip", default=None, help="exact-enabled scip binary ($SCIPEXACT)")
    ap.add_argument("--viprcomp", default=None, help="viprcomp binary ($VIPRCOMP)")
    ap.add_argument("--viprchk", default=None, help="viprchk binary ($VIPRCHK)")
    ap.add_argument("--budget", type=float, default=3600.0)
    ap.add_argument("--compress", action="store_true", help="gzip the certificate")
    ap.add_argument("-o", default=None)
    a = ap.parse_args()

    scip = a.scip or os.environ.get("SCIPEXACT") or shutil.which("scip")
    viprcomp = a.viprcomp or os.environ.get("VIPRCOMP") or shutil.which("viprcomp")
    viprchk = a.viprchk or os.environ.get("VIPRCHK") or shutil.which("viprchk")
    for label, path in (("scip", scip), ("viprcomp", viprcomp), ("viprchk", viprchk)):
        if not path or not os.path.exists(path):
            print("missing %s binary (%r); see CERTIFICATION.md" % (label, path),
                  file=sys.stderr)
            return 2

    os.makedirs(a.outdir, exist_ok=True)
    stem = "n%d_M%d" % (a.n, a.M)
    opb = os.path.join(a.outdir, "inst_%s.opb" % stem)
    vipr = os.path.join(a.outdir, "cert_%s.vipr" % stem)
    meta = pb_encode.write_opb(opb, a.n, a.M, mu=2)

    rec = {
        "statement": ("K(%d,1,2) > %d  --  no set C subset F_2^%d with |C| <= %d "
                      "has every word of F_2^%d within Hamming distance 1 of at "
                      "least 2 members of C" % (a.n, a.M, a.n, a.M, a.n)),
        "route": "exact-rational MILP (SCIP) -> VIPR certificate -> viprcomp -> viprchk",
        "n": a.n, "M": a.M, "mu": 2,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "machine": machine(),
        "instance": {
            "path": os.path.basename(opb),
            "variables": meta["variables"], "constraints": meta["constraints"],
            "bytes": meta["bytes"], "sha256": meta["sha256"],
            "note": "byte-identical to the instance certify.py refutes",
        },
        "tools": {"scip": scip, "viprcomp": viprcomp, "viprchk": viprchk,
                  "python": sys.version.split()[0]},
    }

    srec, status = run_scip(scip, opb, vipr, a.budget)
    rec["solve"] = srec
    if not status or "infeasible" not in status.lower():
        rec["result"] = "NOT REFUTED (SCIP status %r)" % status
        rec["certified"] = False
    elif not os.path.exists(vipr):
        rec["result"] = "NO CERTIFICATE EMITTED"
        rec["certified"] = False
    else:
        rec["certificate"] = {
            "path": os.path.basename(vipr),
            "bytes": os.path.getsize(vipr),
            "lines": sum(1 for _ in open(vipr, "rb")),
            "sha256": sha256(vipr),
        }
        crec, done = run_viprcomp(viprcomp, vipr, a.budget)
        rec["complete"] = crec
        if not crec["completed_path"]:
            rec["result"] = "COMPLETION FAILED"
            rec["certified"] = False
            text = json.dumps(rec, indent=2)
            print(text)
            if a.o:
                open(a.o, "w").write(text + "\n")
            print(rec["result"])
            return 1
        rec["complete"]["bytes"] = os.path.getsize(done)
        rec["complete"]["sha256"] = sha256(done)
        rec["check"] = run_viprchk(viprchk, done, a.budget)
        if a.compress and rec["check"]["accepted"]:
            # viprchk, unlike VeriPB, cannot read a compressed certificate, so
            # the committed .gz has to be expanded before checking. recheck.py
            # does that itself; the raw sha256 is kept so the expansion can be
            # verified against what was actually checked.
            import gzip
            gz = done + ".gz"
            with open(done, "rb") as src, gzip.open(gz, "wb", 6) as dst:
                shutil.copyfileobj(src, dst, 1 << 22)
            os.unlink(done)
            os.unlink(vipr)
            rec["complete"]["uncompressed_bytes"] = rec["complete"].pop("bytes")
            rec["complete"]["uncompressed_sha256"] = rec["complete"]["sha256"]
            rec["complete"]["completed_path"] = os.path.basename(gz)
            rec["complete"]["bytes"] = os.path.getsize(gz)
            rec["complete"]["sha256"] = sha256(gz)
            rec["certificate"]["note"] = ("the incomplete certificate SCIP wrote "
                                          "is not retained; regenerate with the "
                                          "solve command above")
        rec["certified"] = bool(rec["check"]["accepted"])
        rec["result"] = "VERIFIED" if rec["certified"] else "CHECKER REJECTED"

    text = json.dumps(rec, indent=2)
    print(text)
    if a.o:
        with open(a.o, "w") as f:
            f.write(text + "\n")
    print(rec["result"])
    return 0 if rec.get("certified") else 1


if __name__ == "__main__":
    sys.exit(main())
