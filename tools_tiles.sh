#!/usr/bin/env bash
# Regenerate every tile asset in assets/img/tile/ as a TRANSPARENT cut-out.
#
# There is no white mat any more. A tile is the thing itself with its own
# outline, so the silhouette identifies the work before the label is read:
# Taiwan is Taiwan-shaped, the receptor is a V, the RNA is a cloverleaf, a
# whiteboard drawing is ink with nothing behind it.
#
# Three treatments, chosen by what the source IS:
#   photo  subject lifted out with the macOS Vision framework (tools_lift.swift,
#          VNGenerateForegroundInstanceMaskRequest). Offline, no model download.
#   ink    near-white knocked out, so pen/whiteboard/plot lines float. Used for
#          handwritten working and for figures rendered on white.
#   plain  already has an alpha channel (our own PyMOL renders); trim only.
#
# Requires: swiftc, ImageMagick 7, rsvg-convert, pymol (only for tools_render.py).
# Usage: ./tools_tiles.sh [key ...]      (no args = everything)
set -uo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
LIB="/Users/timmylin/Documents/Claude/Projects/iGEM2026_Images"
OUT="assets/img/tile"; TMP="$(mktemp -d)"; mkdir -p "$OUT"
trap 'rm -rf "$TMP"' EXIT

swiftc -O tools_lift.swift -o "$TMP/lift" 2>/dev/null

# our own PyMOL renders (transparent background, no burnt-in labels), and the
# SignalP output, which only ships as a zip
TMPRENDER="$TMP/render"; TMPSP="$TMP/sp"; mkdir -p "$TMPRENDER" "$TMPSP"
OUTDIR="$TMPRENDER" BPV2_DIR="$PWD" pymol -cq tools_render.py >/dev/null 2>&1
unzip -oq "$ROOT/00_Deliverable_Reports/24_0820_Student_SignalP analysis/output_all_results.zip" -d "$TMPSP"

# the tiles we draw ourselves, from our own data (tools_figures.py)
python3 tools_figures.py >/dev/null

# The island, rebuilt from our own QGIS layers rather than the flat export, so
# the tile is the same cartography as the map section further down: five
# volatility bands, then the small parcels back on top of them. Flat map.jpg was
# tried and it crops to a rectangle and loses the coastline, which is the whole
# reason this tile exists.
magick assets/img/map/base.webp \
       assets/img/map/v1.webp -composite assets/img/map/v2.webp -composite \
       assets/img/map/v3.webp -composite assets/img/map/v4.webp -composite \
       assets/img/map/v5.webp -composite assets/img/map/large.webp -composite \
       assets/img/map/sb1.webp -composite assets/img/map/sb2.webp -composite \
       assets/img/map/sb3.webp -composite assets/img/map/sb4.webp -composite \
       assets/img/map/sb5.webp -composite assets/img/map/edge.webp -composite \
       -modulate 100,122,100 "$TMP/taiwan_src.png"

# H is the rendered height of every cut-out at 2x. Widths follow the artwork,
# which is the whole point: tiles are not a grid.
H=340

emit() { # $1=key  $2=file with alpha
  magick "$2" -trim +repage -resize "x${H}>" \
     -define webp:alpha-quality=92 -quality 86 "$OUT/$1.webp"
  printf "  %-14s %s\n" "$1" "$(identify -format '%wx%h' "$OUT/$1.webp")"
}

do_photo() { # $1=key $2=src
  "$TMP/lift" "$2" "$TMP/$1.png" --all >/dev/null 2>&1 || { echo "  !! lift failed: $1"; return 1; }
  magick "$TMP/$1.png" -modulate 100,104,100 -unsharp 0x0.6+0.5+0.02 "$TMP/$1b.png"
  emit "$1" "$TMP/$1b.png"
}

do_ink() { # $1=key $2=src [3=crop geometry] [4=fuzz%]
  local crop="${3:-}" fz="${4:-14}"
  magick "$2" ${crop:+-crop $crop +repage} -bordercolor white -border 1 \
     -fuzz "${fz}%" -fill none -draw "alpha 0,0 floodfill" \
     -channel A -blur 0x0.4 -level 20%,80% +channel "$TMP/$1.png"
  emit "$1" "$TMP/$1.png"
}

do_crop_photo() { # $1=key $2=src $3=crop — lift picks the salient thing, and
                  # sometimes the salient thing is a picture on the wall behind
                  # the subject. Crop first, then lift.
  magick "$2" -crop "$3" +repage "$TMP/$1_c.png"
  do_photo "$1" "$TMP/$1_c.png"
}

do_board() { # $1=key $2=src [3=crop] [4=black pt] [5=white pt]
  local crop="${3:-}"
  magick "$2" ${crop:+-crop $crop +repage} -resize x1400 \
     -modulate 100,124,100 -channel RGB -contrast-stretch 1%x0.3% +channel \
     \( +clone -colorspace gray -negate -level "${4:-9}%,${5:-52}%" \) \
     -alpha off -compose CopyOpacity -composite "$TMP/$1.png"
  emit "$1" "$TMP/$1.png"
}

do_frame() { # $1=key $2=src [3=crop] — KEEP THE BACKGROUND.
  # Not every tile should be a cut-out. Where the PLACE is the evidence — a
  # farmer's plot, a grow wall four storeys high, a shelf of a competitor's
  # products, a bench under a glowing gel — lifting the subject out throws away
  # the thing that made the photograph worth taking. Those keep their frame:
  # a soft-cornered crop, no white mat, and the same contact shadow the
  # cut-outs get, so the two kinds sit on one page without arguing.
  local crop="${3:-}"
  magick "$2" ${crop:+-crop $crop +repage} -resize "x$((H * 2))^" \
     -gravity center -extent "$(printf %.0f $(echo "$H * 2 * 1.34" | bc -l))x$((H * 2))" \
     -modulate 100,104,100 -unsharp 0x0.6+0.4+0.02 "$TMP/$1_p.png"
  local w=$(identify -format %w "$TMP/$1_p.png") hh=$(identify -format %h "$TMP/$1_p.png")
  # the mask has to be black-on-white, not drawn on a transparent canvas:
  # CopyOpacity reads INTENSITY, and a transparent canvas has none
  magick -size "${w}x${hh}" xc:black -fill white \
     -draw "roundrectangle 0,0 $((w-1)),$((hh-1)) 18,18" "$TMP/$1_m.png"
  magick "$TMP/$1_p.png" "$TMP/$1_m.png" -alpha off -compose CopyOpacity -composite "$TMP/$1.png"
  emit "$1" "$TMP/$1.png"
}

do_gen() { # $1=key $2=svg in assets/img/gen — our own generated figures
  rsvg-convert -h 900 "assets/img/gen/$2" -o "$TMP/$1.png"
  emit "$1" "$TMP/$1.png"
}

do_ink2() { # $1=key $2=src $3=crop — same idea as do_ink, but the background
            # here is a plot grey rather than white
  magick "$2" -crop "$3" +repage \
     -fuzz 16% -transparent "srgb(98,93,90)" -fuzz 14% -transparent "srgb(88,84,81)" \
     -channel A -blur 0x0.6 -level 30%,75% +channel "$TMP/$1.png"
  emit "$1" "$TMP/$1.png"
}

do_plain() { emit "$1" "$2"; }        # already transparent
do_svg()  { rsvg-convert -h 900 "$2" -o "$TMP/$1.png"; do_ink "$1" "$TMP/$1.png" "" 6; }

# ── the manifest ──────────────────────────────────────────────────────────
# key  treatment  source (paths relative to ROOT, or absolute for the photo lib)
build_one() {
case "$1" in
# ── THE STRESS ──
# sensing and farmers keep their backgrounds: cut out, a person wiring a board
# becomes a floating arm and a farmer on her knees loses the plot she is kneeling in.
sensing)    do_frame  sensing    "$ROOT/WikiHomepage/img/building-2400.jpg";;
agar)       do_photo  agar       "$LIB/2026-07/Wetlab/W31  7_5-7_12/20260705_Wetlab_Photo_VerticalPlantAgarInspectionOutsideTheIncubator.jpg";;
rigs)       do_photo  rigs       "$ROOT/0828鄭/site/assets/img/p4.jpg";;
farmers)    do_frame  farmers    "$LIB/2026-07/HP/W33  7_19-7_26/20260721_HP_Photo_Outreach_FarmerChenOnHerKneesShowingSoilPlantsWith2StudentsAlsoLowInspecting.jpg";;
stressindex)do_gen    stressindex stressmeter.svg;;
taiwan)     do_ink    taiwan     "$TMP/taiwan_src.png" "" 6;;
dataphys)   do_photo  dataphys   "$LIB/2026-08/Drylab/W37  8-16-8-23/20260817_Photo_DataPhysicalizationModel.png";;
# ── THE PROTEIN ──
msa)        do_gen    msa        msa.svg;;
docking)    do_plain  docking    "$TMPRENDER/docking.png";;
# ── THE CELLS ──
signalp)    do_gen    signalp    signalpeptide.svg;;
codon)      do_ink    codon      "$ROOT/Codon Optimization/DNA files/vienna_rs_analysis/struct_BoPep4.png" "820x760+230+170" 8;;
genedesign) do_ink    genedesign "$ROOT/0828鄭/0828Photos/synbio-modules-1400.webp" "" 6;;
cassette)   do_ink    cassette   "$ROOT/00_Deliverable_Reports/0816_IDT_Send/figures/fig_cassette_map.png" "820x400+330+50" 4;;
# stacks of labelled transformation plates, and the bench they are on: nobody in
# frame once the top strip is cropped off, and it reads as cloning at a glance.
cloning)    do_frame  cloning    "$LIB/2026-07/Wetlab/W32  7_12-7_19/20260715_Wetlab_Photo_CasualTableOfPilesOfPlatesInLab.jpg" "2791x1740+0+400";;
# the glowing gel itself, not the room it was in
sequencing) do_frame  sequencing "$LIB/2026-06/Wetlab/W27  6_7-6_14/20260610_Wetlab_Photo_GelElectroporation.jpg" "820x560+1160+780";;
growth)     do_gen    growth     growthcurve.svg;;
# ── THE BIOREACTOR ──
# the cartridge on its own, out of our own flow schematic. No photograph of the
# module by itself exists anywhere in the archive.
membrane)   do_ink    membrane   "$LIB/2026-08/Drylab/W35  8_2-8_9/20260804_Drylab_Figure_BioreactorDesignFigureFullDesign.png" "460x1830+4260+1040" 5;;
photometer) do_photo  photometer "$LIB/2026-06/Drylab/W30  6_28-7_5/20260704_Drylab_Photo_PhotometerGreatTestingPhotoWithTheAmberLightVisibleInBox.jpg";;
tandemrun)  do_photo  tandemrun  "$LIB/2026-07/Drylab/W33  7_19-7_26/20260720_Drylab_Photo_Bioreactor_GreatPhotoOfBioreactorRunningInIncubatorWithSerumBottleHavingYellowBSubAndPlantsOnTheAboveFloor.jpg";;
lightarray) do_photo  lightarray "$LIB/2026-07/Drylab/W32  7_12-7_19/20260717_Drylab_Photo_LPA_3DPrintedMaterialArrivedAndOurFirstAssembledLookOfOurFullLPA.jpg";;
pressure)   do_ink    pressure   "$LIB/2026-08/Drylab/W35  8_2-8_9/20260804_Drylab_Figure_BioreactorDesignFigureFullDesign.png" "800x420+2950+620" 5;;
phsensor)   do_gen    phsensor   phprobe.svg;;
dosensor)   do_gen    dosensor   doprobe.svg;;
# ── THE FIELD ──
law)        do_gen    law        regulation.svg;;
transport)  do_ink2   transport  "$ROOT/0828鄭/0828Photos/MathModel.png" "200x330+470+110";;
realfarms)  do_frame  realfarms  "$LIB/2026-08/HP/W36  8_9-8_16/20260811_HP_Photo_Outreach_源先智慧農場_StudentsImpressedByTheHugeWallOfHydroponicFarmInFrontOfUsEverybodyHeadsUp_GreatPhoto.jpg";;
experts)    do_photo  experts    "$LIB/2026-06/HP/W28  6_14-6_21/20260620_HP_Photo_ProfChen陳文亮_Bioreactor_Great.jpg";;
cost)       do_frame  cost       "$LIB/2026-07/HP/W31  7_5-7_12/20260709_HP_Photo_正瀚Outreach_GreatPhotoOfResearcherExplainingToStudentsInFrontOfResearchPaperWallAndWithProductBottlesOnTheSide.jpg";;
*) echo "  ?? unknown key: $1";;
esac
}

KEYS="sensing agar rigs farmers stressindex taiwan dataphys
      msa docking
      signalp codon genedesign cassette cloning sequencing growth
      membrane photometer tandemrun lightarray pressure phsensor dosensor
      law transport realfarms experts cost"
[ $# -gt 0 ] && KEYS="$*"
for k in $KEYS; do build_one "$k"; done
echo "done -> $OUT"
