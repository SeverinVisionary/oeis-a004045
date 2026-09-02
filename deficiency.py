#!/usr/bin/env python3
"""The deficiency inequality |C| >= 64 - D/8, and a check that it is not wrong.

DERIVATION. Let C subset F_2^8 be a mu=2 covering of Q_8: every one of the 256
words has at least two members of C in its closed radius-1 ball. Count the edge
endpoints leaving C, writing e(C,C) for edges inside C and e(C, V\\C) for edges
from C to its complement:

    8|C| = 2 e(C,C) + e(C, V\\C).

Every NON-codeword v needs two codeword neighbours (its ball contributes no
codeword at distance 0), so

    e(C, V\\C) >= 2 (256 - |C|).

For u in C write d(u) for its number of codeword neighbours, and define the
DEFICIENCY

    D = sum_{u in C} max(0, 2 - d(u)),   whence   2 e(C,C) = sum d(u) >= 2|C| - D.

Substituting both bounds:

    8|C| >= (2|C| - D) + 2(256 - |C|) = 512 - D,     so     |C| >= 64 - D/8.

TWO SHARPENINGS (verified below).

First, d(u) >= 1 is FORCED, so no codeword is isolated: coverage at a codeword
reads c(u) = 1 + d(u) >= 2 directly. Hence the max(0, .) never sees a d(u) = 0
term and D counts exactly the codewords of induced-degree one:

    D = n_1 := #{u in C : d(u) = 1}.

Second, the counting is an IDENTITY, not merely an inequality. Write
s = sum_{u in C} max(0, d(u) - 2) for surplus degree inside C, and
a = sum_{v not in C} (c(v) - 2) for coverage excess outside C. Then

    8|C| + n_1 = 512 + s + a,      s, a >= 0,

so n_1 = 512 + s + a - 8|C| >= 512 - 8|C|, which is the inequality above with
D = n_1. Keeping s and a explicit says where any slack goes, and the identity
is what makes the statement checkable rather than merely true.

WHY THIS IS WORTH WRITING DOWN. The inequality is tight on the known 64-word
code, where every codeword has exactly two codeword neighbours (D = 0, so C
induces a disjoint union of cycles in Q_8) and the bound returns exactly 64. It
converts "is there a covering smaller than 64?" into a structural question with
no search in it:

    |C| = 63  requires  n_1 >= 8    (13% of its codewords)
    |C| = 62  requires  n_1 >= 16   (26%)
    |C| = 61  requires  n_1 >= 24   (39%)
    |C| = 60  requires  n_1 >= 32   (53%)
    n_1 = 0   forces    |C| >= 64.

Read the last two lines slowly. A 60-word covering needs MORE THAN HALF of its
codewords to have exactly one codeword neighbour -- that is, the subgraph C
induces in Q_8 must be more than half degree-one vertices, close to a matching.
The published 64-word code is the opposite extreme: 2-regular, a disjoint union
of cycles.

So proving that no mu=2 covering of Q_8 has deficiency D >= 8 would give
|C| >= 64 - 7/8 > 63, hence |C| >= 64, and would settle K(8,1,2) = 64 outright
-- replacing a 6.47 GB certificate per rung with a structural argument.

HONESTY. The counting here is elementary and is the standard excess argument
for multiple coverings specialised to (n, mu) = (8, 2); it is very likely known
in some form, and nothing is claimed as new. Its value is the reformulation:
it names the single quantity that any sub-64 covering must pay for.

    python3 deficiency.py            # verify on the known code + random coverings
"""
import json
import os
import random
import sys

N = 8
HERE = os.path.dirname(os.path.abspath(__file__))


def ball(v):
    return [v] + [v ^ (1 << i) for i in range(N)]


def analyse(S):
    """Return (|C|, n_1, bound) for S, or None if S is not a mu=2 covering.

    Also asserts the identity 8|C| + n_1 = 512 + s + a on every input.
    """
    S = set(S)
    if any(sum(1 for u in ball(v) if u in S) < 2 for v in range(1 << N)):
        return None
    degree = {u: sum(1 for w in ball(u)[1:] if w in S) for u in S}
    if any(d == 0 for d in degree.values()):
        raise AssertionError("isolated codeword in a mu=2 covering: impossible, "
                             "since c(u) = 1 + d(u) >= 2 forces d(u) >= 1")
    n1 = sum(1 for d in degree.values() if d == 1)
    surplus = sum(max(0, d - 2) for d in degree.values())
    excess = sum(sum(1 for u in ball(v) if u in S) - 2
                 for v in range(1 << N) if v not in S)
    # the identity, asserted rather than assumed
    assert 8 * len(S) + n1 == 512 + surplus + excess, "counting identity failed"
    return len(S), n1, 64 - n1 / 8.0


def main():
    path = os.path.join(HERE, "code64.json")
    code = json.load(open(path))
    code = code["code"] if isinstance(code, dict) and "code" in code else code
    got = analyse([int(w) for w in code])
    if got is None:
        print("code64.json is not a valid mu=2 covering", file=sys.stderr)
        return 1
    size, deficiency, bound = got
    print("known code: |C|=%d  n_1=%d  bound=%.2f  tight=%s"
          % (size, deficiency, bound, size == bound))
    if deficiency != 0 or size != 64:
        print("expected D=0 and |C|=64 for the published code", file=sys.stderr)
        return 1

    random.seed(11)
    tested = 0
    for _ in range(400):
        S = set(random.sample(range(1 << N), random.randint(60, 110)))
        for _ in range(600):
            bad = [v for v in range(1 << N)
                   if sum(1 for u in ball(v) if u in S) < 2]
            if not bad:
                break
            v = random.choice(bad)
            S.add(random.choice([u for u in ball(v) if u not in S]))
        got = analyse(S)
        if got is None:
            continue
        tested += 1
        size, deficiency, bound = got
        if size < bound - 1e-9:
            print("VIOLATION: |C|=%d n_1=%d bound=%.2f" % (size, deficiency, bound),
                  file=sys.stderr)
            return 1
    print("checked %d further coverings, no violation" % tested)
    return 0


if __name__ == "__main__":
    sys.exit(main())
