#!/bin/bash
# Pulls the QGIS export apart into the layers the page drives.
#
# In:  "Taiwan Farmland Distribution x Climate Volatility.pdf" (the version
#      WITHOUT division titles; the labelled one leaves county names in the
#      raster and they end up baked into every layer).
# Out: base, v1..v5, small, large, edge as 800px webp.
#
# The export is flat, so the only handle on it is colour. Quantising against a
# nine-entry palette of the legend's own swatches makes every pixel snap to a
# class exactly, which is what lets fuzz stay at 0 and the masks stay honest.
#
# The band layers come out with parcel-shaped holes, because the parcels were
# drawn over the choropleth before the export was flattened. Leave them. The
# page only ever draws a band as an overlay with the parcel layer above it,
# which fills the holes exactly. Closing them morphologically was tried and is
# wrong: small kernels do not fill them, large kernels redraw the counties.
set -e
SRC="$1"; OUT="${2:-.}"
[ -z "$SRC" ] && { echo "usage: $0 <qgis-export.pdf> [outdir]"; exit 1; }

sips -s format png -Z 2400 "$SRC" --out /tmp/clean.png >/dev/null
magick /tmp/clean.png -trim +repage /tmp/trim.png
# blank the legend, in three rectangles that follow its own bounding boxes;
# one rectangle wide enough to cover the top row would clip the island
magick /tmp/trim.png -fill white \
  -draw "rectangle 140,0 1697,400"    -draw "rectangle 140,400 1045,610" \
  -draw "rectangle 140,610 660,660"   -draw "rectangle 140,660 600,1015" /tmp/nolegend.png
magick /tmp/nolegend.png -crop 1130x1790+230+550 +repage /tmp/island.png

magick -size 9x1 xc:none \
  -fill '#ffffff' -draw 'point 0,0' -fill '#09204D' -draw 'point 1,0' -fill '#414D6B' -draw 'point 2,0' \
  -fill '#7D7C78' -draw 'point 3,0' -fill '#BEAF6F' -draw 'point 4,0' -fill '#FBEA4E' -draw 'point 5,0' \
  -fill '#9C1F14' -draw 'point 6,0' -fill '#1B02F3' -draw 'point 7,0' -fill '#000000' -draw 'point 8,0' /tmp/pal.png
magick /tmp/island.png -dither None -remap /tmp/pal.png /tmp/q.png

layer () {   # $1 source colour  $2 this page's colour  $3 name
  magick /tmp/q.png -alpha set -fuzz 0% -fill none +opaque "$1" -fill "$2" -opaque "$1" \
    -resize 800x -strip "PNG32:/tmp/m-$3.png"
}
layer '#09204D' '#eceadf' v1        # 0.38 to 0.49
layer '#414D6B' '#ddd8c2' v2        # 0.49 to 0.60
layer '#7D7C78' '#cbbf98' v3        # 0.60 to 0.71
layer '#BEAF6F' '#c2984e' v4        # 0.71 to 0.82
layer '#FBEA4E' '#9a3d22' v5        # 0.82 to 0.93
layer '#9C1F14' '#14402b' small     # parcels under two hectares
layer '#1B02F3' '#3f5468' large     # and over
layer '#000000' '#5b5f57' edge      # county lines
magick /tmp/q.png -alpha set -fuzz 0% -fill none -opaque '#ffffff' -fill '#f3f1ea' +opaque none \
  -resize 800x -strip PNG32:/tmp/m-sil.png

magick -size 800x1267 xc:none /tmp/m-sil.png -composite \
  /tmp/m-v1.png -composite /tmp/m-v2.png -composite /tmp/m-v3.png -composite \
  /tmp/m-v4.png -composite /tmp/m-v5.png -composite /tmp/m-edge.png -composite \
  /tmp/m-large.png -composite /tmp/m-small.png -composite -strip PNG32:/tmp/m-base.png

mkdir -p "$OUT"
for f in base v1 v2 v3 v4 v5 edge small large; do
  magick "/tmp/m-$f.png" -strip -quality 80 "$OUT/$f.webp"
done
echo "wrote 9 layers to $OUT"
