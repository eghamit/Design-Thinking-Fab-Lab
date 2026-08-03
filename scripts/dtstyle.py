"""Shared styling helpers for Design Thinking & Fabrication Lab figures.

Provides a consistent colour palette and a set of drawing primitives
(rounded boxes, arrows, chips, circular badges) used across all figures.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Rectangle
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm

# ---------------------------------------------------------------- palette
INK      = "#22333B"   # near-black text
NAVY     = "#264653"   # dark teal (headings / dark boxes)
TEAL     = "#2A9D8F"   # green-teal
BLUE     = "#2A6F97"   # primary blue
SKY      = "#61A5C2"   # light blue
YELLOW   = "#E9C46A"   # sand yellow
ORANGE   = "#F4A261"   # orange
CORAL    = "#E76F51"   # coral / red-orange
PLUM     = "#7B506F"   # muted plum
MOSS     = "#6A994E"   # green
PAPER    = "#FBF9F5"   # warm paper background
CLOUD    = "#EDF2F4"   # very light grey-blue
GRID     = "#D8DEE4"

# Ordered accent cycle for multi-item diagrams
CYCLE = [BLUE, TEAL, ORANGE, CORAL, PLUM, MOSS, SKY, YELLOW]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "text.color": INK,
    "axes.edgecolor": INK,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})


def new_ax(w=10, h=6, bg="white", xlim=(0, 100), ylim=(0, 100)):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc, ec=None, text="", tc="white", fs=13,
         weight="bold", radius=0.03, lw=1.6, alpha=1.0, ha="center",
         va="center", zorder=2, pad=0.0, style="round"):
    """Rounded rectangle centred at (x, y) with wrapped text."""
    ec = ec or fc
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad={pad},rounding_size={radius*min(w,h)*10}",
        linewidth=lw, edgecolor=ec, facecolor=fc, alpha=alpha, zorder=zorder,
    )
    ax.add_patch(box)
    if text:
        tx = x if ha == "center" else x - w / 2 + 2
        ax.text(tx, y, text, ha=ha, va=va, color=tc, fontsize=fs,
                weight=weight, zorder=zorder + 1, wrap=True)
    return box


def chip(ax, x, y, w, h, fc, text, tc="white", fs=12, weight="bold", ec=None,
         zorder=3):
    ec = ec or fc
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=%.2f" % (h * 0.45),
        linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=zorder)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", color=tc, fontsize=fs,
            weight=weight, zorder=zorder + 1)
    return box


def arrow(ax, p0, p1, color=INK, lw=2.2, style="-|>", mut=20, rad=0.0,
          ls="-", zorder=1, alpha=1.0):
    a = FancyArrowPatch(
        p0, p1, arrowstyle=style, mutation_scale=mut, lw=lw, color=color,
        connectionstyle=f"arc3,rad={rad}", linestyle=ls, zorder=zorder,
        alpha=alpha, capstyle="round")
    ax.add_patch(a)
    return a


def badge(ax, x, y, r, fc, text, tc="white", fs=15, ec="white", lw=2.5,
          weight="bold", zorder=4):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=lw,
                        zorder=zorder))
    ax.text(x, y, text, ha="center", va="center", color=tc, fontsize=fs,
            weight=weight, zorder=zorder + 1)


def title(ax, text, x=50, y=95, fs=19, color=NAVY, sub=None, subfs=12.5,
          subcolor="#5B6B73"):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, weight="bold",
            color=color)
    if sub:
        ax.text(x, y - 6, sub, ha="center", va="center", fontsize=subfs,
                color=subcolor, style="italic")


def radial_cycle(ax, cx, cy, R, steps, box_w=22, box_h=13, fs=11,
                 center_fc=None, center_text="", arrow_color=None, rad=-0.30,
                 center_fs=9):
    """steps: list of (name, colour, angle_deg). Draws boxes around a ring
    with curved directional arrows that meet the box edges cleanly."""
    import math
    pts = []
    for name, col, ang in steps:
        a = math.radians(ang)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pts.append((x, y, col, a))
        rbox(ax, x, y, box_w, box_h, col, text=name, fs=fs)
    n = len(pts)
    for i in range(n):
        x0, y0, c0, a0 = pts[i]
        x1, y1, c1, a1 = pts[(i + 1) % n]
        ac = arrow_color or c1
        off = 0.42
        p0 = (cx + (R - 1) * math.cos(a0 - off),
              cy + (R - 1) * math.sin(a0 - off))
        p1 = (cx + (R - 1) * math.cos(a1 + off),
              cy + (R - 1) * math.sin(a1 + off))
        arrow(ax, p0, p1, color=ac, lw=3, rad=rad, mut=20)
    if center_fc:
        badge(ax, cx, cy, R * 0.40, center_fc, "", ec="white", lw=2)
        ax.text(cx, cy, center_text, ha="center", va="center",
                fontsize=center_fs, weight="bold", color="white", zorder=6)
    return pts


def save(fig, name, folder="figures"):
    import os
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.15,
                facecolor="white")
    plt.close(fig)
    print("wrote", path)
