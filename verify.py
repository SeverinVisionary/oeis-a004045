#!/usr/bin/env python3
"""Standalone verifier for binary mu-fold radius-1 coverings.

Independent of every search model in this directory: standard library only, no
shared helpers, takes a code as data.

    python3 verify.py code64.json            # verify a code file (n inferred)
    python3 verify.py --incumbent            # rebuild and verify the 64-word incumbent
    python3 verify.py code.json --mu 2 -n 8
"""
import argparse
import json
import sys


def coverage(code, n):
    """cov[v] = number of codewords within Hamming distance 1 of v."""
    cov = [0] * (1 << n)
    for c in code:
        cov[c] += 1
        for i in range(n):
            cov[c ^ (1 << i)] += 1
    return cov


def verify(code, n, mu):
    """Return (ok, report). A code is a list of distinct ints in [0, 2^n)."""
    problems = []
    if len(set(code)) != len(code):
        problems.append("codewords are not distinct (K(n,r,mu) is defined on sets)")
    if any(not (0 <= c < (1 << n)) for c in code):
        problems.append("codeword outside F_2^%d" % n)
    if problems:
        return False, {"problems": problems}
    cov = coverage(code, n)
    uncovered = [v for v, k in enumerate(cov) if k < mu]
    profile = {}
    for k in cov:
        profile[k] = profile.get(k, 0) + 1
    report = {
        "n": n,
        "mu": mu,
        "size": len(code),
        "sphere_bound": -(-(mu << n) // (n + 1)),
        "excess": (n + 1) * len(code) - mu * (1 << n),
        "coverage_profile": {k: profile[k] for k in sorted(profile)},
        "deficient_words": len(uncovered),
    }
    return not uncovered, report


def hamming_7():
    """The [7,4,3] Hamming code as 16 integers (columns = syndromes 1..7)."""
    H = [1, 2, 3, 4, 5, 6, 7]
    out = []
    for c in range(1 << 7):
        if all(sum(((c >> j) & 1) * ((H[j] >> b) & 1) for j in range(7)) % 2 == 0
               for b in range(3)):
            out.append(c)
    return out


def incumbent_64():
    """C0 u (C0 + e1) with C0 = H_7 x F_2: the published upper-bound witness."""
    c0 = [c | (b << 7) for c in hamming_7() for b in (0, 1)]
    return sorted(set(c0) | set(c ^ 1 for c in c0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code", nargs="?", help="JSON file holding a list of ints")
    ap.add_argument("--incumbent", action="store_true",
                    help="rebuild the 64-word incumbent instead of reading a file")
    ap.add_argument("-n", type=int, default=None)
    ap.add_argument("--mu", type=int, default=2)
    a = ap.parse_args()

    if a.incumbent:
        code = incumbent_64()
        assert len(hamming_7()) == 16
    elif a.code:
        code = json.load(open(a.code))
    else:
        ap.error("give a code file or --incumbent")

    n = a.n if a.n is not None else max(1, max(code).bit_length())
    while (1 << n) <= max(code):
        n += 1
    ok, report = verify(code, n, a.mu)
    print(json.dumps(report, indent=2))
    print("VALID" if ok else "INVALID")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
