"""Assign every small-farm parcel to the volatility band of the ground around it.

The QGIS export is flat: the parcels were drawn over the choropleth, so at a
parcel pixel the band underneath is gone. It is recoverable, because the
choropleth is by administrative area and a parcel is tiny next to one: the band
that surrounds a parcel IS that parcel's band. This grows the band labels into
the parcel holes one pixel at a time until the holes are full, which is a
nearest-label fill, then counts the parcels per band.
"""
import subprocess, numpy as np, json

def read_ppm(path):
    raw = subprocess.run(["magick", path, "-depth", "8", "ppm:-"], capture_output=True).stdout
    # P6\n<w> <h>\n255\n
    parts, i = [], 0
    while len(parts) < 4:
        j = raw.index(b"\n", i); tok = raw[i:j].split(); parts += tok; i = j + 1
    w, h = int(parts[1]), int(parts[2])
    return np.frombuffer(raw[i:i + w*h*3], dtype=np.uint8).reshape(h, w, 3)

img = read_ppm("q.png")
H, W, _ = img.shape
def is_(hexs):
    r, g, b = int(hexs[1:3],16), int(hexs[3:5],16), int(hexs[5:7],16)
    return (img[:,:,0]==r) & (img[:,:,1]==g) & (img[:,:,2]==b)

BANDS = ['#09204D', '#414D6B', '#7D7C78', '#BEAF6F', '#FBEA4E']
small = is_('#9C1F14')
label = np.zeros((H, W), dtype=np.uint8)
for n, hx in enumerate(BANDS, start=1):
    label[is_(hx)] = n

# grow the labels into everything unlabelled (parcels, county lines) until full
free = label == 0
inside = free & ~is_('#ffffff')          # only fill holes on land
work = label.copy()
for _ in range(60):
    if not (work[inside] == 0).any(): break
    cand = np.zeros_like(work)
    for sh, ax in ((1,0), (-1,0), (1,1), (-1,1)):
        cand = np.maximum(cand, np.roll(work, sh, axis=ax))
    grow = (work == 0) & inside & (cand > 0)
    work[grow] = cand[grow]

counts = [int(((work == n) & small).sum()) for n in range(1, 6)]
tot = sum(counts)
print("small-farm pixels per band, calmest to worst:", counts)
print("total", tot, "unassigned", int((small & (work == 0)).sum()))
print("share of small-farm area per band:", [round(100*c/tot, 1) for c in counts])
print("cumulative from the worst end:", [round(100*sum(counts[i:])/tot, 1) for i in range(5)])

# write one mask per band: the small farms sitting on that band
for n in range(1, 6):
    m = ((work == n) & small).astype(np.uint8) * 255
    with open(f"/tmp/band{n}.pgm", "wb") as f:
        f.write(b"P5\n%d %d\n255\n" % (W, H)); f.write(m.tobytes())
json.dump({"counts": counts, "total": tot}, open("band_counts.json", "w"))

# how much land is in each band at all, so the parcels can be read as a rate
land = [int((work == n).sum()) for n in range(1, 6)]
print("\nland pixels per band, calmest to worst:", land)
print("share of all land per band:", [round(100*l/sum(land),1) for l in land])
print("small-farm share OF each band (density):", [round(100*counts[i]/land[i],1) for i in range(5)])
large = is_('#1B02F3')
lg = [int(((work == n) & large).sum()) for n in range(1,6)]
print("large-farm pixels per band:", lg)
print("large-farm share of each band:", [round(100*lg[i]/land[i],2) for i in range(5)])
print("small:large ratio per band:", [round(counts[i]/max(lg[i],1),1) for i in range(5)])
