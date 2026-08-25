# The big picture &middot; V2

The closing section of the ReLeaf homepage, read one level of abstraction above V1, and built to
stand alone while it is being worked on.

**Live page:** https://timmy97-tw.github.io/releaf-big-picture-v2/

V1 lives at [releaf-big-picture](https://github.com/Timmy97-TW/releaf-big-picture) and is settled.
It is not edited to accommodate this one. The two are different readings of the same material and
only one of them ships.

Drawn on the wiki's own design tokens, copied unmodified from
[`releaf-wiki`](https://github.com/Timmy97-TW/releaf-wiki) at `assets/css/tokens.css`, with the same
self-hosted Inter. Nothing in this repo forks the palette.

## What it argues

**V1 drew eight concrete steps on two horizontal lines.** V2 tells the same material as a story a
judge can follow with one finger, down a single trunk, with the work converging on it horizontally:

| | |
|---|---|
| **The stress** | Heat and salt. The smallest farms sit where they are worst. |
| **The protein** | One of three, chosen against that stress. Not yet made. |
| **The cells** | *B. subtilis*, engineered to make it and let it out. No output measured. |
| **The reactor** | Ours, built from nothing. It has never stood at a farm. |
| **The field** | The dose arrives where the crop is. No plant has had one. |

Two rules produced those five, and they are worth keeping:

1. **Every step is a thing you can point at**, not a stage of a process. An earlier pass used verbs
   (*see it coming, pick what to make, make it, hand it over, do it again*) and it was clever in a
   way that cost clarity: a judge had to build the object back out of the verb before they could
   place a piece of work against it. Nouns let sixteen pieces of work find their step in one look.
2. **Each step carries its claim and its limit in one breath**, at the same size, and then stops.
   Two short sentences, never three. If a step needs a paragraph, the step is wrong.

**There are no step numbers.** The ramp on the left edge of each card walks light to dark down the
five, and the chevrons between them point one way; that is enough. A numbered list says "process
diagram" when this is meant to say "here is the thing".

Under the five sit **one week on one plot**, which is the mechanism at a single farm, and then
**the map**, which is where the argument stops being about a machine and starts being about ground.
Zoom in, then all the way out.

## Reading it

- **Nothing opens.** No panel, no modal, no drawer, no page change. Every label is on screen before
  you touch anything.
- **Point at a step** and the work that feeds it lights up, along with the moments in the week at
  the end that come out of it.
- **Point at a piece of work** and it lights the step it feeds, every step after that one, and the
  segments between them. Its photograph comes up to full colour and a line draws into the step it
  serves. That is the answer to the only question worth asking of a figure like this: how does my
  work reach a farm.
- **Point at anything and its cross-links are marked in amber.** That is the quiet half. The model
  marks the baselines, the light array and the tandem run. The business plan marks the map,
  regulation and the farmers. The run down the trunk stays the loud thing, and the web of
  who-talks-to-whom sits underneath it rather than being drawn as permanent lines that would turn
  the trunk into a hairball. Cross-links live in `data-with` on each tile.
- **Point at a moment in the week** and the step it came out of lights, up the page.

Keyboard reaches all of it: twenty-seven focusable elements plus the dial, and focus runs the same
code path as hover.

## A piece of work is its own photograph

There is no card beside the picture. **The tile is the picture**, with the name under it, and that
is the whole thing: no pill, no icon, no subtitle. Sixteen of them, fifteen photographs from
`iGEM2026_Images` (filenames are `YYYYMMDD_Subteam_Type_Description`, and the date is the day the
photograph was taken) plus the one tile that moves.

An earlier pass put a photograph in the margin *next to* a labelled pill, and it read as two things
about one subject. Collapsing them was the change that made the figure quiet. Four decisions hold it
there:

1. **They run horizontally, not down.** A step and everything that feeds it occupy one line of the
   page, which is what lets all five fit on a laptop screen with nothing scrolled.
2. **One line per label, always**, terse and with the definite articles dropped. Under a photograph
   "Photometer" reads faster than "The photometer", and a fixed one-line label means every row of
   the chain is exactly as tall as every other. Ragged rows were what read as mess.
3. **They sit held back until wanted.** Desaturated and slightly down in opacity, so they read as a
   contact sheet feeding the trunk rather than sixteen pictures competing with it.
4. **No captions.** The name under the tile is the caption. The detail, including the date, lives in
   `alt`, where a screen reader gets it and the drawing does not have to carry it.

**The dark half has no photographs at all.** The five steps are the record and the pictures are
evidence for them. The week is a projection: none of it has happened, so there is nothing to
photograph, and putting real pictures beside a hypothetical week would be the one dishonest thing on
the page. The only image down there is the map, which is a measurement.

## The trajectory

The tile marked **Docking** is not a photograph. It is 46 frames of our own MD run,
`R1_BoPep4_WT_PEPR1`: 30 ns of production, BoPep4 in the PEPR1 groove, drawn straight out of
`21_MD_Simulation/results/R1_BoPep4_WT_PEPR1_out/stripped.dcd`.

- Every frame is superposed on the receptor Cα, so what moves is the peptide and not the view.
- The pale band behind the chain is the envelope the backbone stays inside across the window, which
  is the picture of the acceptance criterion: receptor Cα RMSD 1.59 Å, peptide backbone RMSD 2.77 Å.
- **Green is Asn23, amber is Arg487.** They stay together for the whole loop because in the run they
  were within 4 Å in 100 % of frames. That is the result, drawn rather than asserted.
- The 46 frames are the window whose last frame is closest to its first, so the loop closes without
  a jump. Closure is 0.68 Å in the projection.

It is **still until it is pointed at**. The frames live in `data-frames` on the SVG and are stepped
by the script, so with scripting off it is one frame and nothing on this page moves on its own.
Under `prefers-reduced-motion` it never steps. Regenerating it is two scripts kept
beside the page: `tools_md_extract.py` reads the parm7 and the DCD with no MD libraries installed
and writes the Cα coordinates, and `tools_md_svg.py` superposes, projects, picks the loop window and
emits the SVG. Neither runs at page load; the reader only ever gets the finished drawing.

## The week at the end

One call, one plot, one week, on ink. The mechanism is concrete and every number carries where it
came from in the same sentence, at the same size:

- **roughly 105 minutes** to half maximum, **borrowed, not ours**: a different organism at a
  different wavelength, and it is not on record which output it describes.
- **1 mU/mL** of ACC deaminase in neat cell-free permeate, the gate we set ourselves, which is at
  once the ACC-cleaving capacity of a 10⁸ CFU/mL colonisation by *P. putida* UW4 and a 39 hour
  clearance half-life in the reservoir. From `28_ACCD_Permeate_Threshold`.
- **2.4 mU/mL** at the reactor, for a 5 L reservoir and 60 mL/h of permeate.
- **K_M 3.4 mM** (Hontzeas 2004), three orders above anything a root zone holds, which is why
  clearance runs first order and why we never had to guess a concentration nobody has measured. The
  same paper is the reason the pH risk is stated next to it.
- **Nothing at the plant.** No plant has received anything from this system.

Then the sentence a judge will otherwise say first: **the forecast has to warn us earlier than the
system takes to answer, and we have measured neither number.** If the warning is shorter than the
answer, the protein arrives after the stress.

Then it widens back out to the country, on the scale-out model from the
[invariant explorer](https://timmy97-tw.github.io/releaf-invariant-explorer/): adding modules holds
wall shear, Reynolds number, flux and fouling margin, and power is the one thing that does not
scale. Model output, none of it measured.

## The reach, and the dial

The page ends on **our own QGIS map**: farm parcels under two hectares in red, parcels over two in
blue, over a five step choropleth of the climate volatility index, which is computed from mean
diurnal temperature range, seasonal temperature range and the coefficient of variation of
precipitation. The finding is in the overlay rather than in either layer: **the small parcels and
the top band of the index are the same ground.** The farms least able to buy their way out of a bad
season are sitting on the worst of it.

Beside it is a dial, and the dial is the honest part. It moves a **share** of those small farms, and
a hundred squares fill to match. A share is true by construction: no count is implied and none is
needed, because the grid is the percentage, drawn. What the dial refuses to do is turn that share
into a number of machines or a quantity of protein, and it says why, in two boxes underneath:

- **How many machines.** Our own parcel layer can be counted. It has not been counted.
- **How much protein.** No titre has been measured, and there is no bill of materials total.

That is the shape every impact claim on this project should take: show the ground, move the share,
and name the two measurements standing between a share and a number. Do not close the gap with a
guess. The one number that is allowed to be large is sourced rather than ours: 84% of the world's
570 million farms are under two hectares (FAO), which is the same cut the red on the map is drawn at.

## Slots, and why they are drawn rather than left out

Seven numbers this page needs are not on record. **A slot is a designed element, not an omission.**
Each one says what is missing and what would fill it, in the same type as everything else:

forecast lead time · the dose policy · the permeate rate Q_p · end-to-end latency · how many small
farms sit in that band · what one machine costs to build · what one machine puts out.

Do not fill a slot with a guess, and do not delete one to tidy the page up. Never invent a number, a
quote, a date or a result: it is the project's main credibility asset, and this page is where a
judge will check it.

The site itself is a slot on purpose. The QGIS layers exist; the township reading is not written up,
so the page does not name a place.

## Two colour systems, and they do not overlap

**The ramp** says direction. The five accent bars walk light to dark down the trunk. With the step
numbers gone it is the only cue in the figure that says which way to read it.

**Amber** marks a cross-link, and never means anything else.

**The icons** are coloured by what the object actually is. So is the trajectory: its chain, its
envelope and its two marked residues all come through the same icon palette, so the one moving thing
on the page is in the same voice as the glyphs.

V1 had a third system, a zone colour saying which subteam owned a card, read off a key at the top of
the figure. **The key was cut and the colour went with it** rather than sitting on the page
unexplained. An unlabelled code is worse than no code, and the figure got quieter for losing it.

## The icons

Every glyph is drawn from our own hardware or from the system schematic, not from a library. That is
the point of them: a generic flask says "science", and the culture carboy with its ribbed cap, its
pink medium, its rod cells and its stir bar says *this bottle*.

The 26-symbol sprite is **V1's, reused unchanged**, so one drawing serves both pages and a hardware
change is one edit. Five of its glyphs sit on the step cards (the potted plant, the docking pose,
the culture carboy, the reactor, the hydroponic tray) and the rest are held for the wiki. Two glyphs
were drawn new for an earlier pass of this page, in the same voice from the same CAD, and are kept
in the sprite:

| Glyph | Drawn from |
|---|---|
| **Do it again** (node 05) | the cartridge with its black end caps and slate body, an amber cassette block seated in the middle of it, and the loop that says the machine comes back |
| **Scale-out** | the same module three times on one manifold, with the same green permeate leaving each, because on the model that is what scaling is: more of the same, not a bigger one |

Sources live in the wiki at `hardware/img/card-*.png` and `assets/img/home/system-schematic-1600.png`.
If a piece of hardware changes, redraw the glyph rather than swapping in a library icon. Every colour
in the sprite goes through `var()`.

The drawing at the very end, the reactor standing at the head of an irrigation line, is V1's, reused.

## Behaviour worth keeping

- **Readable with no JavaScript and no motion.** The hidden state of the entrance is added by
  script, never by the stylesheet, so with scripting off the drawing is simply there, photographs
  and all, with the trajectory on its first frame. There is also a 1400 ms fallback that reveals the
  figure if the observer never fires, because a figure is never allowed to stay invisible.
- **No horizontal scroll, and no drag gesture to explain.** The trunk is vertical, so the drawing is
  never wider than the column. V1 needed a scroll frame and a line of text telling you to drag it;
  this one does not, which is the quiet practical win of turning the figure ninety degrees.
- **Under 900px** the trunk moves to the left edge and each step's work wraps underneath it, step
  first. Same markup, no second copy of the content to keep in sync.
- **The five steps fit one laptop screen.** That is a constraint, not an accident: a judge should
  see the whole chain without scrolling and then choose where to look. If an edit pushes the fifth
  step below the fold, cut writing rather than shrinking type.
- **Two motion primitives only**: one entrance on first sight, one highlight on point. The
  trajectory belongs to the second of those, because it runs only while its card is pointed at. It
  is deliberately not a third, always-on animation. Nothing scales, nothing bounces, and focus rings
  are never transitioned.
- The trajectory is stepped on `requestAnimationFrame`, so a background tab costs nothing. SMIL was
  tried first and dropped: pausing a SMIL timeline before it has ever run wedges it at zero.
- `prefers-reduced-motion` turns every transition off, including the entrance.

## Merging into the homepage

1. Copy `assets/css/big-picture-v2.css`, `assets/js/big-picture-v2.js` and the sixteen files in
   `assets/img/` into the wiki's `assets/`. The image paths in the markup are relative
   (`assets/img/*.jpg`), so they need no edit if the wiki keeps the same layout.
2. Paste **both** `<section>` elements into `index.html`: the white `section.bpv2` and the ink
   `section.band--dark.act` that follows it, which carries the week, the map and the claim. Include the `<svg class="sprite">` block at the top of
   the first one. The sprite has to travel with the section: a `<use href="external.svg#id">` does
   not resolve reliably, so the symbols are inlined.
3. Add the stylesheet link and the script tag.
4. Delete the `<div class="shell">` element and the inline `<style>` block in the head. Both exist
   only so the standalone page has a body to sit in. `home.css` already supplies `.band`,
   `.band__inner`, `.band--dark` and `h2.band__title`.
5. Delete the three lines in the stylesheet that declare `--ink`, `--ink-2` and `--sig-green`.
   `home.css` already defines all three for the dark act.

It reads as the last band, after **Explore our project**, which is `band--tint`, so the white half
stays on white and the ink half closes the page.

## A conflict worth knowing about

`tokens.css` sets `--font-display` and `--font-body` to the same face. The rule is to preserve a
project's font stack rather than fork it, so this section does. The comment at the top of
`tokens.css` already notes that the homepage brief argues against Inter and that swapping the site
over is an edit to two variables. If that swap happens, this section follows it with no changes.

## Editing the content

Everything readable is in `index.html`. The script holds no content of its own.

- **A step** is a `.node` with `data-node="1"` to `"5"`, containing a `.strip--l`, a `.node__core`
  and a `.strip--r`. Two short sentences in `.node__note`, claim then limit. Never three.
- **A piece of work** is a `.task` with an `id`, `data-at="<step number>"`, an optional
  `data-with="<space separated ids>"`, a `<figure class="task__shot">` holding one image, and a
  `.task__name`. Adding one is a single element and no JavaScript. Keep the name to one line;
  it is clipped rather than wrapped on purpose, so a long one will tell you.
- Swapping a photograph is one `src` and one `alt`. The `alt` names what is in the frame and the
  date, and nothing more.
- **A segment** is a `.link` with `data-seg`, matching the node it leaves.
- **A moment** in the week is a `.moment` with `data-node`, naming the step it came out of.
- **A slot** is a `.slot` with a `<b>` label and one sentence saying what would fill it.

Related pages: the [judging session board](https://timmy97-tw.github.io/judging-session-prep/), the
[iGEM bioreactor landscape](https://timmy97-tw.github.io/igem-bioreactor-landscape/), the
[invariant explorer](https://timmy97-tw.github.io/releaf-invariant-explorer/), and
[V1 of this section](https://timmy97-tw.github.io/releaf-big-picture/).
