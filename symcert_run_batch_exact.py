#!/usr/bin/env python3
"""Run symcert_certify_exact.certify_class_exact over a list of classes,
in-process, writing one JSON record per class immediately as it finishes.

    SCIPEXACT=... VIPRCOMP=... VIPRCHK=... python3 symcert_run_batch_exact.py \
        --labels p3_a1,p2_a0_b7_c1 --budget 1800 --outdir certs_symmetry
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import symcert_certify_exact as sce  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--ub", type=int, default=63)
    ap.add_argument("--budget", type=float, default=1800.0)
    ap.add_argument("--outdir", default=os.path.join(HERE, "certs_symmetry"))
    ap.add_argument("--summary", default=None)
    a = ap.parse_args()

    scip = os.environ.get("SCIPEXACT") or "scip"
    viprcomp = os.environ.get("VIPRCOMP") or "viprcomp"
    viprchk = os.environ.get("VIPRCHK") or "viprchk"
    for lbl, path in (("scip", scip), ("viprcomp", viprcomp), ("viprchk", viprchk)):
        if not path or not os.path.exists(path):
            print("missing %s binary (%r)" % (lbl, path), file=sys.stderr)
            return 2

    labels = [x.strip() for x in a.labels.split(",") if x.strip()]
    os.makedirs(a.outdir, exist_ok=True)
    results = []
    for label in labels:
        t0 = time.time()
        print("=== %s (ub=%d, budget=%.0fs) ===" % (label, a.ub, a.budget), flush=True)
        rec_path = os.path.join(a.outdir, "cert_exact_%s_ub%d.json" % (label, a.ub))
        try:
            rec = sce.certify_class_exact(label, a.ub, a.outdir, scip, viprcomp, viprchk,
                                           a.budget, mu=2, compress=False)
        except Exception as e:  # noqa: BLE001
            rec = {"label": label, "ub": a.ub, "certified": False,
                   "result": "DRIVER EXCEPTION: %r" % (e,)}
        dt = time.time() - t0
        with open(rec_path, "w") as f:
            json.dump(rec, f, indent=2)
            f.write("\n")
        line = "%-16s ub=%-3d %-9s %8.2fs  %s" % (
            label, a.ub, "CERTIFIED" if rec.get("certified") else "NOT-CERT",
            dt, rec.get("result", ""))
        print(line, flush=True)
        if a.summary:
            with open(a.summary, "a") as f:
                f.write(line + "\n")
        results.append((label, rec.get("certified", False), dt))
    ok = sum(1 for _, c, _ in results if c)
    print("=== batch done: %d/%d certified ===" % (ok, len(results)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
