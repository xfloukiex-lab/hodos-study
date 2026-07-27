"""Seven methods that CHEAT. The controls must catch every one before any measure is trusted.

Borrowed, with credit, from the discipline in Elifterminal/relational-metrics, whose lab keeps a
suite of deliberately-cheating methods and requires the controls to catch all of them. The failure
mode it guards against is specific to relational/geometric frameworks: loose criteria produce
striking-looking correspondences that mean nothing, and you cannot tell from the number alone.

Hodos has already been bitten by exactly this class, twice, which is why this file exists rather
than being a nice idea:

  - Finding 9: the min-mean distance's "distinctive win" was a padding degeneracy. The optimum
    padded the alignment path with cheap repeats and collapsed toward plain averaging. It looked
    like a result for weeks.
  - Findings 17/24: a comparison run in a space where the Fisher-Rao distance between every pair
    of distinct characters is IDENTICAL (off-diagonal spread exactly 0.0000). The measure was a
    constant function, so the experiment was arithmetic wearing the costume of a measurement.

Each impostor below is a plausible-looking method that should NOT pass. A control that fails to
catch one is not a control.

    python lab/impostors.py
"""
from __future__ import annotations

import numpy as np

RNG = np.random.default_rng(0)


# ---------------------------------------------------------------- the impostors
def imp_constant(a, b):
    """I-1 CONSTANT. Returns the same number for every pair.

    The finding-17 failure exactly: a measure with zero dynamic range. It will happily produce a
    'no significant difference' result forever, and a naive reading calls that a null.
    """
    return 1.0


def imp_noise(a, b):
    """I-2 PURE NOISE. Ignores the inputs entirely."""
    return float(RNG.random())


def imp_length_only(a, b):
    """I-3 LENGTH-ONLY. Looks only at how long the sequences are.

    On corpora where class correlates with duration this scores well while knowing nothing about
    content -- the classic confound that a per-class accuracy table hides.
    """
    return abs(len(a) - len(b)) + 0.0


def imp_first_frame(a, b):
    """I-4 FIRST FRAME ONLY. Discards the entire trajectory after t=0.

    If this ties the real measure, the task never needed a process representation and the whole
    premise of the paper does not apply to it.
    """
    return float(np.abs(np.asarray(a)[0] - np.asarray(b)[0]).sum())


def imp_mean_pool(a, b):
    """I-5 MEAN POOL. Averages time away, then compares.

    The specific baseline Hodos exists to beat. If it wins, the geometry is not earning its keep,
    and a retrieval 'signature' that reduces to this is a mean-pool in disguise -- which is what
    the first version of our retrieval index actually was.
    """
    return float(np.abs(np.asarray(a).mean(0) - np.asarray(b).mean(0)).sum())


def imp_padding_gamer(a, b):
    """I-6 PADDING GAMER. Rewards alignments that pad with cheap repeats.

    Reproduces finding 9's degeneracy: minimise the MEAN cost along the path and the optimum
    stuffs the path with free repeats until it collapses toward averaging. Its 'win' was an
    artifact of the objective, not a property of the data.
    """
    A, B = np.asarray(a), np.asarray(b)
    n = max(len(A), len(B)) * 8                      # pad generously, then take the mean
    return float(np.abs(A.mean(0) - B.mean(0)).sum() * len(A) / n)


def imp_label_leak(a, b, _labels={}):
    """I-7 LABEL LEAK. Peeks at an identifier that encodes the answer.

    Stands in for every accidental leak: an index that correlates with class, a cache key built
    from the label, a train/test split done after feature extraction.
    """
    ka, kb = id(a) % 10, id(b) % 10
    return 0.0 if ka == kb else 1.0


IMPOSTORS = [
    ("I-1 constant", imp_constant),
    ("I-2 noise", imp_noise),
    ("I-3 length-only", imp_length_only),
    ("I-4 first-frame", imp_first_frame),
    ("I-5 mean-pool", imp_mean_pool),
    ("I-6 padding-gamer", imp_padding_gamer),
    ("I-7 label-leak", imp_label_leak),
]


# ---------------------------------------------------------------- the controls
def control_dynamic_range(measure, samples):
    """C-1 DYNAMIC RANGE. A measure whose spread is ~0 measured nothing.

    This is the control that findings 17 and 24 did not have. Had it been in place, the
    off-diagonal spread of exactly 0.0000 would have failed the run instead of producing a
    publishable-looking null.
    """
    vals = [measure(a, b) for a, b in samples]
    spread = float(np.max(vals) - np.min(vals))
    return spread > 1e-6, f"spread {spread:.2e}"


def control_identity(measure, samples):
    """C-2 IDENTITY. d(x,x) must be ~0 and strictly below d(x,y) for x != y."""
    a = samples[0][0]
    self_d = measure(a, a)
    other = np.median([measure(x, y) for x, y in samples])
    return self_d < other - 1e-9, f"self {self_d:.4f} vs other {other:.4f}"


def control_determinism(measure, samples):
    """C-3 DETERMINISM. The same pair twice must give the same number."""
    a, b = samples[0]
    return abs(measure(a, b) - measure(a, b)) < 1e-12, "repeat call differs"


def control_permutation(measure, samples):
    """C-4 PERMUTATION NULL. Shuffling time must degrade a process measure.

    A measure indifferent to temporal order is not measuring a process -- it is measuring a bag
    of frames, which is what I-5 does openly and what a bad signature does secretly.
    """
    real = np.median([measure(a, b) for a, b in samples])
    shuf = np.median([measure(RNG.permutation(np.asarray(a)),
                              RNG.permutation(np.asarray(b))) for a, b in samples])
    return abs(shuf - real) > 1e-9, f"ordered {real:.4f} vs shuffled {shuf:.4f}"


def control_tail_sensitivity(measure, samples):
    """C-5 TAIL SENSITIVITY. Changing the sequence AFTER the first frame must change the measure.

    ADDED 2026-07-26, on the suite's first run, because I-4 (first-frame-only) walked past all
    four original controls untouched. A measure that reads only t=0 is order-invariant, perfectly
    deterministic, has real dynamic range, and satisfies identity -- it passes everything the
    other controls ask, while ignoring the entire trajectory.

    That is precisely the value of keeping deliberately-cheating methods around: the gap was in
    OUR control set, and nothing else would have shown it.
    """
    changed = 0
    for a, b in samples[:12]:
        A = np.asarray(a, dtype=float).copy()
        before = measure(A, b)
        A[1:] = A[1:][::-1]                          # disturb only the tail, never frame 0
        if abs(measure(A, b) - before) > 1e-9:
            changed += 1
    return changed > 0, f"tail changes moved the measure on {changed}/12 pairs"


CONTROLS = [("C-1 dynamic-range", control_dynamic_range),
            ("C-2 identity", control_identity),
            ("C-3 determinism", control_determinism),
            ("C-4 permutation", control_permutation),
            ("C-5 tail-sensitivity", control_tail_sensitivity)]


def make_samples(n=24, T=12, F=6):
    out = []
    for _ in range(n):
        a = np.abs(RNG.normal(size=(T, F))) + 0.05
        b = np.abs(RNG.normal(size=(T, F))) + 0.05
        out.append((a / a.sum(1, keepdims=True), b / b.sum(1, keepdims=True)))
    return out


def main():
    samples = make_samples()
    print("=" * 74)
    print("IMPOSTOR SUITE — every cheating method must be caught by at least one control")
    print("=" * 74)
    all_caught = True
    for name, measure in IMPOSTORS:
        caught_by = []
        for cname, control in CONTROLS:
            try:
                ok, detail = control(measure, samples)
            except Exception as e:
                ok, detail = False, f"raised {type(e).__name__}"
            if not ok:
                caught_by.append(f"{cname} ({detail})")
        status = "CAUGHT" if caught_by else "*** SLIPPED THROUGH ***"
        print(f"\n  {name:20s} {status}")
        for c in caught_by:
            print(f"       caught by {c}")
        if not caught_by:
            all_caught = False

    print()
    print("=" * 74)
    print("ALL SEVEN CAUGHT" if all_caught
          else "AN IMPOSTOR SURVIVED — the control set is incomplete, do not trust a result")
    return 0 if all_caught else 1


if __name__ == "__main__":
    raise SystemExit(main())
