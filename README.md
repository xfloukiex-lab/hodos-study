# Hodos — the study record

**Live record:** https://xfloukiex-lab.github.io/hodos-study/

A working research log for Hodos: comparing processes as curves of distributions on a statistical
manifold. It contains negative results and retracted claims **on purpose** — as of the latest
build, 27 findings of which 6 are negative and 6 are retracted, with the original wording of every
retraction kept visible and the reason it was wrong stated next to it.

By **Alexander Parnell** · [Vektorgeist](https://vektorgeist.com)
Research programme: **https://vektorgeist.com/research**

Part of the Vektorgeist Method (VGM).

## How to read it

Four tabs. You land on the findings log rather than the theory, which is deliberate.

| Tab | What it is |
|---|---|
| **Findings** | the chronological record, newest first, including everything retracted |
| **The equations** | all seven sections, each labelled ASSEMBLED / KNOWN / OURS |
| **How the tests work** | the rules, and the specific mistake each one was written after |
| **The thesis** | what the project actually claims, and what it does not |

Read **ASSEMBLED** carefully — it is not a lesser category. Nearly every method in this field is a
composition; §1, the Hodos distance itself, is ASSEMBLED, and the composition is the contribution.

## Confidence rungs

Findings carry a rung from 1 (reasoned, unmeasured) to 7 (reproduced independently, outside this
project).

**Nothing here is at rung 7.** That is the gap, it is stated on the record itself, and it is the
reason any of this is public.

## What is in this repository

Only the study record: the manifest, the builder, the consistency checker, and the generated page.
The engine source, the tests and the preprints live elsewhere.

    manifest.json   the single source of truth — every number on the page is generated from it
    build.py        manifest -> docs/index.html
    check.py        refuses to let the page disagree with the record
    docs/           what GitHub Pages serves

`check.py` enforces, among other things, that a retraction must carry an explanation — a retraction
with no reason is a deletion, not a retraction — and that a finding claiming to supersede another
is named by that other in return.

Some `code` paths in the manifest point into the private engine repository and cannot be verified
from this copy. `check.py` **reports** those as unverifiable rather than silently skipping them: a
check that quietly does nothing is worse than no check.

## Reproducing it locally

    python build.py && python check.py

No dependencies beyond the standard library.
