# Our own structures, re-rendered for the tiles.
#
# The report figures in Haddock/BoPep4-PEPR1-results/latex-source/figs are the
# right science but the wrong artwork for a 130px tile: they are drawn on opaque
# white and they carry burnt-in text labels that turn to noise at this size. So
# the tile renders the SAME top-scoring complexes from the SAME PDB files, with
# ray_opaque_background off and no labels at all, and lets the receptor's own
# outline be the label.
#
#   run: OUTDIR=/some/dir pymol -cq tools_render.py
from pymol import cmd
import os

HERE = os.environ.get("BPV2_DIR", os.getcwd())
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT  = os.environ.get("OUTDIR", HERE)
H    = os.path.join(ROOT, "Haddock", "BoPep4-PEPR1-results")

WT = os.path.join(H, "BoPep4-PEPR1_native-mode_top.pdb")        # BoPep4, canonical mode
AT = os.path.join(H, "AtPep1-PEPR1_validation_top.pdb")         # AtPep1 control, 5GR8-validated


def base():
    for k, v in dict(ray_opaque_background=0, ray_shadows=0, antialias=2,
                     cartoon_fancy_helices=1, cartoon_side_chain_helper=1,
                     ambient=0.42, specular=0.18, depth_cue=0, surface_quality=1,
                     transparency_mode=1, opaque_background=0,
                     cartoon_flat_sheets=1).items():
        cmd.set(k, v)


def peptide(sel, col, tube=0.72, stick=0.36):
    """A peptide has to survive being 40px across, so it is drawn fat."""
    cmd.show('cartoon', sel); cmd.show('sticks', sel)
    cmd.cartoon('tube', sel); cmd.set('cartoon_tube_radius', tube)
    cmd.set('stick_radius', stick, sel); cmd.color(col, sel)


# ── docking: BoPep4 (blue) superposed on the AtPep1 control (orange) ──────────
# Receptor alignment first, then both peptides in the same groove. This is the
# claim of fig4 in the report — the two track each other across the conserved
# C-terminus — with the V of the PEPR1 LRR ectodomain carrying the silhouette.
cmd.reinitialize(); base()
cmd.load(WT, 'wt'); cmd.load(AT, 'at')
cmd.align('at and chain A', 'wt and chain A')
cmd.hide('everything')
cmd.show('surface', 'wt and chain A')
cmd.color('grey88', 'wt and chain A')
# 0.30 made the receptor a flat grey mass that outweighed every other
# tile on the page. At 0.56 the V still carries the silhouette and the two
# peptides in the groove are what you actually see.
cmd.set('transparency', 0.56, 'wt and chain A')
peptide('wt and chain B', 'marine', 0.86, 0.42)
peptide('at and chain B', 'orange', 0.86, 0.42)
cmd.orient('wt'); cmd.turn('y', 18); cmd.turn('x', -12); cmd.zoom('wt', 1.6)
cmd.ray(1700, 1180); cmd.png(os.path.join(OUT, 'docking.png'), dpi=200)
print('wrote docking.png')
