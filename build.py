"""Build the Hodos study site from manifest.json. LOCAL ONLY — nothing here publishes.

The design is adapted from a relational-metrics reference site, whose structural idea is the good
one: the MANIFEST is the single source of truth, and every number on the page — including the
summary counts — is generated from it, so the summary cannot drift out of date. There is no
hand-written HTML holding a stale figure.

Three tabs, and you land on the running log rather than the theory:
    findings   the chronological record, including everything we retracted
    method     how the tests work, and why the rules exist
    thesis     what the project actually claims

    python study/build.py     -> docs/index.html
    python study/serve.py     -> http://localhost:8800
"""
from __future__ import annotations

import html
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

STATUS_ORDER = ["active", "provisional", "negative", "retracted", "untested"]
STATUS_CLASS = {"active": "ok", "provisional": "prov", "negative": "neg",
                "retracted": "ret", "untested": "unt"}

CSS = """
:root{
  --bg:#0f1417; --panel:#161d21; --line:#243036; --ink:#dfe7ea; --dim:#8ea3ac;
  --ok:#4fbf87; --prov:#d2a24c; --neg:#7f97a3; --ret:#d4685f; --unt:#5c6f79; --acc:#5aa9c9;
}
@media(prefers-color-scheme:light){
  :root{ --bg:#f7f9fa; --panel:#fff; --line:#dde5e9; --ink:#17242a; --dim:#5d727c; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.65 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:960px;margin:0 auto;padding:0 22px 80px}
header{border-bottom:1px solid var(--line);margin-bottom:0;padding:34px 0 0}
h1{margin:0 0 4px;font-size:27px;letter-spacing:-.3px}
.sub{color:var(--dim);margin:0 0 4px}
.byline{color:var(--dim);font-size:13px;margin:0 0 18px}
.private{background:#3a2320;border:1px solid #6d3a33;color:#f0c9c3;
  padding:9px 13px;border-radius:7px;font-size:13px;margin:14px 0 20px}
nav{display:flex;gap:2px;margin-top:8px}
nav button{background:none;border:0;border-bottom:2px solid transparent;color:var(--dim);
  padding:10px 15px;font:inherit;font-size:14px;cursor:pointer}
nav button.on{color:var(--ink);border-bottom-color:var(--acc)}
nav button:hover{color:var(--ink)}
section{display:none;padding-top:26px}
section.on{display:block}
.counts{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px}
.pill{border:1px solid var(--line);border-radius:20px;padding:4px 13px;font-size:13px;
  background:var(--panel)}
.pill b{font-variant-numeric:tabular-nums}
.gen{color:var(--dim);font-size:12px;margin:0 0 22px}
.tracks{border:1px solid var(--line);border-radius:9px;padding:12px 14px;margin:0 0 20px}
.tlab{color:var(--dim);font-size:13px;margin-right:8px}
.tf{border:1px solid var(--line);background:transparent;color:var(--fg);border-radius:20px;
padding:4px 13px;font-size:13px;cursor:pointer;margin:4px 4px 0 0;font-family:inherit}
.tf.on{border-color:var(--acc);color:var(--acc);font-weight:600}
.tdesc{color:var(--dim);font-size:13px;margin:10px 0 0;line-height:1.5}
.trk{font-size:11px;border-radius:20px;padding:2px 9px;margin-left:8px;vertical-align:2px;
border:1px solid var(--line);color:var(--dim);font-weight:600;white-space:nowrap}
.trk.t-clinical-rhythm{border-color:#b3261e;color:#b3261e}
.trk.t-beyond-weights{border-color:var(--acc);color:var(--acc)}
tr.hide,div.f.hide{display:none}
table{width:100%;border-collapse:collapse;margin:0 0 26px;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--dim);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.4px}
td.n{font-variant-numeric:tabular-nums;color:var(--dim);width:34px}
.tag{font-size:11px;padding:2px 8px;border-radius:20px;border:1px solid;white-space:nowrap;
  text-transform:uppercase;letter-spacing:.4px}
.tag.ok{color:var(--ok);border-color:var(--ok)} .tag.prov{color:var(--prov);border-color:var(--prov)}
.tag.neg{color:var(--neg);border-color:var(--neg)} .tag.ret{color:var(--ret);border-color:var(--ret)}
.tag.unt{color:var(--unt);border-color:var(--unt)}
.f{border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:17px 19px;
  margin:0 0 15px}
.f.ret{border-color:#6d3a33}
.f h3{margin:0 0 3px;font-size:16.5px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.f h3 .id{color:var(--dim);font-variant-numeric:tabular-nums;font-weight:400;font-size:14px}
.meta{color:var(--dim);font-size:12.5px;margin:0 0 11px}
.lab{color:var(--dim);font-size:11.5px;text-transform:uppercase;letter-spacing:.5px;
  margin:12px 0 2px}
.f p{margin:0}
.eqtag{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0 0 10px}
.eqtag.own{color:var(--ok);font-weight:700}
.eqf{background:#11171b;border:1px solid var(--line);border-radius:6px;padding:12px 14px;
  margin:0 0 12px;overflow-x:auto;font-size:12.5px;line-height:1.65;white-space:pre;
  font-family:'Cascadia Code',Consolas,monospace;color:#cfe0e6}
.eqprov{color:var(--dim);font-size:13.5px}
.retr{background:#3a2320;border-left:3px solid var(--ret);padding:11px 14px;margin:12px 0 0;
  border-radius:0 6px 6px 0}
.note{border-left:3px solid var(--acc);padding:9px 14px;margin:12px 0 0;color:var(--dim);
  background:rgba(90,169,201,.06);border-radius:0 6px 6px 0}
ul.ctl{margin:3px 0 0;padding-left:19px} ul.ctl li{margin:2px 0}
code{background:rgba(127,151,163,.16);padding:1px 5px;border-radius:4px;font-size:12.5px}
.rung{color:var(--dim);font-size:12px}
h2{font-size:19px;margin:30px 0 10px;padding-bottom:7px;border-bottom:1px solid var(--line)}
h2:first-child{margin-top:0}
.lede{font-size:16px;color:var(--ink)}
"""

JS = """
// Track filter: a reader who came for one line of work should be able to see only that line.
document.querySelectorAll('.tf').forEach(b=>b.onclick=()=>{
  const t=b.dataset.t;
  document.querySelectorAll('.tf').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  document.querySelectorAll('#findings tbody tr, #findings div.f').forEach(el=>{
    const own=el.dataset.track||'';
    el.classList.toggle('hide', t!=='all' && own!==t);
  });
});
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('section').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  document.getElementById(b.dataset.t).classList.add('on');
  location.hash = b.dataset.t;
});
const h=location.hash.slice(1);
if(h && document.getElementById(h)){
  document.querySelector('nav button.on').classList.remove('on');
  document.querySelector('section.on').classList.remove('on');
  document.querySelector(`nav button[data-t="${h}"]`).classList.add('on');
  document.getElementById(h).classList.add('on');
}
"""


def e(x):
    return html.escape(str(x))


TRACK_LABEL = {"beyond-weights": "architecture", "clinical-rhythm": "cardiac rhythm"}


def finding_card(f, rungs):
    cls = STATUS_CLASS[f["status"]]
    trk = f.get("track", "")
    parts = [f'<div class="f {"ret" if f["status"]=="retracted" else ""}" data-track="{e(trk)}">']
    tlab = (f'<span class="trk t-{e(trk)}">{e(TRACK_LABEL.get(trk, trk))}</span>' if trk else "")
    parts.append(f'<h3><span class="id">{f["id"]}</span>{e(f["title"])}{tlab}'
                 f'<span class="tag {cls}">{e(f["status"])}</span></h3>')
    rung = f.get("rung")
    rtxt = f' · rung {rung} — {e(rungs.get(str(rung), ""))}' if rung else ""
    parts.append(f'<p class="meta">{e(f["date"])}{rtxt}</p>')

    parts.append(f'<p class="lab">Claim</p><p>{e(f["claim"])}</p>')
    if f.get("evidence"):
        parts.append(f'<p class="lab">Evidence</p><p>{e(f["evidence"])}</p>')
    if f.get("scope"):
        parts.append(f'<p class="lab">Scope / limits</p><p>{e(f["scope"])}</p>')
    if f.get("controls"):
        items = "".join(f"<li>{e(c)}</li>" for c in f["controls"])
        parts.append(f'<p class="lab">Controls that could have killed it</p><ul class="ctl">{items}</ul>')
    if f.get("retraction"):
        parts.append(f'<div class="retr"><p class="lab">Why this was wrong</p>'
                     f'<p>{e(f["retraction"])}</p></div>')
    if f.get("note"):
        parts.append(f'<div class="note">{e(f["note"])}</div>')

    tail = []
    if f.get("code"):
        tail.append(f'<code>{e(f["code"])}</code>')
    if f.get("result_file"):
        tail.append(f'<code>{e(f["result_file"])}</code>')
    if f.get("supersedes"):
        tail.append(f'supersedes finding {f["supersedes"]}')
    if f.get("superseded_by"):
        tail.append(f'superseded by finding {f["superseded_by"]}')
    if tail:
        parts.append(f'<p class="meta" style="margin-top:13px">{" · ".join(tail)}</p>')
    parts.append("</div>")
    return "".join(parts)


def build():
    m = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    fs = m["findings"]
    counts = Counter(f["status"] for f in fs)
    rungs = m.get("rungs", {})

    # ---- counts, generated FROM the manifest so this line cannot go stale
    pills = "".join(
        f'<span class="pill"><span class="tag {STATUS_CLASS[s]}">{s}</span> <b>{counts.get(s,0)}</b></span>'
        for s in STATUS_ORDER if counts.get(s))
    pills += f'<span class="pill">total <b>{len(fs)}</b></span>'

    # ---- the status matrix
    rows = "".join(
        f'<tr data-track="{e(f.get("track",""))}"><td class="n">{f["id"]}</td>'
        f'<td>{e(f["title"])}'
        + (f'<span class="trk t-{e(f["track"])}">{e(TRACK_LABEL.get(f["track"], f["track"]))}'
           f'</span>' if f.get("track") else "")
        + f'</td>'
        f'<td><span class="tag {STATUS_CLASS[f["status"]]}">{f["status"]}</span></td>'
        f'<td class="rung">{f.get("rung","–")}</td>'
        f'<td>{e(f["date"])}</td></tr>'
        for f in fs)

    cards = "".join(finding_card(f, rungs) for f in sorted(fs, key=lambda x: -x["id"]))

    # The equations tab. Tags come straight from EQUATIONS.md and are NOT softened on the way
    # here -- ASSEMBLED / KNOWN / OURS being stated plainly is the entire point of that sheet.
    def equation_card(q):
        # NB: not class="tag"/"prov" — those are the status-pill styles and would render these
        # paragraphs as bordered pills.
        own = "OURS" in q["tag"]
        bits = [f'<h3><span class="id">§{q["n"]}</span> {e(q["title"])}</h3>',
                f'<p class="eqtag{" own" if own else ""}">{e(q["tag"])}</p>',
                f'<pre class="eqf">{e(q["formula"])}</pre>',
                f'<p><b>Plain:</b> {e(q["plain"])}</p>',
                f'<p class="eqprov"><b>Provenance:</b> {e(q["provenance"])}</p>']
        if q.get("correction"):
            bits.append(f'<p class="retr"><b>Correction:</b> {e(q["correction"])}</p>')
        return '<div class="f">' + "".join(bits) + "</div>"

    eqs = "".join(equation_card(q) for q in m.get("equations", {}).get("items", []))

    meanings = "".join(f'<tr><td><span class="tag {STATUS_CLASS[k]}">{k}</span></td>'
                       f'<td>{e(v)}</td></tr>' for k, v in m["status_meanings"].items())
    rung_rows = "".join(f'<tr><td class="n">{k}</td><td>{e(v)}</td></tr>'
                        for k, v in sorted(rungs.items()))

    n_ret = counts.get("retracted", 0)
    n_neg = counts.get("negative", 0)

    # ---- track intro: a reader from one field should not have to wade through the other
    n_clin = sum(1 for f in fs if f.get("track") == "clinical-rhythm")
    n_arch = sum(1 for f in fs if f.get("track") == "beyond-weights")
    track_intro = (
        f"<b>Cardiac rhythm</b> ({n_clin} findings) — per-patient detection of atrial "
        f"fibrillation from inter-beat intervals. Read these if you came for the medical work; "
        f"they stand on their own. &nbsp;·&nbsp; <b>Architecture</b> ({n_arch} findings) — the "
        f"memory-based learning method the cardiac work is built on, measured on speech. "
        f"&nbsp;·&nbsp; The remaining findings are the underlying distance itself, tested on "
        f"speech, handwriting and other signals. "
        f"<b>A result in one line is not a claim about another.</b>")

    # ---- papers of record: the DOIs this record underpins, clickable from the byline
    papers_line = ""
    if m.get("papers"):
        links = " · ".join(
            f'<a href="https://doi.org/{e(p["doi"])}">{e(p["title"])}</a>' for p in m["papers"])
        papers_line = f'<p class="byline">Papers of record: {links}</p>'

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(m['project'])} — study record</title><style>{CSS}</style></head><body>
<div class="wrap">
<header>
  <h1>{e(m['project'])}</h1>
  <p class="sub">{e(m['subtitle'])}</p>
  <p class="byline">{e(m['byline'])}</p>
  {papers_line}
  <div class="private">PRIVATE — {e(m['private_note'])}</div>
  <nav>
    <button class="on" data-t="findings">Findings</button>
    <button data-t="equations">The equations</button>
    <button data-t="method">How the tests work</button>
    <button data-t="thesis">The thesis</button>
  </nav>
</header>

<section id="findings" class="on">
  <div class="counts">{pills}</div>
  <div class="tracks">
    <span class="tlab">This record covers two separate lines of work:</span>
    <button class="tf on" data-t="all">show both</button>
    <button class="tf" data-t="clinical-rhythm">cardiac rhythm only</button>
    <button class="tf" data-t="beyond-weights">architecture only</button>
    <p class="tdesc" id="tdesc">{track_intro}</p>
  </div>
  <p class="gen">Counts and the table below are generated from <code>manifest.json</code>, so they
     cannot disagree with the record. Newest finding: {max(f['date'] for f in fs)}.</p>
  <table><thead><tr><th></th><th>Finding</th><th>Status</th><th>Rung</th><th>Date</th></tr></thead>
  <tbody>{rows}</tbody></table>
  <h2>The record, newest first</h2>
  {cards}
</section>

<section id="equations">
  <h2>Every equation, with an honest label on each</h2>
  <p class="lede">{e(m.get('equations', {}).get('lede', ''))}</p>
  <p class="gen">{e(m.get('equations', {}).get('notation', ''))}</p>
  {eqs}
  <h2>The one-paragraph honest summary</h2>
  <p>{e(m.get('equations', {}).get('summary', ''))}</p>
</section>

<section id="method">
  <h2>The rules, and why each one exists</h2>
  <p class="lede">Every rule here was written after something went wrong. They are not general
     good practice; they are scar tissue.</p>

  <h2>Write the criterion before running the test</h2>
  <p>A test whose bar is set afterwards can always be read as a success. Finding 13 predicted that
     the advantage would <em>shrink</em> with data — the signature of a prior. It grew instead. That
     makes it a better representation rather than a better prior: a different claim, and one we
     would have described wrongly had the criterion not been fixed in advance.</p>

  <h2>Build the control that can kill the result</h2>
  <p>Findings 8, 9, 18 and 22 were all killed by a control built for that purpose. Finding 18's
     smoothing arm matched the result exactly, which is what ended it. A benchmark with no arm
     capable of producing a negative is a demonstration, not a test.</p>

  <h2>Design the test to exercise the mechanism</h2>
  <p>Findings 5 and 19 both passed on inputs that could not have shown the effect. The activity
     adapter deleted direction, so two postures were identical by construction. The fp16 test used
     random data that never approaches the regime in question. <strong>A null from a crippled input
     is not a boundary.</strong></p>

  <h2>An unexplained win is a red flag</h2>
  <p>Finding 9 won on one modality and lost on another with no account of why. Investigating the
     mechanism showed it was collapsing toward plain averaging — which is exactly why it won on the
     task where averaging wins. Explain the mechanism before banking the win.</p>

  <h2>Distinguish "measured nothing" from "could not measure"</h2>
  <p>Finding 23 returned a statistic that was identically zero for the real data and for all 900
     shuffled controls. A z of zero against a null with zero spread is a dead instrument, not a null
     result. It is reported as a failed measurement.</p>

  <h2>An impossible number is worth chasing even when the headline is good</h2>
  <p>Finding 21 reported a <em>negative</em> forgetting score, which cannot happen if the store is
     order-independent. Chasing it found a real defect — and fixing it made the opposing method look
     worse, meaning the bug had been flattering the opponent.</p>

  <h2>Replicate on a second, unrelated modality</h2>
  <p>Speech and handwriting share no sensor, no physics and no preprocessing. Finding 4 is what
     turned finding 3 from a sound trick into a claim. And per finding 21, a second dataset is not
     only confirmation — it is a different defect detector.</p>

  <h2>Retractions stay visible</h2>
  <p>{n_ret} findings on this page are retracted, with the original wording kept and labelled.
     {n_neg} more are outright negatives. Deleting them would make the record look stronger and be
     worth less.</p>

  <h2>Status meanings</h2>
  <table><tbody>{meanings}</tbody></table>

  <h2>Confidence rungs</h2>
  <table><thead><tr><th></th><th>What it takes</th></tr></thead><tbody>{rung_rows}</tbody></table>
</section>

<section id="thesis">
  <h2>What this claims</h2>
  <p class="lede">{e(m['one_line'])}</p>

  <h2>The narrow version, which is the one that survived</h2>
  <p>The <strong>ground</strong> — the information-geometry representation, not the alignment
     machinery — is what earns a measurable advantage, and it does so wherever identity lives in the
     relative-space pattern of a process. The <strong>warp</strong> is a separate lane: it earns its
     keep only where identity lives in temporal motion, and on discrete already-aligned data it
     actively hurts (finding 17).</p>
  <p>These are two lanes. Conflating them was our own error, retracted as finding 5 and corrected in
     finding 6.</p>

  <h2>What it is good at, stated as capabilities</h2>
  <p><strong>It learns from 5–10× less data</strong> than a matched standard network, on two
     unrelated modalities (finding 13). At one example the network is barely above chance.</p>
  <p><strong>It does not forget</strong> (finding 14). Taught in sequence, a standard network loses
     half to four-fifths of what it first learned. This loses nothing — and cannot, because building
     the store in reverse order yields byte-identical answers, so the final state provably does not
     depend on the sequence.</p>
  <p><strong>It is invariant by construction</strong> rather than by training (finding 7). A
     transposed signal collapses 61× while a genuinely different one is preserved. A network has to
     learn that from examples and only ever approximates it.</p>

  <h2>What it costs</h2>
  <p>The store grows. Consolidation folds repeated episodes into one prototype per concept, so it
     scales with how many distinct things are known rather than with how much has been seen — but
     lookup gets slower as it learns, where a network's does not. That is the real trade, and it is
     why a fast retrieval index exists.</p>

  <h2>What it is not</h2>
  <p>Not a universal oracle. It solves what can be posed as a least-cost path on a
     distribution-manifold; it does not invent a domain's law and does not reach discrete or logical
     truths. The Riemann work (finding 22) reproduces known mathematics and proves nothing new.</p>
  <p>Not better on language. Memory helps a language model, but a plain distance retrieves better
     than this one for text (finding 24), and the mechanism is understood (finding 17).</p>
  <p>Not novel wholesale. Dynamic time warping, Fisher–Rao, the square-root sphere, soft-DTW,
     barycenter averaging and optimal transport are all prior art, reused. What is ours is the
     synthesis, the pitch quotient, and the measurements on this page.</p>
</section>

</div><script>{JS}</script></body></html>"""

    out = HERE / "docs"   # Pages only serves / or /docs
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(doc, encoding="utf-8")

    print(f"built {out / 'index.html'}")
    print(f"  {len(fs)} findings: " + ", ".join(
        f"{counts[s]} {s}" for s in STATUS_ORDER if counts.get(s)))
    return out / "index.html"


if __name__ == "__main__":
    build()
