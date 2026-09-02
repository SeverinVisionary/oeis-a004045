#!/usr/bin/env python3
"""Route 2 for the prime-order-symmetric orbit-ILPs: exact-rational SCIP ->
VIPR certificate -> viprcomp -> viprchk. Same architecture as
certify_exact.py, over symcert_encode.py's instances instead of pb_encode.py's.

    SCIPEXACT=... VIPRCOMP=... VIPRCHK=... python3 symcert_certify_exact.py \
        --label p2_a1_b6_c0 --ub 63 --outdir certs_symmetry --budget 7200

Requires a SCIP built with -DEXACTSOLVE=ON -DLPSEXACT=spx and the maintained
github.com/scipopt/vipr (not the archived ambros-gleixner one). See
CERTIFICATION.md Sec.5 for why both of those are load-bearing.
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
import vipr_bind  # noqa: E402


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
        "cpu_count": os.cpu_count(),
        "loadavg_1min_at_start": os.getloadavg()[0],
    }


def _certificate_bytes(vipr):
    total = 0
    for suffix in ("", "_der", "_ori"):
        p = vipr + suffix
        if os.path.exists(p):
            total += os.path.getsize(p)
    return total


def run_scip(scip, opb, vipr, budget, threads=1, max_cert_mb=4000):
    """Solve in exact mode, but also watch disk: SCIP's uncommitted
    certificate (.vipr + working .vipr_der) has been observed growing past
    7-8 GB on instances that do not close within the time budget anyway, on
    a machine with a low double-digit GB of free disk. Kill the solve early
    if the certificate crosses max_cert_mb, rather than let one hard class
    fill the disk and take the rest of the run down with it.
    """
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
    # stdout goes to a real file, not subprocess.PIPE: SCIP's periodic display
    # lines exceed the OS pipe's 64 KB capacity within tens of minutes on any
    # instance that runs for hours, and nothing here drains a PIPE while
    # polling p.wait() -- that combination deadlocks the child in write() well
    # before the time budget, silently freezing the solve (0% CPU) while wall
    # clock keeps advancing toward the external kill. Observed directly on
    # this instance. A file has no such capacity limit.
    log_path = vipr + ".scip_stdout.log"
    logf = open(log_path, "w")
    p = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT)
    disk_killed = False
    # SCIP's own "set limits time" has been observed NOT to bound wall-clock
    # tightly in exact mode on these instances -- one run needed the full
    # budget+600s grace before it noticed, which defeated the point of a
    # short triage budget. Enforce the deadline ourselves; give only a
    # small (20s) allowance for it to exit cleanly after crossing it.
    deadline = t0 + budget
    grace = 20
    threshold = max_cert_mb << 20
    while True:
        try:
            p.wait(timeout=5)
            break
        except subprocess.TimeoutExpired:
            if _certificate_bytes(vipr) > threshold:
                disk_killed = True
                p.kill()
                p.wait()
                break
            if time.time() > deadline + grace:
                p.kill()
                p.wait()
                break
    logf.close()
    with open(log_path) as f:
        out = f.read()
    os.unlink(log_path)
    rc = p.returncode
    dt = time.time() - t0
    status = None
    for line in out.splitlines():
        if line.startswith("SCIP Status"):
            status = line.split(":", 1)[1].strip()
    if disk_killed:
        status = ("ABORTED: certificate exceeded %d MB after %.0f s "
                   "(disk-safety kill, not a time limit)" % (max_cert_mb, dt))
        expired = True
    elif status is None:
        status = "BUDGET EXPIRED after %.0f s (no SCIP status line seen)" % dt
        expired = True
    else:
        expired = "time limit reached" in status.lower()
    return {
        "command": " ".join('"%s"' % c if " " in c else c for c in cmd),
        "exit_code": rc,
        "budget_expired": expired,
        "seconds": round(dt, 2),
        "scip_status": status,
        "stdout_tail": out.strip().splitlines()[-30:],
    }, status


def run_viprcomp(viprcomp, vipr, budget):
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


def certify_class_exact(label, ub, outdir, scip, viprcomp, viprchk, budget,
                         mu=2, compress=False, drop_large_mb=50):
    os.makedirs(outdir, exist_ok=True)
    stem = "%s_ub%d" % (label, ub)
    opb = os.path.join(outdir, "inst_%s.opb" % stem)
    vipr = os.path.join(outdir, "cert_exact_%s.vipr" % stem)

    c = symcert_encode.find_class(label)
    meta = symcert_encode.write_opb(opb, c["label"], c["perm"], c["t"], c["orbits"], ub, mu)

    rec = {
        "statement": (
            "no union of <g>-orbits (g in conjugacy class %s, order %d, %d "
            "orbits on F_2^8) of total size <= %d is a mu=2 covering of Q_8"
            % (label, c["order"], c["n_orbits"], ub)),
        "route": "exact-rational MILP (SCIP) -> VIPR certificate -> viprcomp -> viprchk",
        "label": label, "order": c["order"], "n_orbits": c["n_orbits"],
        "ub": ub, "mu": mu,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "machine": machine(),
        "instance": {
            "path": os.path.basename(opb),
            "variables": meta["variables"], "constraints": meta["constraints"],
            "bytes": meta["bytes"], "sha256": meta["sha256"],
        },
        "tools": {"scip": scip, "viprcomp": viprcomp, "viprchk": viprchk,
                  "python": sys.version.split()[0]},
    }

    srec, status = run_scip(scip, opb, vipr, budget)
    rec["solve"] = srec
    if not status or "infeasible" not in status.lower():
        rec["result"] = "NOT REFUTED (SCIP status %r)" % status
        rec["certified"] = False
        # An interrupted exact solve can leave a partial certificate (.vipr)
        # plus SCIP's working .vipr_der -- observed at 7-8 GB on instances
        # that time out, on a machine with a low double-digit GB of free
        # disk. Record the size, then reclaim the disk; there is nothing
        # checkable in an incomplete certificate anyway.
        leftover_bytes = _certificate_bytes(vipr)
        if leftover_bytes:
            rec["solve"]["leftover_certificate_bytes_deleted"] = leftover_bytes
            for suffix in ("", "_der", "_ori"):
                p = vipr + suffix
                if os.path.exists(p):
                    os.unlink(p)
        return rec
    if not os.path.exists(vipr):
        rec["result"] = "NO CERTIFICATE EMITTED"
        rec["certified"] = False
        return rec

    rec["certificate"] = {
        "path": os.path.basename(vipr),
        "bytes": os.path.getsize(vipr),
        "sha256": sha256(vipr),
    }

    # viprchk is invoked as `viprchk cert.vipr` and never sees the .opb, so on
    # its own it proves infeasibility of whatever problem the certificate's own
    # header states. Bind that header to our instance here, on the uncompleted
    # .vipr SCIP wrote, before any cleanup or size-based dropping can remove it.
    t0 = time.time()
    try:
        problems = vipr_bind.check(opb, vipr)
        rec["binding"] = {
            "checked": True,
            "bound": not problems,
            "problems": problems,
            "seconds": round(time.time() - t0, 2),
        }
    except Exception as e:  # noqa: BLE001
        import traceback
        rec["binding"] = {
            "checked": False,
            "bound": False,
            "problems": ["vipr_bind raised %r" % (e,)],
            "traceback": traceback.format_exc().splitlines()[-12:],
            "seconds": round(time.time() - t0, 2),
        }

    crec, done = run_viprcomp(viprcomp, vipr, budget)
    rec["complete"] = crec
    if not crec["completed_path"]:
        rec["result"] = "COMPLETION FAILED"
        rec["certified"] = False
        if os.path.exists(vipr) and os.path.getsize(vipr) > (drop_large_mb << 20):
            os.unlink(vipr)
            rec["certificate"]["path"] = "<deleted after failed completion; sha256/bytes above>"
        return rec
    rec["complete"]["bytes"] = os.path.getsize(done)
    rec["complete"]["sha256"] = sha256(done)
    rec["check"] = run_viprchk(viprchk, done, budget)
    # Both halves are needed: viprchk says the certificate proves the problem in
    # its own header infeasible, and the binding check says that problem is our
    # instance. Either alone is not a refutation of this class.
    accepted = bool(rec["check"]["accepted"])
    bound = bool(rec.get("binding", {}).get("bound"))
    rec["certified"] = accepted and bound
    if rec["certified"]:
        rec["result"] = "VERIFIED"
    elif accepted and not bound:
        rec["result"] = ("CHECKER ACCEPTED BUT CERTIFICATE NOT BOUND TO INSTANCE: %s"
                         % "; ".join(rec.get("binding", {}).get("problems", []))[:400])
    elif bound and not accepted:
        rec["result"] = "CHECKER REJECTED"
    else:
        rec["result"] = "CHECKER REJECTED AND NOT BOUND TO INSTANCE"

    if compress and rec["certified"]:
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

    # VIPR certificates for these instances run into the hundreds of MB to
    # low GB -- far past the 50 MB commit limit. Once checked, the hash and
    # size already in `rec` are the durable record; the raw bytes are
    # disposable (and regenerable from the command in `rec`), so drop
    # anything over the threshold rather than let it pile up on disk across
    # a 28-class run.
    threshold = drop_large_mb << 20
    candidates = [(vipr, "certificate")]
    if compress and rec["certified"]:
        candidates.append((done + ".gz", "complete"))
    else:
        candidates.append((done, "complete"))
    for p, key in candidates:
        if p and os.path.exists(p) and os.path.getsize(p) > threshold:
            os.unlink(p)
            rec[key]["path"] = "<deleted, over %d MB; sha256/bytes above, " \
                "regenerate with the command in this record>" % drop_large_mb
        ori = p + "_ori" if p else None
        if ori and os.path.exists(ori):
            os.unlink(ori)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--ub", type=int, default=63)
    ap.add_argument("--mu", type=int, default=2)
    ap.add_argument("--outdir", default=os.path.join(HERE, "certs_symmetry"))
    ap.add_argument("--scip", default=None)
    ap.add_argument("--viprcomp", default=None)
    ap.add_argument("--viprchk", default=None)
    ap.add_argument("--budget", type=float, default=3600.0)
    ap.add_argument("--compress", action="store_true")
    ap.add_argument("-o", default=None)
    a = ap.parse_args()

    scip = a.scip or os.environ.get("SCIPEXACT") or shutil.which("scip")
    viprcomp = a.viprcomp or os.environ.get("VIPRCOMP") or shutil.which("viprcomp")
    viprchk = a.viprchk or os.environ.get("VIPRCHK") or shutil.which("viprchk")
    for lbl, path in (("scip", scip), ("viprcomp", viprcomp), ("viprchk", viprchk)):
        if not path or not os.path.exists(path):
            print("missing %s binary (%r)" % (lbl, path), file=sys.stderr)
            return 2

    rec = certify_class_exact(a.label, a.ub, a.outdir, scip, viprcomp, viprchk,
                               a.budget, mu=a.mu, compress=a.compress)
    text = json.dumps(rec, indent=2)
    print(text)
    if a.o:
        with open(a.o, "w") as f:
            f.write(text + "\n")
    print(rec["result"])
    return 0 if rec.get("certified") else 1


if __name__ == "__main__":
    sys.exit(main())
