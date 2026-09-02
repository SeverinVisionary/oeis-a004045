#!/usr/bin/env python3
"""Certification driver for the 28 prime-order-symmetric orbit-ILPs of
SYMMETRY_THEOREM.md -- route 1 (RoundingSat + VeriPB).

    python3 symcert_certify.py --label p7_a1 --ub 63 --outdir certs_symmetry

Pipeline, all independent of symmetry_prime.py:
    symcert_reps.py + symcert_encode.py  ->  instance .opb
    roundingsat                          ->  VeriPB cutting-planes proof .pbp
    veripb -c                            ->  independent check (forced
                                              checked deletion)

Emits one JSON record per class with the statement certified, tool versions
and commit hashes, per-stage wall-clock, machine info, and size + SHA-256 of
both artifacts. A record is not a certificate until check.accepted is true.
"""
import argparse
import gzip
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
import symcert_encode  # noqa: E402
import symcert_reps  # noqa: E402


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


def git_commit(path):
    try:
        p = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"],
                            capture_output=True, text=True, timeout=30)
        return p.stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def machine():
    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "loadavg_1min_at_start": os.getloadavg()[0],
    }


def run_solver(solver, opb, pbp, budget, extra, stream_gzip=False):
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


def run_checker(checker, opb, pbp, budget):
    cmd = [checker, "-c", "--stats", opb, pbp]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=budget)
        out = (p.stdout + p.stderr).strip()
        rc = p.returncode
        expired = False
    except subprocess.TimeoutExpired as e:
        expired = True
        out = "".join(x.decode("utf-8", "replace") if isinstance(x, bytes) else (x or "")
                      for x in (e.stdout, e.stderr))
        rc = None
    dt = time.time() - t0
    verified = None
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("s VERIFIED UNSATISFIABLE"):
            verified = "UNSATISFIABLE"
        elif s.startswith("s VERIFIED"):
            verified = s[2:].strip()
    return {
        "command": " ".join(cmd),
        "exit_code": rc,
        "budget_expired": expired,
        "seconds": round(dt, 2),
        "output_tail": out.splitlines()[-20:],
        "checker_verdict": verified,
        "accepted": (not expired) and rc == 0 and verified == "UNSATISFIABLE",
    }


def certify_class(label, ub, outdir, solver, checker, budget, extra,
                   mu=2, stream_gzip=False):
    os.makedirs(outdir, exist_ok=True)
    stem = "%s_ub%d" % (label, ub)
    opb = os.path.join(outdir, "inst_%s.opb" % stem)
    pbp = os.path.join(outdir, "proof_%s.pbp" % stem)

    c = symcert_encode.find_class(label)
    meta = symcert_encode.write_opb(opb, c["label"], c["perm"], c["t"], c["orbits"], ub, mu)

    rec = {
        "statement": (
            "no union of <g>-orbits (g in conjugacy class %s, order %d, %d "
            "orbits on F_2^8) of total size <= %d is a mu=2 covering of Q_8"
            % (label, c["order"], c["n_orbits"], ub)),
        "label": label, "order": c["order"], "n_orbits": c["n_orbits"],
        "ub": ub, "mu": mu,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "machine": machine(),
        "instance": {
            "path": os.path.basename(opb),
            "variables": meta["variables"], "constraints": meta["constraints"],
            "bytes": meta["bytes"], "sha256": meta["sha256"],
        },
        "tools": {
            "encoder": "symcert_encode.py+symcert_reps.py sha256=%s+%s" % (
                sha256(os.path.join(HERE, "symcert_encode.py")),
                sha256(os.path.join(HERE, "symcert_reps.py"))),
            "solver": solver,
            "solver_version": version_of(solver, ["--help"])[:1],
            "solver_commit": git_commit(os.path.dirname(os.path.dirname(os.path.abspath(solver)))),
            "checker": checker,
            "checker_version": version_of(checker, ["--version"]),
            "checker_commit": git_commit(os.path.dirname(os.path.dirname(os.path.abspath(checker)))),
            "python": sys.version.split()[0],
        },
    }

    srec, verdict = run_solver(solver, opb, pbp, budget, extra, stream_gzip)
    rec["solve"] = srec
    if verdict != "UNSATISFIABLE":
        rec["result"] = "NOT ESTABLISHED (solver said %r, wanted 'UNSATISFIABLE')" % (verdict,)
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
        opener = lambda: open(pbp, "rb")  # noqa: E731
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
    rec["check"] = run_checker(checker, opb, pbp, budget)
    rec["certified"] = bool(rec["check"]["accepted"])
    rec["result"] = "VERIFIED" if rec["certified"] else "CHECKER REJECTED OR TIMED OUT"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--ub", type=int, default=63)
    ap.add_argument("--mu", type=int, default=2)
    ap.add_argument("--outdir", default=os.path.join(HERE, "certs_symmetry"))
    ap.add_argument("--solver", default=None)
    ap.add_argument("--checker", default=None)
    ap.add_argument("--budget", type=float, default=3600.0)
    ap.add_argument("--stream-gzip", action="store_true")
    ap.add_argument("--solver-arg", action="append", default=["--lp=-1"])
    ap.add_argument("-o", default=None)
    a = ap.parse_args()

    solver = tool(a.solver, "ROUNDINGSAT", "roundingsat")
    checker = tool(a.checker, "VERIPB", "veripb")
    for lbl, path in (("solver", solver), ("checker", checker)):
        if not path or not os.path.exists(path):
            print("missing %s binary (%r)" % (lbl, path), file=sys.stderr)
            return 2

    rec = certify_class(a.label, a.ub, a.outdir, solver, checker, a.budget,
                         a.solver_arg, mu=a.mu, stream_gzip=a.stream_gzip)
    text = json.dumps(rec, indent=2)
    print(text)
    if a.o:
        with open(a.o, "w") as f:
            f.write(text + "\n")
    print(rec["result"])
    return 0 if rec.get("certified") else 1


if __name__ == "__main__":
    sys.exit(main())
