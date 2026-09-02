#!/usr/bin/env python3
"""Certification driver: refute K(n,1,2) <= M with a *checked* cutting-planes proof.

This is not a search model. It produces a proof object and then has an
independent program check it. Nothing here is a mathematical claim until the
checker line in the emitted record says `VERIFIED`.

    python3 certify.py --n 6 --M 19 --outdir certs        # refute one rung
    python3 certify.py --n 6 --opt   --outdir certs        # certify the value
    python3 certify.py --n 8 --M 57  --outdir certs --budget 86400

Pipeline
--------
    pb_encode.py  ->  instance .opb
    roundingsat   ->  VeriPB v2.0 cutting-planes derivation .pbp   (the proof)
    veripb        ->  independent check of (.opb, .pbp)            (the check)

The two halves are different programs by different authors: RoundingSat
constructs the refutation, VeriPB replays it against the .opb and accepts or
rejects. A `VERIFIED` record therefore does not rest on RoundingSat being
correct -- only on VeriPB being correct, on the encoding being faithful
(`pb_audit.py`), and on the compilers.

What a record certifies
-----------------------
In `--M` (decision) mode, exactly one statement and no more:

    there is no C subset of F_2^n with |C| <= M such that every word of F_2^n
    has at least 2 members of C within Hamming distance 1

i.e. K(n,1,2) > M. Nothing about K(n,1,2)'s value, and nothing about any other
M. Composing rungs into an interval is a separate, human step.

In `--opt` mode the instance carries the objective `min |C|` and no
cardinality constraint, and the solver proves matching bounds on it. VeriPB
then reports `VERIFIED BOUNDS a <= obj <= b`; with `a == b` that certifies
`K(n,1,2) = a` outright -- both directions in one object. This is the stronger
form and it is what the known-answer gate uses, but it is all-or-nothing: a
solver that runs out of budget in this mode emits `conclusion NONE` and yields
no bound at all, whereas each decision rung stands on its own. Hence decision
mode for the `n = 8` ladder.

Paths to the solver and checker default to $ROUNDINGSAT and $VERIPB, then to
whatever is on PATH. `recheck.py` re-runs only the checking half from committed
artifacts.
"""
import argparse
import gzip
import hashlib
import json
import os
import platform
import re
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


def tool(explicit, env, name):
    return explicit or os.environ.get(env) or shutil.which(name)


def version_of(cmd, args):
    if not cmd:
        return None
    try:
        p = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=60)
        return (p.stdout + p.stderr).strip().splitlines()[:3]
    except Exception as e:  # noqa: BLE001
        return ["<unavailable: %s>" % e]


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


def run_solver(solver, opb, pbp, budget, extra, stream_gzip=False):
    """Run the PB solver with proof logging. Returns (record, verdict).

    With `stream_gzip`, the proof is piped through gzip as it is written
    rather than landing on disk raw. RoundingSat's logger only ever appends
    and flushes, so a FIFO is safe, and VeriPB reads the resulting .gz
    directly -- which matters because these proofs reach hundreds of MB per
    rung and the raw form is the binding resource, not the compressed one.
    """
    target, gzproc, fifo = pbp, None, None
    if stream_gzip:
        fifo = pbp + ".fifo"
        if os.path.exists(fifo):
            os.unlink(fifo)
        os.mkfifo(fifo)
        target = fifo
        gzproc = subprocess.Popen(
            ["sh", "-c", "gzip -6 -c < %s > %s" % (fifo, pbp + ".gz")])
    cmd = [solver, "--proof-log=" + target, "--verbosity=1"] + list(extra) + [opb]
    t0 = time.time()
    expired = False
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=budget)
        out = p.stdout + p.stderr
        rc = p.returncode
    except subprocess.TimeoutExpired as e:
        # A rung that runs out of budget is a measurement, not a crash: record
        # where it stopped rather than losing the run.
        expired = True
        out = "".join(x.decode("utf-8", "replace") if isinstance(x, bytes) else (x or "")
                      for x in (e.stdout, e.stderr))
        rc = None
    finally:
        if gzproc is not None:
            gzproc.wait()
            os.unlink(fifo)
    dt = time.time() - t0
    verdict = None
    banner, stats = [], {}
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("s "):
            verdict = s[2:].strip()
        elif s.startswith("c ") and any(
                s[2:].startswith(k) for k in
                ("RoundingSat", "branch ", "commit ", "conflicts ", "decisions ",
                 "propagations ", "LP ", "CPU time")):
            body = s[2:]
            if body.startswith(("RoundingSat", "branch ", "commit ")):
                banner.append(body)
            else:
                k, _, v = body.rpartition(" ")
                stats[k.strip()] = v.strip()
    if expired:
        verdict = "BUDGET EXPIRED after %.0f s" % dt
    return {
        "command": " ".join(cmd),
        "exit_code": rc,
        "budget_expired": expired,
        "seconds": round(dt, 2),
        "verdict": verdict,
        "solver_banner": banner,
        "search": stats,
        "stdout_tail": out.strip().splitlines()[-25:],
    }, verdict


VERDICT_RE = re.compile(r"^s VERIFIED (UNSATISFIABLE|BOUNDS (\S+) <= obj <= (\S+))")


def run_checker(checker, opb, pbp, budget, opt=False):
    cmd = [checker, "--stats", opb, pbp]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=budget)
    dt = time.time() - t0
    out = (p.stdout + p.stderr).strip()
    verified, bounds = None, None
    for line in out.splitlines():
        m = VERDICT_RE.match(line.strip())
        if m:
            verified = m.group(1).split()[0]
            if m.group(2) is not None:
                bounds = [m.group(2), m.group(3)]
    want = "BOUNDS" if opt else "UNSATISFIABLE"
    return {
        "command": " ".join(cmd),
        "exit_code": p.returncode,
        "seconds": round(dt, 2),
        "output": out.splitlines()[-15:],
        "checker_verdict": verified,
        "bounds": bounds,
        "accepted": p.returncode == 0 and verified == want,
    }


def certify(n, M, outdir, solver, checker, budget, extra,
             keep_proof=True, compress=False, stream_gzip=False):
    os.makedirs(outdir, exist_ok=True)
    stem = "n%d_opt" % n if M is None else "n%d_M%d" % (n, M)
    opb = os.path.join(outdir, "inst_%s.opb" % stem)
    pbp = os.path.join(outdir, "proof_%s.pbp" % stem)

    meta = pb_encode.write_opb(opb, n, M, mu=2)
    if M is None:
        statement = ("K(%d,1,2) equals the value the checker reports, if it "
                     "reports matching bounds: the minimum |C| over C subset "
                     "F_2^%d with every word of F_2^%d within Hamming distance "
                     "1 of at least 2 members of C" % (n, n, n))
    else:
        statement = ("K(%d,1,2) > %d  --  no set C subset F_2^%d with |C| <= %d "
                     "has every word of F_2^%d within Hamming distance 1 of at "
                     "least 2 members of C" % (n, M, n, M, n))
    rec = {
        "statement": statement,
        "mode": "optimisation" if M is None else "decision",
        "n": n, "M": M, "mu": 2,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "machine": machine(),
        "instance": {
            "path": os.path.basename(opb),
            "variables": meta["variables"], "constraints": meta["constraints"],
            "bytes": meta["bytes"], "sha256": meta["sha256"],
        },
        "tools": {
            "encoder": "pb_encode.py sha256=" + sha256(os.path.join(HERE, "pb_encode.py")),
            "solver": solver,
            "checker": checker, "checker_version": version_of(checker, ["--version"]),
            "python": sys.version.split()[0],
        },
    }

    srec, verdict = run_solver(solver, opb, pbp, budget, extra, stream_gzip)
    rec["solve"] = srec
    want_verdict = "OPTIMUM FOUND" if M is None else "UNSATISFIABLE"
    if verdict != want_verdict:
        rec["result"] = "NOT ESTABLISHED (solver said %r, wanted %r)" % (
            verdict, want_verdict)
        rec["certified"] = False
        partial = pbp + (".gz" if stream_gzip else "")
        if os.path.exists(partial):
            rec["partial_proof_bytes"] = os.path.getsize(partial)
            os.unlink(partial)
        return rec

    if stream_gzip:
        pbp += ".gz"
        opener = lambda: gzip.open(pbp, "rb")  # noqa: E731
    else:
        opener = lambda: open(pbp, "rb")       # noqa: E731
    with opener() as f:
        lines = raw = 0
        for chunk in iter(lambda: f.read(1 << 22), b""):
            lines += chunk.count(b"\n")
            raw += len(chunk)
    rec["proof"] = {
        "path": os.path.basename(pbp),
        "bytes": os.path.getsize(pbp),
        "uncompressed_bytes": raw,
        "lines": lines,
        "sha256": sha256(pbp),
    }
    rec["check"] = run_checker(checker, opb, pbp, budget, opt=(M is None))
    rec["certified"] = bool(rec["check"]["accepted"])
    rec["result"] = "VERIFIED" if rec["certified"] else "CHECKER REJECTED"
    if rec["certified"] and M is None:
        lo, hi = rec["check"]["bounds"]
        rec["certified_value"] = int(lo) if lo == hi else None
        rec["statement"] = (("K(%d,1,2) = %s" % (n, lo)) if lo == hi
                            else ("%s <= K(%d,1,2) <= %s" % (lo, n, hi)))

    if compress and not stream_gzip and rec["certified"]:
        # VeriPB reads gzipped proofs directly (measured; it links xz and zstd
        # too, untested here), so the compressed file is itself a checkable
        # artifact -- no decompression step for the reader.
        gz = pbp + ".gz"
        with open(pbp, "rb") as src, gzip.open(gz, "wb", compresslevel=9) as dst:
            shutil.copyfileobj(src, dst, 1 << 22)
        os.unlink(pbp)
        rec["proof"]["uncompressed_bytes"] = rec["proof"].pop("bytes")
        rec["proof"]["uncompressed_sha256"] = rec["proof"].pop("sha256")
        rec["proof"]["path"] = os.path.basename(gz)
        rec["proof"]["bytes"] = os.path.getsize(gz)
        rec["proof"]["sha256"] = sha256(gz)
        rec["check"]["checked_file"] = os.path.basename(pbp)
        rec["check"]["note"] = ("checked uncompressed, then gzipped; VeriPB "
                                "accepts the .gz form too and recheck.py uses it")
    if not keep_proof:
        for p in (pbp, pbp + ".gz"):
            if os.path.exists(p):
                os.unlink(p)
        rec["proof"]["path"] = "<not retained; regenerate with the command above>"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--M", type=int, default=None)
    ap.add_argument("--opt", action="store_true",
                    help="certify the value of K(n,1,2) rather than one rung")
    ap.add_argument("--outdir", default=os.path.join(HERE, "certs"))
    ap.add_argument("--solver", default=None, help="RoundingSat binary ($ROUNDINGSAT)")
    ap.add_argument("--checker", default=None, help="VeriPB binary ($VERIPB)")
    ap.add_argument("--budget", type=float, default=3600.0, help="seconds, per stage")
    ap.add_argument("--drop-proof", action="store_true",
                    help="delete the .pbp after checking (keeps sizes and hashes)")
    ap.add_argument("--compress", action="store_true",
                    help="gzip the proof after checking; VeriPB reads .gz directly")
    ap.add_argument("--stream-gzip", action="store_true",
                    help="pipe the proof through gzip as it is written, so the "
                         "raw form never lands on disk (needed above ~1 GB)")
    ap.add_argument("--solver-arg", action="append", default=[],
                    help="extra argument passed through to the solver")
    ap.add_argument("-o", default=None, help="write the JSON record here too")
    a = ap.parse_args()
    if a.opt:
        a.M = None
    elif a.M is None:
        ap.error("give --M or --opt")

    solver = tool(a.solver, "ROUNDINGSAT", "roundingsat")
    checker = tool(a.checker, "VERIPB", "veripb")
    for label, path in (("solver", solver), ("checker", checker)):
        if not path or not os.path.exists(path):
            print("missing %s binary (%r); see CERTIFICATION.md for the build"
                  % (label, path), file=sys.stderr)
            return 2

    rec = certify(a.n, a.M, a.outdir, solver, checker, a.budget,
                  a.solver_arg, keep_proof=not a.drop_proof, compress=a.compress,
                  stream_gzip=a.stream_gzip)
    text = json.dumps(rec, indent=2)
    print(text)
    if a.o:
        with open(a.o, "w") as f:
            f.write(text + "\n")
    print(rec["result"])
    return 0 if rec.get("certified") else 1


if __name__ == "__main__":
    sys.exit(main())
