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

Under the five sits **the map**, which is where the argument stops being about a machine and starts
being about ground. An earlier build put a hypothetical week on a hypothetical plot between them.
It was cut: it was the only part of the page describing something that had not happened, and it made
the reader wade through a projection to reach the evidence.

## Reading it

- **Nothing opens.** No panel, no modal, no drawer, no page change. Every label is on screen before
  you touch anything.
- **Point at a step** and the work that feeds it lights up.
- **Point at a piece of work** and it lights the step it feeds, every step after that one, and the
  segments between them. Its photograph comes up to full colour and a line draws into the step it
  serves. That is the answer to the only question worth asking of a figure like this: how does my
  work reach a farm.
- **Point at a row of the map legend** and the map holds that layer on its own, with the small
  parcels left in place.
- **Point at anything and its cross-links are marked in amber.** That is the quiet half. The model
  marks the baselines, the light array and the tandem run. The business plan marks the map,
  regulation and the farmers. The run down the trunk stays the loud thing, and the web of
  who-talks-to-whom sits underneath it rather than being drawn as permanent lines that would turn
  the trunk into a hairball. Cross-links live in `data-with` on each tile.
Keyboard reaches all of it: twenty-eight focusable elements plus the dial, and focus runs the same
code path as pointing.

**One listener, on the container.** An earlier build wired `pointerenter` and `pointerleave` to
every tile. Crossing from one tile to its neighbour fired leave-then-enter, and the frame in between
had everything un-held, so dragging along a row strobed. Pointing is now handled once, on the
container, with `pointerover`, which bubbles: moving between two tiles is a single event and a single
swap with no blank frame. If you ever see the figure flicker again, this is the thing that broke.

## A piece of work is its own photograph

There is no card beside the picture. **The tile is the picture**, with the name and a mark under it.
Twenty-five of them, twenty-four photographs from
`iGEM2026_Images` (filenames are `YYYYMMDD_Subteam_Type_Description`, and the date is the day the
photograph was taken) plus the one tile that moves.

An earlier pass put a photograph in the margin *next to* a labelled pill, and it read as two things
about one subject. Collapsing them was the change that made the figure quiet. Four decisions hold it
there:

1. **They run horizontally, not down.** A step and everything that feeds it occupy one line of the
   page, which is what lets all five fit on a laptop screen with nothing scrolled.
1b. **Each step sets its own tile format, and the format is the step's signature.** A plot, a person
   kneeling and an island are all upright, so **The stress** runs portrait. A trajectory and a page of
   working are wide, so **The protein** does. Plates and gels are square, benches are landscape, a
   field is a horizon. Uniform tiles read as a spreadsheet; these vary for a reason, the same way the
   ramp does. Change a format in one line: `.node[data-node="3"] { --tile-w; --tile-h }`.
1c. **One photograph leads each step**, marked `data-lead` and set larger. It is the one with people
   in it wherever there is a choice, and it is deliberately not always on the same side, so the eye
   lands somewhere first and the strips do not read as a grid.
1d. **They are prints, not thumbnails.** A white mat, a hairline, a soft drop and about a degree of
   tilt, laid on a common bottom edge. The tilt is a static transform and never changes; it is there
   because a wall of perfectly square crops reads as a database and this is a record of a year of
   somebody's Saturdays. Saturation sits at 0.9 rather than the 0.68 an earlier pass used: faces
   should look like faces.
2. **Two lines per label, fixed**, terse and with the definite articles dropped. Under a photograph
   "Photometer" reads faster than "The photometer". The box is a fixed two lines whether the name
   uses them or not, so every row of the chain is exactly as tall as every other; ragged rows were
   what read as mess. Names are plain on purpose: "Cloning", "Pressure", "Schools", not the internal
   shorthand a subteam would use.
3. **They sit held back until wanted.** Desaturated and slightly down in opacity, so they read as a
   contact sheet feeding the trunk rather than sixteen pictures competing with it.
4. **No captions.** The name under the tile is the caption. The detail, including the date, lives in
   `alt`, where a screen reader gets it and the drawing does not have to carry it.
5. **A mark on the caption line, from our own CAD.** A photograph at this size tells you the mood of
   a day and not much else; the glyph says what the thing is before the name is read. It sits beside
   the name, **never over the picture**. A badge floating on the frame was tried first and it fussed
   up every photograph it landed on: the photo is the evidence and nothing should sit on top of it.

**The closing band carries no photographs.** The five steps are the record and the pictures are
evidence for them. The only image down there is the map, which is a measurement rather than a day.

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

**Every tile is a photograph.** Two of them were briefly student stickers and both were put back:
in a record of what a year of work looked like, a drawing of the thing is not the thing. Illustration
belongs at the end of the page, not in the evidence.

## The map, and the claim it can actually carry

The page ends on our own QGIS work, from `iGEM2026_Images/QGIS Uploads/All Taiwan Farmlands/`.

**An earlier draft of this section said the wrong thing, and the correction is worth keeping on
record.** It claimed the small parcels and the worst volatility bands were the same ground, which is
the tidy story. Measuring the layer said otherwise: small-farm density by band, calmest to worst,
runs 33.6, 30.0, 15.3, 23.6, 8.9 percent. There is no trend, and the calmest band is the densest.

What the layer does support is stronger for this project anyway, so the section now says that
instead:

- **97% of the farmland on this map is under two hectares** (181,026 px against 4,705 px of parcels
  over two hectares).
- **On the ground that swings hardest it is 99.8%.** The little large-farm land there is sits in the
  calm middle band, where it holds 1.4% of the land against 0.01 to 0.14% everywhere else.

So the argument is not that small farms got the worst weather. It is that **there is no other kind
of farmer in Taiwan to build for**, and that this holds hardest exactly where the weather is worst.
`tools_band_assign.py` is what measured it; re-run it before changing any number here.

It is not a screenshot. The QGIS export was quantised to its own legend colours and pulled apart
into nine layers, which the page stacks and drives:

`base` · `v1`–`v5` (the five index classes) · `smalldim` (every parcel, pale) · `sb1`–`sb5` (the same
parcels split by the band they sit on) · `large` · `edge` (county lines). Regenerating them is
`tools_map_layers.sh` and `tools_band_assign.py` beside the page.

Three things about that are worth keeping straight if you touch it:

- **The colours are this page's, the breaks are the analysis's.** QGIS drew navy through yellow with
  red and blue parcels, which fights the leaf palette and reads as a foreign object dropped into the
  page. The five classes were recoloured to a pale-to-rust ramp and the parcels to leaf and slate.
  Recolouring a choropleth is ordinary cartography; moving a class break would not be, and none moved.
  The caption says so on the page.
- **The band layers have parcel-shaped holes in them**, because the parcels were drawn on top of the
  choropleth before the export was flattened. They are never visible, because the band layers are
  only ever drawn as *overlays* above a scrim with the parcel layer above them, which fills the holes
  exactly. Do not try to use a band layer as a base. A morphological close was tried to fill the
  holes and is the wrong answer: a kernel small enough to keep the county boundaries honest does not
  fill them, and a kernel large enough to fill them redraws the regions.
- **The legend is the control.** Pointing at a row scrims the map and holds that layer, with every
  small farm left in at full strength. It carries a swatch and a label and nothing else: the gloss
  column that explained each row was cut, because a legend that needs prose is not a legend. It answers to pointing exactly the way the five steps do, which is the whole
  reason it reads as one page and not as a figure bolted to the end of one.
- **The island sits on the trunk's axis.** It is the same centre line as the five step cards, and the
  rail runs out of the last step, across the band edge, and into the map. The two halves are one
  drawing. If an edit moves the map off centre, the connection is gone and the section reads as an
  appendix again.

## The dial, and why the map fills in that order

Beside the map, a hundred hairlines with the first N inked. The dial moves a **share** of the
small-farm land, and **the map answers by filling in from the hardest ground down**, because that is
the order anybody deploying this would work in. An earlier version washed the whole layer green in
proportion, which looked fine and meant nothing: it connected the slider to a percentage rather than
to the map underneath it.

Every parcel is assigned the volatility band of the ground around it, which is recoverable even
though the export is flat: the parcels were drawn over the choropleth, the choropleth is by
administrative area, and a parcel is tiny next to one, so the band that surrounds a parcel is that
parcel's band. `tools_band_assign.py` grows the band labels into the parcel holes one pixel at a
time until they are full, then counts. The five shares, worst band first, are **0.4, 14.5, 24.0,
50.4 and 10.7 percent** of small-farm area, and those five numbers are what the dial walks through.
They are hard-coded in the script that drives it; if the layer is ever re-rendered, re-run the tool
and update them together.

The readout names the threshold rather than a quantity: *every small farm on ground that swings 0.71
or harder, and part of the band below it*. That is the whole caption. The paragraph that used to sit
under it, spelling out that the parcels have not been counted and no titre has been measured, was cut
for being a lecture; the constraint has not changed and it belongs in this file rather than on the
page. **Do not put a number of machines or a weight of protein next to that dial.**

## The outro

**All of us walking up the row into 陳惠雯's plot, 21 July 2026**: one landscape band the full width of
the viewport, no fade, with one sentence and a signature across the row underneath. She is the farmer
who moved our dosing off a wall clock and onto soil-moisture state, and the frame is a line of
high-schoolers in team shirts following her into her own field. That is the argument the page has
been making, in one picture.

Earlier versions cropped in close on her and feathered the band into the paper. Both were dropped:
the close crop lost the group, and the feather made the picture look uncertain about being there. A
hard-edged full-width band is the stronger ending.

Three things hold it together and are easy to break:

- **The ground stays light.** An ink outro was tried and the sign-off is the hand-drawn wordmark,
  whose letters are filled black; on ink it disappears. Paper also means the band above needs no
  seam, which is what makes the photograph read as part of the page rather than a block dropped on
  the end.
- **The sign-off is a student drawing, not the logo.** The circular team logo was there first and got
  swapped: the wordmark is warmer, it is the same hand as the two sticker tiles above, and it does
  not read as corporate furniture at the end of a page about farmers.

**Consent is not on record.** The project brief lists image consent and release for 陳惠雯 as
outstanding. This page is public. Get her agreement before the wiki goes live, or change the
photograph.

## Slots, and why they are drawn rather than left out

Three numbers this page needs are not on record. **A slot is a designed element, not an omission.**
Each one says what is missing and what would fill it, in the same type as everything else:

how many small farms sit on that coast · what one machine costs to build · what one machine puts
out. The outro photograph is the fourth: a frame that does not exist yet.

Do not fill a slot with a guess, and do not delete one to tidy the page up. Never invent a number, a
quote, a date or a result: it is the project's main credibility asset, and this page is where a
judge will check it.

The site itself is a slot on purpose. The QGIS layers exist; the township reading is not written up,
so the page does not name a place.

## Two colour systems, and they do not overlap

**The ramp** says direction. The five accent bars walk light to dark down the trunk. With the step
numbers gone it is the only cue in the figure that says which way to read it, which is why it is
three pixels of leaf rather than a hairline.

**Amber** marks a cross-link, and never means anything else.

**The icons** are coloured by what the object actually is. So is the trajectory: its chain, its
envelope and its two marked residues all come through the same icon palette, so the one moving thing
on the page is in the same voice as the glyphs.

V1 had a third system, a zone colour saying which subteam owned a card, read off a key at the top of
the figure. **The key was cut and the colour went with it** rather than sitting on the page
unexplained. An unlabelled code is worse than no code, and the figure got quieter for losing it.

The map runs its own palette on top of these, and it is data rather than decoration: five index
classes from pale to rust, leaf for a parcel under two hectares, slate for one over. Those seven
values live as tokens (`--vol-1` to `--vol-5`, `--parcel-small`, `--parcel-large`) because the raster
layers were rendered to exactly them, and a legend swatch that drifts from its layer is a lie.

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
  first, and the map plate stacks above its legend. Same markup, no second copy of the content.
- **Verified at 320, 375, 414, 768, 900, 1280, 1440 and 1920.** No horizontal scroll at any of them,
  and no label overflows its two-line box.
- **The five steps no longer fit one screen**, and that was a deliberate trade: the chain carries
  twenty-five pieces of work rather than sixteen. If it has to fit again, cut tiles, not type.
- **The five steps fit one laptop screen.** That is a constraint, not an accident: a judge should
  see the whole chain without scrolling and then choose where to look. If an edit pushes the fifth
  step below the fold, cut writing rather than shrinking type.
- **Two motion primitives only**: one entrance on first sight, one highlight on point. The
  trajectory and the map both belong to the second, because both run only while something is being
  pointed at. Nothing scales, nothing bounces, and focus rings are never transitioned.
- The trajectory is stepped on `requestAnimationFrame`, so a background tab costs nothing. SMIL was
  tried first and dropped: pausing a SMIL timeline before it has ever run wedges it at zero.
- `prefers-reduced-motion` turns every transition off, including the entrance.

## Merging into the homepage

1. Copy `assets/css/big-picture-v2.css`, `assets/js/big-picture-v2.js`, the images in `assets/img/`
   (sixteen tiles, the outro frame, the logo) and the fourteen map layers in `assets/img/map/` into
   the wiki's `assets/`. The image paths in the markup are relative
   (`assets/img/*.jpg`), so they need no edit if the wiki keeps the same layout.
2. Paste **all three** `<section>` elements into `index.html`, in order: the white `section.bpv2`,
   the tinted `section.reach`, and the full-bleed `section.outro`. The rail runs across the first two
   boundaries, so their order and their zero vertical padding at the join both matter. Include the `<svg class="sprite">` block at the top of
   the first one. The sprite has to travel with the section: a `<use href="external.svg#id">` does
   not resolve reliably, so the symbols are inlined.
3. Add the stylesheet link and the script tag.
4. Delete the `<div class="shell">` element and the inline `<style>` block in the head. Both exist
   only so the standalone page has a body to sit in. `home.css` already supplies `.band`,
   `.band__inner`, `.band--dark` and `h2.band__title`.
5. `section.reach` is white with a hairline above it, so it can follow anything.
6. The three sections raise their own specificity (`section.bpv2`, `section.reach`, `section.outro`)
   because `home.css` sets `.band { padding: var(--sp-8) 0 }` and a bare class would lose to it.
   Keep the element selector or the rail will break at the band edge.

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
- **A legend row** is a `.key__row` with `data-hold` naming a layer id. Adding a layer is one image,
  one row and one line of CSS.
- **A piece of work** is a `.task` with an `id`, `data-at="<step number>"`, an optional
  `data-with="<space separated ids>"`, a `<figure class="task__shot">` holding one image, a
  `.task__mark` pointing at a sprite symbol, and a `.task__name`. Adding one is a single element and no JavaScript. Keep the name to one line;
  it is clipped rather than wrapped on purpose, so a long one will tell you.
- Swapping a photograph is one `src` and one `alt`. The `alt` names what is in the frame and the
  date, and nothing more.
- **A segment** is a `.link` with `data-seg`, matching the node it leaves.

- **A slot** is a `.slot` with a `<b>` label and one sentence saying what would fill it.

Related pages: the [judging session board](https://timmy97-tw.github.io/judging-session-prep/), the
[iGEM bioreactor landscape](https://timmy97-tw.github.io/igem-bioreactor-landscape/), the
[invariant explorer](https://timmy97-tw.github.io/releaf-invariant-explorer/), and
[V1 of this section](https://timmy97-tw.github.io/releaf-big-picture/).
