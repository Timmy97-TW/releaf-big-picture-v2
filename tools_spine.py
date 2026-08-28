#!/usr/bin/env python3
"""Rewrite the five-step spine of index.html from the one table below.

The twenty-nine pieces of work, which step each feeds, the label, the mark, the
alt text and the cross-links all live HERE, in one readable table, and the
markup is generated from it. Editing the HTML by hand is how a figure this size
drifts: a tile gets renamed in one place and not the other, or a data-with
points at an id that no longer exists. Change the table, run this, commit both.

The tile ARTWORK is a separate job — see tools_tiles.sh, which cuts every one of
these out of its source photograph or figure. The keys match.

  run: python3 tools_spine.py
"""
import re, os, html

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
src = open(P, encoding="utf-8").read()

# keep the MD animation verbatim — 46 frames of our own trajectory live in its
# data-frames attribute and nothing here should retype them
m = re.search(r'<figure class="task__shot">\s*<svg class="mdanim".*?</figure>', src, re.S)
MD_FIGURE = m.group(0)

# key, label, icon, alt, cross-links[, True if this one leads its step]
# The alt carries the date and the honest limit. Every step's own limit — the
# sentence that used to sit on the plate — is on `note` and is written onto the
# plate's title attribute, so dropping it from the page did not drop it from the
# document.
NODES = [
 dict(n=1, icon="i-field", name="The stress",
      note="Heat and salt. The smallest farms sit where they are worst.",
      L=[
        ("sensing","Stress sensing electronics","i-board",
         "Our sensing bench: a temperature and humidity sensor wired to a board that trips the light on a threshold. There is no trained model behind this and no forecast.", "t-genedesign t-lightarray"),
        ("agar","Stress tests with Arabidopsis","i-dish",
         "Two Arabidopsis agar boxes held up to the light in our lab, 5 July 2026. Salt and heat, on plates.", "t-rigs t-stressindex"),
        ("rigs","Hydroponic and soil rigs","i-tray",
         "Prototype 4 of the hydroponic tray, the version that germinated 100% after the seedlings were moved across from agar.", "t-agar t-tandemrun"),
      ],
      R=[
        ("farmers","Learning from farmers","i-field",
         "\u9673\u60e0\u96ef on her knees in her plot, showing two of us the soil, 21 July 2026.", "t-realfarms t-experts t-cost", True),
        ("stressindex","Stress index modelling","i-model",
         "Temperature and humidity read out as one stress index. Deterministic meteorology, not a forecast, and the link from index to dose is still open.", "t-agar t-transport"),
        ("taiwan","Taiwan geospatial analysis","i-taiwan",
         "Our QGIS layer: farm parcels under two hectares drawn over five bands of climate volatility, west coast.", "t-dataphys t-cost"),
        ("dataphys","Data physicalisation","i-diopal",
         "Our data physicalisation model: the stress record built as an object you can stand in front of rather than a chart you scroll past.", "t-taiwan t-stressindex"),
      ]),

 dict(n=2, icon="i-peptide", name="The protein",
      note="One of three, chosen against that stress. Not yet made.",
      L=[
        ("msa","Multiple sequence alignment","i-again",
         "Our alignment of BoPep4 against the eight Arabidopsis Peps. The invariant C-terminal SSG..G..N core is the receptor-binding motif, and BoPep4 carries it intact.", "t-docking t-codon"),
        ("docking","Protein docking","i-insilico",
         "Our HADDOCK result: BoPep4 (blue) superposed on the AtPep1 crystal control (orange) in the PEPR1 groove after receptor alignment. The two track each other across the conserved C terminus.", "t-md t-msa", True),
      ],
      R=[
        ("md","Molecular dynamics","i-peptide", None, "t-docking t-genedesign"),
      ]),

 dict(n=3, icon="i-culture", name="The cells",
      note="B. subtilis, engineered to make it and let it out. No output measured.",
      L=[
        ("signalp","Signal peptide screen","i-insilico",
         "The secretion end of the design: which signal peptide gets BoPep4 out of the cell, and where the peptidase cuts it.", "t-cassette t-genedesign"),
        ("codon","Codon optimisation, ViennaRNA","i-insilico",
         "Our ViennaRNA minimum-free-energy fold of the BoPep4 translation-initiation window. Recoding codons 1\u201315 opened the ribosome binding site: SD core accessibility 0.067 to 0.641.", "t-cassette t-signalp"),
        ("genedesign","Light-gated circuit design","i-led",
         "Our four-module design: haem to PCB, CcaS sensing green light, CcaR driving transcription, and the protectant leaving through the membrane. Every parameter is still a literature value.", "t-lightarray t-cassette t-md", True),
      ],
      R=[
        ("cassette","Expression cassettes ordered","i-construct",
         "The construct map we ordered against: SamyQ signal peptide, tag and BoPep4 block by block, with the signal-peptidase cut marked.", "t-codon t-cloning"),
        ("cloning","Cloning into B. subtilis","i-construct",
         "The cloning bench: the constructs going into competent cells and out onto selection.", "t-cassette t-sequencing"),
        ("sequencing","Sanger clone verification","i-blot",
         "Bands on the transilluminator, 10 June 2026. Behind them, our own ABIF reader and per-part k-mer libraries across 117 reads and 61 clones.", "t-cloning t-growth"),
        ("growth","B. subtilis growth tests","i-culture",
         "434 hours of B. subtilis 168 at 22 \u00b0C on our own in-line photometer, 2 671 readings. The amber band is where the instrument's reference channel was failing and it recorded that itself.", "t-photometer t-tandemrun"),
      ]),

 dict(n=4, icon="i-reactor", name="The bioreactor",
      note="Ours, built from nothing. It has never stood at a farm.",
      L=[
        ("membrane","Hollow fibre membrane","i-shield",
         "The hollow fibre cartridge on its own. It is the containment boundary: cells stay in, protein crosses.", "t-pressure t-law"),
        ("photometer","In-line OD600 photometer","i-photometer",
         "Our photometer under test, its lamp visible inside the box, 4 July 2026. It caught its own four-fold overestimate and we traced it to an un-cleanable blank.", "t-growth t-tandemrun"),
        ("tandemrun","Reactor and plants in tandem","i-tandem",
         "The reactor running in the incubator with the plants on the floor above it, 20 July 2026. The two have never been connected.", "t-rigs t-photometer t-transport", True),
      ],
      R=[
        ("lightarray","Light plate apparatus","i-diopal",
         "The light array, first assembled with its printed housing, 17 July 2026. Three independent channels at 31, 63 and 100 per cent duty.", "t-genedesign t-sensing"),
        ("pressure","Pressure across the membrane","i-gauge",
         "The transmembrane pressure sensor. The pulsation it reads is the peristaltic pump, confirmed by an expert.", "t-membrane t-dosensor"),
        ("phsensor","pH sensor","i-board",
         "The pH probe. Wired and reading; not yet calibrated or logged through a run.", "t-dosensor t-pressure"),
        ("dosensor","DO sensor","i-board",
         "The dissolved oxygen probe. Wired and reading; not yet calibrated or logged through a run.", "t-phsensor t-pressure"),
      ]),

 dict(n=5, icon="i-tandem", name="The field",
      note="The dose arrives where the crop is. No plant has had one.",
      L=[
        ("law","Regulation pathway","i-law",
         "Three jurisdictions this has to be legal on: Taiwan, the United States, the European Union. Taiwan is the one we have asked, and BAPHIQ has not answered.", "t-membrane t-cost"),
        ("transport","Permeate transport model","i-model",
         "A modelled concentration field through the module: how far the protectant gets once it has crossed the membrane. Computed, never measured.", "t-tandemrun t-stressindex"),
      ],
      R=[
        ("realfarms","Vertical farm visit","i-tray",
         "All of us looking up at the wall of hydroponics at \u6e90\u9bae, 11 August 2026.", "t-farmers t-rigs", True),
        ("experts","Industry pitch","i-log",
         "Prof \u9673\u6587\u4eae talking us through the reactor, 20 June 2026. Every architecture decision on this page traces to a named person.", "t-tandemrun t-farmers"),
        ("cost","Entrepreneurship pitch with industry","i-plan",
         "Talking our way through the design with CH Biotech's researchers, in front of the protectant products they already sell, 9 July 2026.", "t-law t-taiwan"),
      ]),
]

MARK = ('<span class="task__label"><span class="task__mark">'
        '<svg class="ico" viewBox="0 0 32 32" aria-hidden="true"><use href="#{ico}"/></svg>'
        '</span><span class="task__name">{label}</span></span>')

def tile(t, n, ind):
    key, label, ico, alt, with_ = t[0], t[1], t[2], t[3], t[4]
    lead = " data-lead" if len(t) > 5 and t[5] else ""
    cls = "task task--md" if key == "md" else "task"
    if key == "md":
        fig = MD_FIGURE
    else:
        fig = ('<figure class="task__shot"><img src="assets/img/tile/%s.webp"\n%s     '
               'loading="lazy" decoding="async" alt="%s" /></figure>'
               % (key, ind, html.escape(alt, quote=True)))
    return ('%s<div class="%s"%s id="t-%s" tabindex="0" data-at="%d" data-with="%s">\n'
            '%s  %s\n%s  %s\n%s</div>'
            % (ind, cls, lead, key, n, with_, ind, fig, ind, MARK.format(ico=ico, label=label), ind))

out = ['      <div class="chain">']
for i, nd in enumerate(NODES):
    I = "            "
    out.append('        <div class="node" data-node="%d">' % nd["n"])
    out.append('          <div class="strip strip--l">')
    out += [tile(t, nd["n"], I) for t in nd["L"]]
    out.append('          </div>')
    out.append('          <div class="node__core" tabindex="0" title="%s">' % html.escape(nd["note"], quote=True))
    out.append('            <span class="well"><svg class="ico" viewBox="0 0 32 32" aria-hidden="true"><use href="#%s"/></svg></span>' % nd["icon"])
    out.append('            <span>')
    out.append('              <span class="node__name">%s</span>' % nd["name"])
    out.append('            </span>')
    out.append('          </div>')
    out.append('          <div class="strip strip--r">')
    out += [tile(t, nd["n"], I) for t in nd["R"]]
    out.append('          </div>')
    out.append('        </div>')
    if i < len(NODES) - 1:
        out.append('        <div class="link" data-seg="%d"><span class="link__rail"></span></div>' % nd["n"])
out.append('        <div class="link link--tail" aria-hidden="true"><span class="link__rail"></span></div>')
out.append('      </div>')
chain = "\n".join(out)

a = src.index('      <div class="chain">')
b = src.index('    </div>\n  </div>\n</section>', a)
src = src[:a] + chain + "\n" + src[b:]
src = src.replace('<h2 class="band__title" id="bpv2-title">The whole project, in five steps.</h2>',
                  '<h2 class="band__title" id="bpv2-title">The whole ReLeaf project.</h2>')
open(P, "w", encoding="utf-8").write(src)
print("spine rewritten:", sum(len(n["L"]) + len(n["R"]) for n in NODES), "tiles")
