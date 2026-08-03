# Hodos — the study record

**Live record:** https://xfloukiex-lab.github.io/hodos-study/

> A signal is a curve of probability distributions on a statistical manifold; comparison is a geodesic distance between curves.

By **Alexander Parnell · Vektorgeist · vektorgeist.com/research**

Papers of record: [The Afferent Gnosis Model: Self-Knowledge Without Self-Control](https://doi.org/10.5281/zenodo.21613153) · [The Vektorgeist Method: a Programme for Model-Free, Locally Sovereign AI](https://doi.org/10.5281/zenodo.21613155) · [Comparing Processes as Curves of Distributions](https://doi.org/10.5281/zenodo.21612829) · [Learning Without Weights](https://doi.org/10.5281/zenodo.21612831)

*This file is GENERATED from `manifest.json` by `gen_docs.py`. Do not edit it by hand — a hand-written summary is the first thing to go stale after a retraction, and then the most-read file in the repo is the one that is wrong.*

## Where the record stands

| Status | Count | Meaning |
|---|---:|---|
| Active | 14 | Survives the controls it was tested against; currently believed. |
| Provisional | 1 | Measured, but on one task or at small scale; not yet replicated. |
| Negative | 6 | Tested and did NOT hold. Reported because a negative is a result. |
| Retracted | 6 | We claimed it, then our own measurement refuted it. Original wording kept visible. |
| **Total** | **27** | |

**6 negative results and 6 retractions are in here on purpose.** A retraction keeps its original wording visible with the reason it was wrong next to it. `check.py` fails the build if a retraction carries no explanation — that would be a deletion, not a retraction.

## Confidence rungs

| Rung | What it takes |
|---:|---|
| 1 | reasoned, unmeasured |
| 2 | measured once, synthetic data |
| 3 | measured on real data, one modality |
| 4 | replicated on a second, unrelated modality |
| 5 | survives a fair control designed to kill it |
| 6 | survives comparison against a published method |
| 7 | reproduced independently, outside this project |

**Highest rung reached: 6. Nothing is at rung 7** — reproduced independently, outside this project. That is the gap, and it is the reason this is public.

## The equations

| § | Equation | Provenance |
|---:|---|---|
| 1 | The master distance | ASSEMBLED — the composition IS the contribution |
| 2 | The ground metrics, frame against frame | KNOWN |
| 3 | The sphere lemma — a process is literally a curve on a sphere | KNOWN, load-bearing framing |
| 4 | Geodesic operations on the sphere | KNOWN math, our operators |
| 5 | The temporal-pooling information-loss theorem | ASSEMBLED — downgraded from OURS on 2026-07-26 |
| 6 | The pitch / shift quotient | OURS — new extension |
| 7 | Instruments applied to the Riemann side | KNOWN — reproductions, NOT ours |

Read **ASSEMBLED** carefully — it is not a lesser category. Nearly every method in this field is a composition; §1 is ASSEMBLED and is where the invention lives.

## Findings

### Active

- **[27] The equation predicts the next step better than a trained network, with no training** — rung 5, 2026-07-24  
  Continuing the curve along its geodesic — a closed-form step with zero learned parameters — predicts the next frame of a real signal 3-16x more accurately than a matched dense network that was trained to do it.
- **[26] The learned character metric encodes linguistic class, and it is not frequency** — rung 3, 2026-07-26  
  Trained only to predict the next character, the model places characters on the simplex so that Fisher-Rao distance tracks linguistic class -- case pairs, vowels, sentence terminators, whitespace -- and this is not explained by how often the characters occur.
- **[25] The Fisher-Rao ground IS a better retrieval key than L2 -- once characters have a learned metric** — rung 5, 2026-07-26  
  Given character positions that carry a real metric, retrieving past contexts under the Hodos process distance predicts the next character better than retrieving under plain L2 over the identical frames. The only difference between the two arms is the distance function.
- **[21] An impossible value exposed a flaw that only a second dataset could reveal** — rung 5, 2026-07-26  
  A negative forgetting score — sequential beating joint — is impossible if the store is order-invariant, and chasing that impossibility found a real defect in the comparison.
- **[16] Anything between the landed point and the answer must start as a pass-through** — rung 5, 2026-07-25  
  A randomly-initialised readout layer costs ~21 perplexity — a 2.5× degradation — regardless of its form. Initialised as a pass-through, the cost vanishes entirely.
- **[14] It does not forget — and cannot, by construction** — rung 5, 2026-07-26  
  Taught classes in sequence, a standard network loses half to four-fifths of its first-task accuracy. This system loses nothing, because learning is appending to a store rather than overwriting weights.
- **[13] The geometry needs 5–10× less data than a standard network** — rung 4, 2026-07-25  
  Class-barycenter prototypes with NO training reach a standard method's 50-example accuracy using 5 examples (speech) or 10 (handwriting).
- **[12] The win decomposes: trajectory > ground > warp** — rung 4, 2026-07-24  
  The advantage over mean-pooling splits cleanly into three ingredients in a fixed order: using the trajectory at all, then the Fisher–Rao ground, then the alignment.
- **[11] Against a published method: the field's warp is better, our ground still wins** — rung 6, 2026-07-23  
  soft-DTW beats our hard-DTW warp — but the Fisher–Rao ground beats Euclidean under BOTH warps on BOTH modalities. The transferable contribution is the ground, and it composes with the field's better alignment.
- **[7] Pitch invariance by construction, not by training** — rung 5, 2026-07-22  
  Quotienting the process space by the global bin-shift group gives a distance between ORBITS, making recognition invariant to transposition exactly — not approximately, and with no examples required.
- **[6] The corrected boundary: two lanes, not one** — rung 3, 2026-07-24  
  The GROUND earns its keep wherever identity lives in the relative-space pattern — INCLUDING static posture. The WARP earns its keep only where identity lives in temporal motion. These are separate lanes; the earlier single-axis 'motion vs static' framing conflated them.
- **[4] The same win replicates on handwriting, with no audio at all** — rung 4, 2026-07-23  
  The identical claim holds on pen motion — a completely different modality — and more strongly than on speech.
- **[3] The information-geometry ground beats Euclidean on real speech across voices** — rung 3, 2026-07-23  
  Recognising the same spoken word through a DIFFERENT human voice, the Fisher–Rao ground reduces error ~17% vs Euclidean.
- **[1] A process is literally a curve on a sphere** — rung 5, 2026-07-21  
  The map p ↦ √p sends the simplex onto the unit sphere, under which Fisher–Rao becomes ordinary great-circle geometry. A signal over time is therefore a curve on a sphere, and comparing signals is comparing curves.

### Provisional

- **[2] Time-averaging is quadratically blind to a brief event** — rung 2, 2026-07-21  
  Averaging a signal over time loses a short event at O(ρ²) while the curve distance loses it at Θ(ρ) — so pooling destroys exactly what a process comparison keeps.

### Negative

- **[23] Character spacing is not Riemann level repulsion** — rung 5, 2026-07-25  
  The apparent 'empty band' in character separations is an artifact of one-hot encoding, not a repulsion signature.
- **[22] The Riemann work reproduces known mathematics and proves nothing new** — rung 5, 2026-07-22  
  The distance works as a REFEREE — it correctly ranks a quantum-chaotic drum closest to the real Riemann zeros — but every attempt to use it to find a load-bearing arithmetic operator returned a null.
- **[18] Hierarchy does not beat a flat representation** — rung 5, 2026-07-25  
  Lifting a trajectory into nested levels gives no advantage over the flat version on either modality.
- **[15] A compressed latent representation does NOT help** — rung 5, 2026-07-25  
  Squeezing characters onto a lower-dimensional concept simplex is monotonically worse, at matched parameters, with a working readout.
- **[10] Doppler / velocity measurement is not an edge** — rung 5, 2026-07-22  
  The conceptual link (Doppler is a time-warp, so the method should measure velocity) is real and elegant, but empirically purpose-built DSP measures it better.
- **[8] The distinctive ground does NOT generalise across light, echo and turbulence** — rung 5, 2026-07-22  
  The Fisher–Rao ground shows no edge over plain L2 on light spectra, sonar range-profiles or turbulence. It ties; it does not beat.

### Retracted

- **[24] Memory helps a language model, but the geometry is not why** — rung 5, 2026-07-25  
  ORIGINAL WORDING, NOW KNOWN TO BE WRONG: 'Retrieval is what helps; the geometric distance is not better than a flat one for this.'
  *Why it was wrong:* Both of these were measured in a space where the Fisher-Rao ground is a CONSTANT FUNCTION. Contexts were built as label-smoothed one-hot rows, and on the actual vocabulary (V=65, eps=0.03) the Fisher-Rao distance between every pair of distinct characters is identical: min 2.9971, mean 2.9971, max 2.9971 -- spread exactly 0.0000. In that space Fisher-Rao and L2 induce the SAME ranking, so 'the grou
- **[20] Measurement error: a growing label space looked like memory decaying** — rung 2, 2026-07-26  
  ORIGINAL WORDING, NOW KNOWN TO BE WRONG: 'the geometry forgets too — task-1 accuracy drops 0.500 as later tasks arrive.'
  *Why it was wrong:* In class-incremental learning the LABEL SPACE GROWS: task 1 is a 2-way choice when first learned and a 10-way choice at the end. Comparing those two numbers makes the task getting harder look like memory degrading. Measuring against the joint-trained ceiling makes the growing label space cancel, leaving only the cost of having learned in sequence — which for this system is exactly zero. The file's
- **[19] The geometry is not fp16-safe** — rung 1, 2026-07-24  
  ORIGINAL WORDING, NOW KNOWN TO BE WRONG: 'sph_log takes arccos of an inner product very close to 1.0; fp16 resolution there is coarser than the guard clamp, so every Log map collapses to zero and the geometry dies silently.'
  *Why it was wrong:* Both halves were wrong. The premise is BACKWARDS: characters are label-smoothed one-hots, so two DIFFERENT consecutive characters are nearly ORTHOGONAL (real-text mean inner product 0.096), nowhere near 1.0. The fp16 danger band contains 0.0000 of real pairs and zero pairs lose real motion. And naive autocast never reaches the geometry anyway — the manifold tensors come out float32. The 'safety' c
- **[17] On discrete aligned data the warp HURTS and the ground is neutral** — rung 5, 2026-07-25  
  ORIGINAL WORDING, NOW KNOWN TO BE WRONG: 'For character contexts, the Fisher-Rao ground ties plain L2 exactly, and the entire performance gap is the alignment machinery.'
  *Why it was wrong:* Both of these were measured in a space where the Fisher-Rao ground is a CONSTANT FUNCTION. Contexts were built as label-smoothed one-hot rows, and on the actual vocabulary (V=65, eps=0.03) the Fisher-Rao distance between every pair of distinct characters is identical: min 2.9971, mean 2.9971, max 2.9971 -- spread exactly 0.0000. In that space Fisher-Rao and L2 induce the SAME ranking, so 'the grou
- **[9] The min-mean distance 'win' was a padding degeneracy** — rung 5, 2026-07-22  
  ORIGINAL WORDING, NOW KNOWN TO BE WRONG: 'min-MEAN + Fisher–Rao beats standard DTW on light by +0.21 (0.61→0.82), and it survives 6→12/class.'
  *Why it was wrong:* min-mean degenerates into long, padded, cheap-repeat paths (path padding 0.00 for standard DTW vs 0.61 for min-mean) which makes it behave MORE like plain averaging (correlation with mean-pool 0.779 → 0.845). Light is precisely the task where averaging wins — so it 'won' for the wrong reason, and the same collapse HURT on echo where timing is the signal. The object is Marzal–Vidal's Normalized Edi
- **[5] The method fails where identity is static — the predicted boundary** — rung 3, 2026-07-23  
  ORIGINAL WORDING, NOW KNOWN TO BE WRONG: 'Fisher–Rao does not beat Euclidean on human-activity windows because activity identity in a short window is static — exactly what the principle predicts.'
  *Why it was wrong:* The adapter fed gravity-removed acceleration reduced to a MAGNITUDE — a representation with direction deleted. Sitting and standing are both 'at rest, no direction', so under that input they were identical BY CONSTRUCTION. The method was not failing on static identity; it was succeeding on an input from which the answer had already been removed. A null produced by a crippled representation is not 

## Running it

```
python build.py        # manifest -> docs/index.html
python check.py        # refuse to let the page disagree with the record
python gen_docs.py     # regenerate this README from the manifest
python lab/impostors.py  # seven cheating methods; the controls must catch all of them
```

## Layout

```
manifest.json   the single source of truth for what has been run and what is claimed
check.py        fails the build if the page and the record disagree
gen_docs.py     regenerates this README from the manifest
build.py        manifest -> docs/index.html
lab/            adversarial controls
results/        raw JSON emitted by the experiments
docs/           what GitHub Pages serves
```

## On the impostors

`lab/impostors.py` holds seven methods that deliberately cheat, and the controls have to catch every one before any measure here is trusted. The discipline is borrowed, with credit, from [Elifterminal/relational-metrics](https://github.com/Elifterminal/relational-metrics).

It is not decorative. This project has shipped two results that a cheating method would have predicted: a distance whose 'win' was a padding degeneracy (finding 9), and a comparison run in a space where the measure was a constant function — off-diagonal spread of exactly 0.0000 (findings 17 and 24). On its very first run the suite exposed a gap in our own control set, and a fifth control had to be written.

## Licence

Findings text CC-BY-4.0. Preprints are open access on Zenodo; see the study page.
