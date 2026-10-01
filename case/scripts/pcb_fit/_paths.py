"""Repo-relative paths for the PCB-variant fit scripts.

Run every script from this folder:  cd case/scripts/pcb_fit && python <script>.py
Intermediate files (*.npz, placement_*.json, PNG previews) are written to the current folder.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))           # repo/case/scripts/pcb_fit
SCRIPTS = os.path.dirname(HERE)                              # repo/case/scripts (fit_tatakan_gmt130.py)
CASE_DIR = os.path.dirname(SCRIPTS)                          # repo/case
REPO = os.path.dirname(CASE_DIR)
for _p in (SCRIPTS, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

CASE_ORIG = os.path.join(CASE_DIR, 'case_luar_lcd_23_40mm.stl')       # original shell (unchanged)
STAND_ORIG = os.path.join(CASE_DIR, 'tatakan_GMT130_fit.stl')         # GMT130 stand, loose-wiring variant
CASE_PCB = os.path.join(CASE_DIR, 'case_luar_lcd_23_40mm_pcb.stl')    # shell for the PCB variant
STAND_PCB = os.path.join(CASE_DIR, 'tatakan_GMT130_fit_pcb.stl')      # stand for the PCB variant
OUTLINE_V2 = os.path.join(REPO, 'pcb', 'outline', 'pcb_recommended_outline_v2.json')
LAYOUT_V3 = os.path.join(REPO, 'pcb', 'v3', 'layout_v3_case_frame.json')
LAYOUT_V3_SVG = os.path.join(REPO, 'pcb', 'v3', 'layout_case_frame.svg')
DOCS_FIT = os.path.join(REPO, 'docs', 'fit')
PLACEMENT_V7_VERIFIED = os.path.join(DOCS_FIT, 'placement_pcb_v7_cap6.3_verified.json')
