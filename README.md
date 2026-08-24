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

**V1 drew eight concrete steps on two horizontal lines.** A stressed field, a molecule, cells, a
plant, and underneath them the call, the light, the reactor, the membrane. Objects, mostly.

**V2 draws five verbs on one vertical trunk**, because the argument is not really about the kit. It
is about what the machine does, and about who is allowed to do it.

| | | |
|---|---|---|
| 01 | **See it coming** | a stress called before the plant shows it |
| 02 | **Pick what to make** | which molecule, and how much of it |
| 03 | **Make it** | a culture that runs where the crop is |
| 04 | **Hand it over** | protein out, cells in |
| 05 | **Do it again** | for something else, somewhere else |

Three of these are deliberate departures from the obvious chain.

- **Not *locate*.** Locating is what the map does, once, offline. It is not something the machine
  does. What the machine does every day is call a stress early, and that is the claim the whole
  prediction argument rests on, including its unclosed half. The map earns a better job below the
  trunk instead.
- **Not *deliver*.** Deliver overstates what we can defend. Delivery stops at a reservoir.
  *Hand it over* is the membrane act itself, and it lets the limit sit inside the node rather than
  beside it.
- **Not *scale*.** Half of that node is not scale, it is retasking, and retasking is the answer to
  the one competitor this whole device has: a dried spore sachet. *Do it again* carries both halves.
  A sachet answers only *whether*, once, forever. This answers *how much*, again, and for something
  else.

Fifteen pieces of work enter the trunk from both sides, icon and name only. The node carries the
sentence; a card that carries its own subtitle competes with the node it is meant to feed, which is
what V1 learned the hard way with fifteen subtitled cards in a horizontal band.

Below the trunk sits **the map**, keeping V1's best structural move: one tandem run says the line
works once, and the map says how much land is under the stress, where, and in which month. Past it,
on ink, sits **the week**, which is the payoff.

## Reading it

- **Nothing opens.** No panel, no modal, no drawer, no page change. Every label is on screen before
  you touch anything.
- **Point at a node** and the work that feeds it lights up, along with the moments in the week at
  the end that come out of it.
- **Point at a piece of work** and it lights the node it feeds, every node after that one, the
  segments between them, and the map. That is the answer to the only question worth asking of a
  figure like this: how does my work reach a farm.
- **Point at anything and its cross-links are marked in amber.** That is the quiet half. The model
  marks stress baselines, the light array and the tandem run. The business plan marks the map,
  regulation and the farmers. The run down the trunk stays the loud thing, and the web of
  who-talks-to-whom sits underneath it rather than being drawn as permanent lines that would turn
  the trunk into a hairball. Cross-links live in `data-with` on each card.
- **Point at a zone in the key** and every card that belongs to it lights. The key is the one thing
  V1 did not need, because V1 had labelled zone bands behind its lanes and a vertical trunk has no
  lanes to label. It is a key that does something, which is the only kind worth having.
- **Point at a moment in the week** and the verb it came out of lights, up the page.
- **Point at anything and the photographs follow it.** A card's picture comes up to full colour with
  it, a marked cross-link's comes part way, and the rest of the contact sheet steps back.

Keyboard reaches all of it: thirty focusable elements, and focus runs the same code path as hover.

## The margins

Every card carries a photograph of the work, outboard of it in the margin, from
`iGEM2026_Images` (filenames are `YYYYMMDD_Subteam_Type_Description`, and the date is the day the
photograph was taken). Fifteen of them, plus the trajectory below.

Four decisions keep this from turning into clutter, and they are the point of the arrangement:

1. **Two fixed columns per wing.** Every picture in a margin shares one edge and every card sits
   flush against the trunk. An earlier pass let each pair size itself, and the ragged inner edge was
   the thing that read as mess.
2. **They sit quiet until they are wanted.** Held back in saturation and opacity, they read as a
   contact sheet running down the sides rather than as fifteen pictures competing with the figure.
   The card being pointed at brings its own up to full.
3. **No captions.** A caption under each one is exactly the mess this is trying to avoid, and the
   card beside it already names the work. The detail, including the date, lives in `alt`, where a
   screen reader gets it and the drawing does not have to carry it.
4. **The dark act has no photographs at all.** The light half is the record and the pictures are
   evidence for it. The week at the end is a projection: none of it has happened, so there is
   nothing to photograph, and putting real pictures beside a hypothetical week would be the one
   dishonest thing on the page.

## The trajectory

The margin of **Design and docking** is not a photograph. It is 46 frames of our own MD run,
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

## Slots, and why they are drawn rather than left out

Seven numbers this page needs are not on record. **A slot is a designed element, not an omission.**
Each one says what is missing and what would fill it, in the same type as everything else:

the township reading · forecast lead time · the dose policy · the permeate rate Q_p · end-to-end
latency · how many irrigation lines are like this one · what one machine costs to build.

Do not fill a slot with a guess, and do not delete one to tidy the page up. Never invent a number, a
quote, a date or a result: it is the project's main credibility asset, and this page is where a
judge will check it.

The site itself is a slot on purpose. The QGIS layers exist; the township reading is not written up,
so the page does not name a place.

## Three colour systems, and they do not overlap

**The zone** says whose work a card is. Green is biology, slate is engineering, amber is deployment.
It colours the well behind the icon, the connector that ties a card to the trunk, and the swatch in
the key, so a card's home is legible before a word on it is read.

**The ramp** says direction. The five node badges walk light to dark down the trunk, and so does the
accent bar on each card. It is the only cue in the figure that says which way to read it.

**The icons** are coloured by what the object actually is. So is the trajectory: its chain, its
envelope and its two marked residues all come through the same icon palette, so the one moving thing
on the page is in the same voice as the glyphs.

Amber has one more job, and only one: **marking a cross-link**. It never means anything else.

## The icons

Every glyph is drawn from our own hardware or from the system schematic, not from a library. That is
the point of them: a generic flask says "science", and the culture carboy with its ribbed cap, its
pink medium, its rod cells and its stir bar says *this bottle*.

The 26-symbol sprite is **V1's, reused unchanged**, so one drawing serves both pages and a hardware
change is one edit. Two glyphs are new here, drawn in the same voice from the same CAD:

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
- **Under 900px** the trunk moves to the left edge and each node's work stacks underneath it, node
  first. Same markup, no second copy of the content to keep in sync.
- **Two motion primitives only**: one entrance on first sight, one highlight on point. The
  trajectory belongs to the second of those, because it runs only while its card is pointed at. It
  is deliberately not a third, always-on animation. Nothing scales, nothing bounces, and focus rings
  are never transitioned.
- The trajectory is stepped on `requestAnimationFrame`, so a background tab costs nothing. SMIL was
  tried first and dropped: pausing a SMIL timeline before it has ever run wedges it at zero.
- `prefers-reduced-motion` turns every transition off, including the entrance.

## Merging into the homepage

1. Copy `assets/css/big-picture-v2.css`, `assets/js/big-picture-v2.js` and the fifteen files in
   `assets/img/` into the wiki's `assets/`. The image paths in the markup are relative
   (`assets/img/*.jpg`), so they need no edit if the wiki keeps the same layout.
2. Paste **both** `<section>` elements into `index.html`: the white `section.bpv2` and the ink
   `section.band--dark.act` that follows it. Include the `<svg class="sprite">` block at the top of
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

- **A node** is a `.node` with `data-node="1"` to `"5"`, containing a `.wing--l`, a `.node__core`
  and a `.wing--r`.
- **A card** is a `.chip` with an `id`, `data-feeds="bio|eng|dep"`, `data-at="<node number>"`, an
  optional `data-with="<space separated ids>"`, and an `<svg class="ico">` pointing at a symbol in
  the sprite. Adding a piece of work is one element and no JavaScript.
- **A card and its photograph** are a `.feed` with `data-zone` matching the card's `data-feeds`,
  holding a `<figure class="shot">` and then the `.chip`, in that order. The right wing puts the
  figure back on the outside itself, so the markup order never changes. Swapping a photograph is one
  `src` and one `alt`; the `alt` should name what is in the frame and the date, and nothing more.
- **A segment** is a `.link` with `data-seg`, matching the node it leaves.
- **A moment** in the week is a `.moment` with `data-node`, naming the verb it came out of.
- **A slot** is a `.slot` with a `<b>` label and one sentence saying what would fill it.

Related pages: the [judging session board](https://timmy97-tw.github.io/judging-session-prep/), the
[iGEM bioreactor landscape](https://timmy97-tw.github.io/igem-bioreactor-landscape/), the
[invariant explorer](https://timmy97-tw.github.io/releaf-invariant-explorer/), and
[V1 of this section](https://timmy97-tw.github.io/releaf-big-picture/).
