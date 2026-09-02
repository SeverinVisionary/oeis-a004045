#!/usr/bin/env python3
"""Mandatory over-constraint control (see SYMMETRY_THEOREM.md / task spec):
for a hard class, encode the SAME instance at ub=64 with symcert_encode.py,
solve it (scipy.optimize.milp / HiGHS -- independent of symmetry_prime.py's
raw highspy call and of the RoundingSat/VeriPB certification route), extract
a genuine 256-bit code from the selected orbits, check it is closed under g
by direct simulation, and run it through verify.py (stdlib only, shares no
solver code with anything else in this directory).

If ub=64 comes back infeasible too, the encoding is wrong -- this script
raises rather than silently reporting a control failure as a pass.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from scipy.optimize import LinearConstraint, milp, Bounds
from scipy.sparse import csr_matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import symcert_encode  # noqa: E402
import symcert_reps  # noqa: E402


def solve_feasibility(c, ub, mu=2):
    """Solve the orbit-ILP for `c` at cardinality <= ub with scipy/HiGHS.
    Returns (feasible, selected_orbit_indices) -- independent of
    symmetry_prime.solve_class and of RoundingSat.
    """
    orbs = c["orbits"]
    k = len(orbs)
    idx = symcert_encode.orbit_index_map(orbs)
    sizes = [len(o) for o in orbs]

    data, ri, ci, lb = [], [], [], []
    row = 0
    for v in range(symcert_encode.UNIVERSE):
        counts = {}
        for w in symcert_encode.ball(v):
            oi = idx[w]
            counts[oi] = counts.get(oi, 0) + 1
        for oi, cnt in counts.items():
            data.append(cnt)
            ri.append(row)
            ci.append(oi)
        lb.append(mu)
        row += 1
    for oi in range(k):
        data.append(-sizes[oi])
        ri.append(row)
        ci.append(oi)
    lb.append(-ub)
    row += 1

    A = csr_matrix((data, (ri, ci)), shape=(row, k))
    lb = np.array(lb, dtype=float)
    ub_arr = np.full(row, np.inf)
    constraints = LinearConstraint(A, lb, ub_arr)
    bounds = Bounds(0, 1)
    integrality = np.ones(k)
    obj = np.zeros(k)
    res = milp(obj, constraints=constraints, bounds=bounds, integrality=integrality)
    if not res.success:
        return False, None
    selected = [i for i in range(k) if res.x[i] > 0.5]
    return True, selected


def check_g_invariant(code, perm, t):
    code_set = set(code)
    for v in code_set:
        if symcert_reps.act(perm, t, v) not in code_set:
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--ub", type=int, default=64)
    ap.add_argument("--mu", type=int, default=2)
    ap.add_argument("--verify-py", default=os.path.join(HERE, "verify.py"))
    ap.add_argument("--outdir", default=os.path.join(HERE, "logs"))
    a = ap.parse_args()

    c = symcert_encode.find_class(a.label)
    feasible, selected = solve_feasibility(c, a.ub, a.mu)
    report = {"label": a.label, "ub": a.ub, "mu": a.mu, "order": c["order"],
              "n_orbits": c["n_orbits"]}
    if not feasible:
        report["feasible_at_ub"] = False
        report["FATAL"] = ("ub=%d came back infeasible for class %s -- the encoding "
                            "is wrong; do not trust the ub<=63 refutation for this "
                            "class or any other until this is fixed." % (a.ub, a.label))
        print(json.dumps(report, indent=2))
        return 1

    code = symcert_encode.orbit_code_from_selection(c["orbits"], selected)
    report["feasible_at_ub"] = True
    report["selected_orbits"] = len(selected)
    report["code_size"] = len(code)
    report["g_invariant"] = check_g_invariant(code, c["perm"], c["t"])

    os.makedirs(a.outdir, exist_ok=True)
    code_path = os.path.join(a.outdir, "control_inv%d_%dorbits_%s.json" % (a.ub, c["n_orbits"], a.label))
    with open(code_path, "w") as f:
        json.dump(code, f)
    report["code_path"] = code_path

    p = subprocess.run([sys.executable, a.verify_py, code_path, "-n", "8", "--mu", str(a.mu)],
                        capture_output=True, text=True)
    report["verify_py_command"] = "python3 verify.py %s -n 8 --mu %d" % (code_path, a.mu)
    report["verify_py_stdout"] = p.stdout.strip()
    report["verify_py_exit_code"] = p.returncode
    report["verify_py_valid"] = (p.returncode == 0)

    print(json.dumps(report, indent=2))
    ok = report["g_invariant"] and report["verify_py_valid"]
    print("CONTROL " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
