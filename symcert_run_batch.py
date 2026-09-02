#!/usr/bin/env python3
"""Run symcert_certify.certify_class over a list of classes, in-process
(avoids per-class subprocess/import overhead), writing one JSON record per
class immediately as it finishes so progress survives an interrupt.

    ROUNDINGSAT=... VERIPB=... python3 symcert_run_batch.py \
        --labels p7_a1,p5_a1,p3_a2 --budget 1800 --outdir certs_symmetry
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import symcert_certify as sc  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True, help="comma-separated class labels")
    ap.add_argument("--ub", type=int, default=63)
    ap.add_argument("--budget", type=float, default=1800.0)
    ap.add_argument("--outdir", default=os.path.join(HERE, "certs_symmetry"))
    ap.add_argument("--summary", default=None, help="append a one-line-per-class summary here")
    a = ap.parse_args()

    solver = sc.tool(None, "ROUNDINGSAT", "roundingsat")
    checker = sc.tool(None, "VERIPB", "veripb")
    for lbl, path in (("solver", solver), ("checker", checker)):
        if not path or not os.path.exists(path):
            print("missing %s binary (%r)" % (lbl, path), file=sys.stderr)
            return 2

    labels = a.labels.split(",")
    os.makedirs(a.outdir, exist_ok=True)
    results = []
    for label in labels:
        label = label.strip()
        if not label:
            continue
        t0 = time.time()
        print("=== %s (ub=%d, budget=%.0fs) ===" % (label, a.ub, a.budget), flush=True)
        rec_path = os.path.join(a.outdir, "cert_%s_ub%d.json" % (label, a.ub))
        try:
            rec = sc.certify_class(label, a.ub, a.outdir, solver, checker, a.budget,
                                    ["--lp=-1"], mu=2, stream_gzip=False)
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
