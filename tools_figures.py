#!/usr/bin/env python3
"""Draw the three tiles that have no photograph and no existing figure.

Each one is generated from OUR OWN data or our own facts, in the wiki palette,
with no axes, no title block and no legend — at 120px a chart's chrome is noise
and its shape is the whole message. tools_tiles.sh rasterises what this writes.

  run: python3 tools_figures.py [outdir]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assets", "img", "gen")
os.makedirs(OUT, exist_ok=True)

LEAF9, LEAF7, LEAF5, LEAF2 = "#14402b", "#23684a", "#4f9c6f", "#cfe4d8"
AMBER, RUST, SLATE, GRAY4 = "#92610c", "#9a3d22", "#3f5468", "#a3a3a3"


def write(name, svg):
    p = os.path.join(OUT, name)
    open(p, "w", encoding="utf-8").write(svg)
    print("wrote", p)


# ── 1. the 434-hour growth curve ─────────────────────────────────────────────
# Straight out of the Prof. Chang page's own dataset: B. subtilis 168 at 22 °C
# on our in-line photometer, 2 671 valid readings at 10-minute intervals. No
# axes: the shape IS the claim (lag, two growth phases, plateau, decline), and
# the amber band is the window where the photometer's reference channel was
# failing — the run where the instrument recorded when to distrust itself.
def growth():
    src = os.path.join(ROOT, "0822_ProfChang_Update", "site", "assets", "js", "data.js")
    s = open(src, encoding="utf-8").read()
    i = s.index("{", re.search(r"RL_DATA\s*=\s*", s).end())
    d = 0
    for j in range(i, len(s)):
        if s[j] == "{": d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                end = j + 1
                break
    gc = json.loads(s[i:end])["gc"]
    T, OD = gc["t"], gc["od"]

    W, H, PAD = 620.0, 300.0, 8.0
    tmax, omax = 440.0, 1.75
    X = lambda t: PAD + (t / tmax) * (W - 2 * PAD)
    Y = lambda o: H - PAD - (min(o, omax) / omax) * (H - 2 * PAD)

    # thin it to ~440 points; at this width more is just heavier file, not detail
    step = max(1, len(T) // 440)
    pts = [(X(T[k]), Y(OD[k])) for k in range(0, len(T), step)]
    line = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f"L{pts[-1][0]:.1f} {H - PAD:.1f}L{pts[0][0]:.1f} {H - PAD:.1f}Z"

    write("growthcurve.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<rect x="{X(240):.1f}" y="{PAD}" width="{X(300) - X(240):.1f}" height="{H - 2 * PAD}" fill="{AMBER}" opacity=".13"/>
<path d="{area}" fill="{LEAF5}" opacity=".22"/>
<path d="{line}" fill="none" stroke="{LEAF9}" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>
<line x1="{PAD}" y1="{H - PAD:.1f}" x2="{W - PAD:.1f}" y2="{H - PAD:.1f}" stroke="{LEAF9}" stroke-width="2.4" opacity=".55"/>
</svg>''')


# ── 2. the Pep-family alignment ──────────────────────────────────────────────
# The nine rows of the AtPep panel from our own alignment artifact, drawn with
# that artifact's residue palette so the two read as the same piece of work.
# BoPep4 is the query row and keeps its highlight; the conserved C-terminal
# SSG..G..N core is what the block is for.
PEPS = [
    ("BoPep4", "GILIGSKKRPREPHSSGKPGGHN"),
    ("AtPep1", "ATKVKAKQRGKEKVSSGRPGQHN"),
    ("AtPep2", "DNKAKSKKRDKEKPSSGRPGQTNSVPNAAIQVYKED"),
    ("AtPep3", "EIKARGKNKTKPTPSSGKGGKHN"),
    ("AtPep4", "GLPGKKNVLKKSRESSGKPGGTNKKPF"),
    ("AtPep5", "SLNVMRKGIRKQPVSSGKRGGVNDYDM"),
    ("AtPep6", "ITAVLRRRPRPPPYSSGRPGQNN"),
    ("AtPep7", "VSGNVAARKGKQQTSSGKGGGTN"),
    ("AtPep8", "GGVIVKSKKAARELPSSGKPGRRN"),
]
AA_FILL = {"pos": "#aed6f1", "neg": "#f1948a", "polar": "#a9dfbf",
           "hydro": "#f5cba7", "arom": "#fad7a0"}
AA_INK = {"pos": "#1a5276", "neg": "#7b241c", "polar": "#1a5e3a",
          "hydro": "#7d4f00", "arom": "#784212"}


def aa_class(a):
    if a in "KRHE": return "pos"
    if a in "DE":   return "neg"
    if a in "NQST": return "polar"
    if a in "FYW":  return "arom"
    return "hydro"


def msa():
    C, R = 15.0, 19.0                    # cell, row
    n = max(len(s) for _, s in PEPS)
    W, H = n * C, len(PEPS) * R + 2
    cells, letters = [], []
    for r, (name, seq) in enumerate(PEPS):
        y = r * R + 1
        if name == "BoPep4":
            cells.append(f'<rect x="0" y="{y - 1:.0f}" width="{W:.0f}" height="{R:.0f}" fill="#f0fdf4"/>')
        for c, a in enumerate(seq):
            last = c == len(seq) - 1
            k = aa_class(a)
            fill = "#e74c3c" if last else AA_FILL[k]
            ink = "#ffffff" if last else AA_INK[k]
            cells.append(f'<rect x="{c * C:.0f}" y="{y:.0f}" width="{C - 1:.0f}" height="{R - 2:.0f}" rx="2" fill="{fill}"/>')
            letters.append(f'<text x="{c * C + C / 2 - .5:.1f}" y="{y + R - 6:.1f}" fill="{ink}">{a}</text>')
    write("msa.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<g>{''.join(cells)}</g>
<g font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11" font-weight="600" text-anchor="middle">{''.join(letters)}</g>
</svg>''')


# ── 3. the three regulators ──────────────────────────────────────────────────
# Three jurisdictions as three roundels, in the order this project has to clear
# them. Taiwan is not drawn by hand — it is OUR OWN map layer, alpha-extracted
# and filled flat, so the island on this tile and the island in the map section
# below are the same coastline. The US and the EU get their standard marks.
# Flags were tried and read as "countries"; roundels read as "jurisdictions",
# which is the actual subject.
import base64, math, subprocess, tempfile

MAPDIR = os.path.join(HERE, "assets", "img", "map")


def taiwan_png(px=260):
    """Flat leaf-900 silhouette of our own coastline, as a data: URI."""
    out = os.path.join(tempfile.mkdtemp(), "tw.png")
    subprocess.run([
        # base.webp, not edge.webp: edge is county boundary lines and traces to
        # dust. base is the filled island, so its alpha IS the coastline.
        "magick", os.path.join(MAPDIR, "base.webp"),
        "-bordercolor", "white", "-border", "1",
        "-fuzz", "8%", "-fill", "none", "-draw", "alpha 0,0 floodfill",
        "-alpha", "extract", "-threshold", "20%",
        "-morphology", "Close", "Disk:3",
        "-negate", "-transparent", "white",
        "-fill", LEAF9, "-colorize", "100",
        "-trim", "+repage", "-resize", "x%d" % px, out,
    ], check=True, capture_output=True)
    return "data:image/png;base64," + base64.b64encode(open(out, "rb").read()).decode()


def star(cx, cy, r):
    p = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * .42
        a = -math.pi / 2 + i * math.pi / 5
        p.append(f"{cx + rad * math.cos(a):.1f} {cy + rad * math.sin(a):.1f}")
    return "M" + "L".join(p) + "Z"


def regulation():
    R, GAP = 84.0, 26.0                      # roundel radius, gap between
    W, H = R * 6 + GAP * 2, R * 2
    cy = R
    cx = [R, R * 3 + GAP, R * 5 + GAP * 2]

    tw = taiwan_png()
    ring = "".join(f'<path d="{star(cx[2] + 42 * math.cos(a), cy + 42 * math.sin(a), 8.5)}"/>'
                   for a in (i * math.pi / 6 for i in range(12)))

    # the US mark: six stripes and a canton, which is the flag reduced to the
    # two things that make it legible at 30px
    stripes = "".join(
        f'<rect x="{cx[1] - 52:.0f}" y="{cy - 45 + i * 15.4:.1f}" width="104" height="7.6" rx="3.4"/>'
        for i in range(6))

    write("regulation.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<g fill="none" stroke="{GRAY4}" stroke-width="2.4" opacity=".55">
  <circle cx="{cx[0]:.0f}" cy="{cy:.0f}" r="{R - 2:.0f}"/>
  <circle cx="{cx[1]:.0f}" cy="{cy:.0f}" r="{R - 2:.0f}"/>
  <circle cx="{cx[2]:.0f}" cy="{cy:.0f}" r="{R - 2:.0f}"/>
</g>
<image x="{cx[0] - 46:.0f}" y="{cy - 62:.0f}" width="92" height="124" preserveAspectRatio="xMidYMid meet" xlink:href="{tw}"/>
<g fill="{SLATE}">{stripes}<rect x="{cx[1] - 52:.0f}" y="{cy - 45:.0f}" width="46" height="38" rx="4"/></g>
<g fill="#ffffff"><path d="{star(cx[1] - 29, cy - 26, 11)}"/></g>
<g fill="{AMBER}">{ring}</g>
</svg>''')



# ── 4. the stress index, as the meter it is ──────────────────────────────────
# Our stress model turns temperature and humidity into one number. The number is
# vapour pressure deficit, and it is DETERMINISTIC — the Magnus saturation
# vapour-pressure formulation, not a prediction and not a trained model. The
# needle is computed here rather than drawn by eye, from a real Taiwan summer
# afternoon (33 °C, 70 % RH), so anyone can check it: es = 0.61094·exp(17.625T/
# (T+243.04)); VPD = es·(1 − RH/100) = 1.51 kPa.
def stressmeter():
    T, RH = 33.0, 70.0
    es = 0.61094 * math.exp(17.625 * T / (T + 243.04))
    vpd = es * (1 - RH / 100.0)
    VMAX = 4.0

    W, H, R = 420.0, 250.0, 168.0
    cx, cy = W / 2, H - 34
    A0, A1 = math.radians(198), math.radians(-18)      # sweep, left to right

    def pt(frac, r):
        a = A0 + (A1 - A0) * frac
        return cx + r * math.cos(a), cy - r * math.sin(a)

    def arc(f0, f1, r, w, col):
        x0, y0 = pt(f0, r); x1, y1 = pt(f1, r)
        return (f'<path d="M{x0:.1f} {y0:.1f}A{r:.0f} {r:.0f} 0 0 1 {x1:.1f} {y1:.1f}" '
                f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="butt"/>')

    band = (arc(0, .40, R, 26, LEAF5) + arc(.40, .72, R, 26, AMBER)
            + arc(.72, 1, R, 26, RUST))
    ticks = ""
    for i in range(9):
        f = i / 8
        x0, y0 = pt(f, R - 17); x1, y1 = pt(f, R - (28 if i % 2 == 0 else 23))
        ticks += (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                  f'stroke="{LEAF9}" stroke-width="{3 if i % 2 == 0 else 2}" opacity=".5"/>')
    nx, ny = pt(vpd / VMAX, R - 40)
    write("stressmeter.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
{band}{ticks}
<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{LEAF9}" stroke-width="9" stroke-linecap="round"/>
<circle cx="{cx:.1f}" cy="{cy:.1f}" r="15" fill="{LEAF9}"/>
<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="#ffffff"/>
</svg>''')


# ── 5. the two probes ────────────────────────────────────────────────────────
# THESE ARE DRAWINGS AND THEY ARE DRAWINGS ON PURPOSE. The archive has one
# photograph of the 5 August bring-up, three students at a table, and nothing in
# it identifies which probe is the pH electrode and which is the dissolved
# oxygen one. Cropping a probe out of that frame and captioning it would be a
# guess printed on a public page. So each is drawn to the thing that actually
# tells them apart — pH ends in a glass bulb, DO ends in a flat membrane cap.
# Swap in vendor photographs the moment there are any.
def probe(name, tip, tint):
    # Tilted 30 degrees on purpose. Upright, a probe is a 1:7 sliver: at tile
    # height it renders eighteen pixels wide and reads as a scratch. On the
    # slant the same object fills its box and still reads as an instrument.
    W, H = 260.0, 400.0
    cx = 60.0
    write(name, f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<g transform="rotate(30 60 200) translate(66 6)">
<path d="M{cx:.0f} 6 C{cx - 26:.0f} 22 {cx + 24:.0f} 40 {cx:.0f} 56" fill="none" stroke="{LEAF9}" stroke-width="7" stroke-linecap="round"/>
<rect x="{cx - 21:.0f}" y="52" width="42" height="30" rx="7" fill="{LEAF9}"/>
<rect x="{cx - 17:.0f}" y="80" width="34" height="216" rx="8" fill="{SLATE}"/>
<rect x="{cx - 17:.0f}" y="112" width="34" height="9" fill="#ffffff" opacity=".35"/>
<rect x="{cx - 17:.0f}" y="128" width="34" height="9" fill="#ffffff" opacity=".35"/>
{tip}
</g>
</svg>''')


def probes():
    # pH: a glass measuring bulb, the shape that says "electrode"
    probe("phprobe.svg",
          f'<path d="M43 292h34v34a17 17 0 0 1-34 0z" fill="{SLATE}"/>'
          f'<circle cx="60" cy="336" r="25" fill="#aed6f1" stroke="{SLATE}" stroke-width="4"/>',
          None)
    # DO: a flat membrane cap over the cathode, the shape that says "galvanic"
    probe("doprobe.svg",
          f'<rect x="39" y="292" width="42" height="52" rx="6" fill="{SLATE}"/>'
          f'<rect x="35" y="336" width="50" height="26" rx="8" fill="{AMBER}"/>'
          f'<line x1="41" y1="349" x2="79" y2="349" stroke="#ffffff" stroke-width="4" opacity=".55"/>',
          None)


# ── 6. the signal peptide, doing its one job ─────────────────────────────────
# Our construct is SamyQ (31 aa) in front of BoPep4 (23 aa); signal peptidase I
# cuts between them and the mature peptide leaves the cell. The SignalP
# probability plot is the RESULT of asking where that cut lands, but at 120px a
# plot of three crossing curves says nothing, and the mechanism does.
def signalpeptide():
    """A chain with its front end cut off, which is the whole job.

    A membrane-and-translocon drawing was tried twice and read as a key at tile
    size. This is the construct itself: the SamyQ signal peptide in slate, the
    signal-peptidase I cut in rust, and mature BoPep4 in leaf, lifting away.
    Bead counts are proportional, not literal — 31 aa and 23 aa would be 54
    circles and a smear.
    """
    W, H = 330.0, 310.0
    r, step = 15.0, 30.0
    y0, x0 = 268.0, 24.0
    beads, n_sig, n_mat = [], 6, 8
    for i in range(n_sig):
        beads.append((x0 + i * step, y0, SLATE))
    cut_x = x0 + (n_sig - .5) * step + 14
    # The mature chain turns and goes UP rather than continuing along. Laid out
    # in a line the whole figure is 3:1 and renders thirty pixels tall in its
    # row; turned, it is nearly square and fills the tile.
    for i in range(n_mat):
        a = math.radians(-4 + i * 15)
        beads.append((cut_x + 30 + i * step * math.cos(a) * .42,
                      y0 - i * step * .96, LEAF7))
    path_sig = " ".join(f"{x:.0f},{y:.0f}" for x, y, c in beads[:n_sig])
    path_mat = " ".join(f"{x:.0f},{y:.0f}" for x, y, c in beads[n_sig:])
    circles = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}"/>'
                      for x, y, c in beads)
    write("signalpeptide.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">
<polyline points="{path_sig}" fill="none" stroke="{SLATE}" stroke-width="9" stroke-linecap="round"/>
<polyline points="{path_mat}" fill="none" stroke="{LEAF7}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
{circles}
<g stroke="{RUST}" stroke-width="9" stroke-linecap="round">
  <line x1="{cut_x - 6:.0f}" y1="{y0 - 32:.0f}" x2="{cut_x + 22:.0f}" y2="{y0 + 28:.0f}"/>
  <line x1="{cut_x + 22:.0f}" y1="{y0 - 32:.0f}" x2="{cut_x - 6:.0f}" y2="{y0 + 28:.0f}"/>
</g>
</svg>''')


if __name__ == "__main__":
    growth(); msa(); regulation(); stressmeter(); probes(); signalpeptide()
