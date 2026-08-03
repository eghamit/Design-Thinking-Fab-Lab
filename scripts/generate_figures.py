#!/usr/bin/env python3
"""Generate every figure used in the Design Thinking & Fabrication Lab deck.

All output PNGs are written to ../figures relative to this script.
Run:  python3 scripts/generate_figures.py
"""
import os, sys, math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle
sys.path.insert(0, os.path.dirname(__file__))
from dtstyle import (INK, NAVY, TEAL, BLUE, SKY, YELLOW, ORANGE, CORAL, PLUM,
                     MOSS, PAPER, CLOUD, GRID, CYCLE, new_ax, rbox, chip,
                     arrow, badge, title, save, radial_cycle)

FIG = os.path.join(os.path.dirname(__file__), "..", "figures")


# ======================================================================
#  COVER / OVERVIEW
# ======================================================================
def cover():
    fig, ax = new_ax(11, 6.2, bg=NAVY)
    ax.add_patch(Rectangle((0, 0), 100, 100, facecolor=NAVY, zorder=0))
    # scattered translucent "idea" bubbles
    rng = np.random.default_rng(7)
    for c in CYCLE:
        for _ in range(3):
            x, y = rng.uniform(6, 94), rng.uniform(8, 92)
            r = rng.uniform(2, 6)
            ax.add_patch(Circle((x, y), r, facecolor=c, alpha=0.14, zorder=1))
    # central lightbulb-in-gear motif
    cx, cy = 50, 55
    teeth = 12
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        ax.add_patch(Rectangle((cx + 20 * math.cos(a) - 2.2,
                                cy + 20 * math.sin(a) - 2.2), 4.4, 4.4,
                               angle=math.degrees(a), facecolor=ORANGE,
                               zorder=2))
    ax.add_patch(Circle((cx, cy), 20, facecolor=YELLOW, ec="white", lw=3,
                        zorder=3))
    ax.add_patch(Circle((cx, cy), 12.5, facecolor=PAPER, zorder=4))
    # simple light-bulb glyph drawn from primitives
    ax.add_patch(Circle((cx, cy + 2), 7, facecolor=ORANGE, ec=NAVY, lw=2,
                        zorder=5))
    ax.add_patch(Rectangle((cx - 3, cy - 9), 6, 4, facecolor=NAVY, zorder=5))
    for fy in (-6.5, -5.2):
        ax.add_patch(Rectangle((cx - 3, cy + fy), 6, 0.9, facecolor=PAPER,
                               zorder=6))
    for dx in (-1.6, 0, 1.6):
        ax.plot([cx + dx, cx + dx], [cy - 1, cy + 6], color=PAPER, lw=1.4,
                zorder=6)
    ax.text(50, 22, "DESIGN THINKING", ha="center", va="center", fontsize=30,
            weight="bold", color="white", zorder=5)
    ax.text(50, 13, "& FABRICATION LABORATORY", ha="center", va="center",
            fontsize=17, weight="bold", color=YELLOW, zorder=5)
    save(fig, "cover.png", FIG)


def course_map():
    fig, ax = new_ax(11, 6.2)
    title(ax, "Course Roadmap — Five Units, One Journey", y=96)
    units = [
        ("I", "Insight to\nLearning", BLUE, "How we learn,\nremember &\nempathise"),
        ("II", "Basics of\nDesign\nThinking", TEAL, "The 5-stage\nmindset &\nprocess"),
        ("III", "Process of\nProduct\nDesign", ORANGE, "Engineering\ndesign &\nprototyping"),
        ("IV", "Customer\nCentricity", CORAL, "Experience,\nfeedback &\nre-design"),
        ("V", "Fabrication\nLaboratory", PLUM, "Route-map,\nCREATE, CJM,\nHMW, blueprint"),
    ]
    xs = np.linspace(13, 87, 5)
    y = 56
    # connecting road
    ax.plot([8, 92], [y, y], color=GRID, lw=10, zorder=0,
            solid_capstyle="round")
    for i, (num, name, col, desc) in enumerate(units):
        x = xs[i]
        badge(ax, x, y, 6.2, col, num, fs=17)
        rbox(ax, x, y + 22, 16, 14, "white", ec=col, tc=INK, text=name,
             fs=10.5, lw=2)
        rbox(ax, x, y - 21, 16, 14, CLOUD, ec=GRID, tc="#42525A",
             text=desc, fs=9, weight="normal", lw=1.2)
        # connector ticks
        arrow(ax, (x, y + 6.2), (x, y + 15), color=col, lw=1.8, mut=13)
        arrow(ax, (x, y - 6.2), (x, y - 14), color=col, lw=1.8, mut=13)
    ax.text(50, 8, "15 hours per unit  ·  75 hours total  ·  theory + hands-on fabrication",
            ha="center", fontsize=11.5, style="italic", color="#5B6B73")
    save(fig, "course_map.png", FIG)


# ======================================================================
#  UNIT I  —  AN INSIGHT TO LEARNING
# ======================================================================
def kolb_cycle():
    fig, ax = new_ax(8.6, 8.2)
    title(ax, "Kolb's Experiential Learning Cycle", y=99, fs=17,
          sub="Learning as a continuous four-stage loop")
    cx, cy, R = 50, 47, 25
    stages = [
        ("CONCRETE\nEXPERIENCE", "Feeling — having an experience", TEAL, 90),
        ("REFLECTIVE\nOBSERVATION", "Watching — reviewing it", BLUE, 0),
        ("ABSTRACT\nCONCEPTUALISATION", "Thinking — forming ideas", ORANGE, 270),
        ("ACTIVE\nEXPERIMENTATION", "Doing — trying it out", CORAL, 180),
    ]
    steps = [(n, c, a) for n, d, c, a in stages]
    radial_cycle(ax, cx, cy, R, steps, box_w=34, box_h=15, fs=11.5,
                 center_fc=NAVY, center_text="EXPERIENTIAL\nLEARNING")
    for name, desc, col, ang in stages:
        a = math.radians(ang)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        if abs(math.sin(a)) > 0.5:          # top / bottom box → label outside vertically
            dx, dy = x, y + (11.5 if math.sin(a) > 0 else -11.5)
        else:                                # side box → label below the box
            dx, dy = x, y - 11.5
        ax.text(dx, dy, desc, ha="center", va="center", fontsize=9,
                color="#42525A", style="italic")
    save(fig, "kolb_cycle.png", FIG)


def kolb_styles():
    fig, ax = new_ax(9.4, 7.0)
    title(ax, "Kolb's Four Learning Styles", y=97,
          sub="Formed by how learners grasp and transform experience")
    # axes
    ax.annotate("", xy=(50, 83), xytext=(50, 15),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.annotate("", xy=(88, 50), xytext=(12, 50),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.text(50, 85.8, "Concrete Experience (Feeling)", ha="center", fontsize=9.5,
            weight="bold", color=TEAL)
    ax.text(50, 11.5, "Abstract Conceptualisation (Thinking)", ha="center",
            fontsize=9.5, weight="bold", color=ORANGE)
    ax.text(8, 50, "Reflective\nObservation\n(Watching)", ha="center",
            va="center", fontsize=8.5, weight="bold", color=BLUE)
    ax.text(92, 50, "Active\nExperimentation\n(Doing)", ha="center",
            va="center", fontsize=8.5, weight="bold", color=CORAL)
    quads = [
        (32, 68, PLUM, "DIVERGING", "Feel + Watch", "Imaginative, empathic,\nbrainstorms many ideas"),
        (68, 68, TEAL, "ACCOMMODATING", "Feel + Do", "Hands-on, intuitive,\nlearns by trial"),
        (32, 32, BLUE, "ASSIMILATING", "Think + Watch", "Logical, concise,\nloves models & theory"),
        (68, 32, CORAL, "CONVERGING", "Think + Do", "Practical, solves\nproblems technically"),
    ]
    for x, y, col, nm, tag, desc in quads:
        rbox(ax, x, y, 31, 26, col, radius=0.02, alpha=0.92)
        ax.text(x, y + 8, nm, ha="center", va="center", fontsize=12.5,
                weight="bold", color="white")
        ax.text(x, y + 2.5, tag, ha="center", va="center", fontsize=9.5,
                color="white", style="italic")
        ax.text(x, y - 5, desc, ha="center", va="center", fontsize=8.8,
                color="white")
    save(fig, "kolb_styles.png", FIG)


def memory_process():
    fig, ax = new_ax(11, 5.6)
    title(ax, "The Memory Process — Information-Processing Model", y=95)
    boxes = [
        (15, 55, SKY, "Sensory\nMemory", "Sight, sound, touch\n(< 1 second)", 20),
        (44, 55, BLUE, "Short-Term /\nWorking\nMemory", "~7 items,\n15–30 seconds", 22),
        (78, 55, TEAL, "Long-Term\nMemory", "Vast, potentially\npermanent store", 20),
    ]
    for x, y, col, nm, desc, w in boxes:
        rbox(ax, x, y, w, 18, col, text=nm, fs=11.5)
        ax.text(x, y - 14, desc, ha="center", va="center", fontsize=9,
                color="#42525A", style="italic")
    arrow(ax, (25, 55), (33, 55), color=INK, lw=2.4)
    ax.text(29, 61, "Attention", ha="center", fontsize=8.5, color=NAVY,
            weight="bold")
    arrow(ax, (55, 55), (68, 55), color=INK, lw=2.4)
    ax.text(60.5, 61, "Encoding /\nRehearsal", ha="center", fontsize=8.5,
            color=NAVY, weight="bold")
    arrow(ax, (68, 49), (53, 49), color=CORAL, lw=2.4)
    ax.text(60.5, 43.5, "Retrieval", ha="center", fontsize=8.5, color=CORAL,
            weight="bold")
    # forgetting exits
    for x, lbl in [(15, "decay"), (43, "displacement")]:
        arrow(ax, (x, 46), (x, 34), color="#9AA5AB", lw=1.8, mut=15)
        ax.text(x, 30, "Forgetting\n(%s)" % lbl, ha="center", fontsize=8.2,
                color="#9AA5AB")
    # retention problem callout
    rbox(ax, 78, 24, 40, 14, CLOUD, ec=GRID, tc=INK,
         text="Retention problems: interference, weak encoding, lack of cues.\n"
              "Enhancement: chunking, mnemonics, spaced rehearsal, elaboration.",
         fs=9.2, weight="normal", lw=1.3)
    save(fig, "memory_process.png", FIG)


def forgetting_curve():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    fig.patch.set_facecolor("white")
    t = np.linspace(0, 6, 300)
    base = 100 * np.exp(-t / 1.3) + 12
    ax.plot(t, base, color=CORAL, lw=3, label="Without review (Ebbinghaus)")
    # spaced repetition sawtooth
    ax.plot(t, base, color=CORAL, lw=3)
    reviews = [1, 2, 3.2, 4.6]
    xs = np.linspace(0, 6, 600)
    y = 100 * np.exp(-xs / 1.3) + 12
    last = 0
    curve = np.copy(y)
    boost = np.zeros_like(xs)
    decay = 1.3
    level = 100
    seg_y = []
    reset_points = [0] + reviews
    for i, x in enumerate(xs):
        # find last review before x
        r = max([rp for rp in reset_points if rp <= x])
        idx = reset_points.index(r)
        strength = decay * (1 + 0.9 * idx)  # slower decay after each review
        seg_y.append(100 * np.exp(-(x - r) / strength) + 12)
    seg_y = np.array(seg_y)
    ax.plot(xs, seg_y, color=TEAL, lw=3, label="With spaced repetition")
    for r in reviews:
        yy = 100 * np.exp(0) + 12
        ax.axvline(r, color=GRID, ls="--", lw=1)
        ax.annotate("review", (r, 108), ha="center", fontsize=8, color=TEAL)
    ax.set_xlabel("Time elapsed (days)")
    ax.set_ylabel("Memory retention (%)")
    ax.set_title("Ebbinghaus Forgetting Curve & Spaced Repetition",
                 fontsize=15, weight="bold", color=NAVY)
    ax.set_ylim(0, 118)
    ax.set_xlim(0, 6)
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    save(fig, "forgetting_curve.png", FIG)


def empathy():
    fig, ax = new_ax(10.5, 5.8)
    title(ax, "Emotions, Empathy & Emotional Intelligence", y=95,
          sub="Understanding emotions is the gateway to human-centred design")
    # left: three types of empathy
    types = [
        ("Cognitive\nEmpathy", "Understanding\nanother's perspective", BLUE, "◉"),
        ("Emotional\nEmpathy", "Feeling what\nanother feels", CORAL, "♥"),
        ("Compassionate\nEmpathy", "Moved to help\nand take action", TEAL, "✧"),
    ]
    for i, (nm, desc, col, sym) in enumerate(types):
        y = 70 - i * 21
        badge(ax, 14, y, 6, col, sym, fs=18, tc="white")
        rbox(ax, 43, y, 38, 16, "white", ec=col, tc=INK, text="", lw=2)
        ax.text(43, y + 3.5, nm.replace("\n", " "), ha="center", va="center",
                fontsize=11, weight="bold", color=col)
        ax.text(43, y - 3.5, desc.replace("\n", " "), ha="center", va="center",
                fontsize=9, color="#42525A")
    # right: EI pillars
    rbox(ax, 84, 58, 28, 58, CLOUD, ec=GRID, tc=INK, text="", lw=1.4)
    ax.text(84, 82, "Goleman's EI Pillars", ha="center", fontsize=10.5,
            weight="bold", color=NAVY)
    pillars = ["Self-awareness", "Self-regulation", "Motivation",
               "Empathy", "Social skills"]
    for i, p in enumerate(pillars):
        chip(ax, 84, 74 - i * 8.2, 24, 6, CYCLE[i], p, fs=9.5)
    ax.text(50, 10, "Assessing empathy with peers → empathy maps, "
            "shadowing, and active-listening interviews",
            ha="center", fontsize=10, style="italic", color="#5B6B73")
    save(fig, "empathy.png", FIG)


# ======================================================================
#  UNIT II  —  BASICS OF DESIGN THINKING
# ======================================================================
def dt_process():
    fig, ax = new_ax(11.5, 5.6)
    title(ax, "The Five Stages of Design Thinking", y=95,
          sub="Non-linear and iterative — teams loop back as they learn")
    stages = [
        ("EMPATHIZE", "Understand\nusers' needs", BLUE),
        ("DEFINE", "Frame the\nproblem", TEAL),
        ("IDEATE", "Generate\nmany ideas", YELLOW),
        ("PROTOTYPE", "Build quick\nmodels", ORANGE),
        ("TEST", "Try with\nusers", CORAL),
    ]
    xs = np.linspace(12, 88, 5)
    y = 58
    bw = 16.5
    for i, (nm, desc, col) in enumerate(stages):
        x = xs[i]
        tc = INK if col == YELLOW else "white"
        rbox(ax, x, y, bw, 21, col, radius=0.04)
        badge(ax, x, y + 6, 3.7, "white", str(i + 1), tc=col, fs=13, ec=col,
              lw=2)
        ax.text(x, y - 4, nm, ha="center", va="center", fontsize=8.4,
                weight="bold", color=tc)
        ax.text(x, y - 18, desc, ha="center", va="center", fontsize=9,
                color="#42525A")
        if i < 4:                                   # short chevron in the gap
            gap_mid = (x + xs[i + 1]) / 2
            ax.text(gap_mid, y, "›", ha="center", va="center", fontsize=20,
                    weight="bold", color=NAVY)
    # iteration loop back (below captions)
    arrow(ax, (xs[4], 30), (xs[1], 30), color=CORAL, lw=2, ls="--",
          rad=0.32, mut=16)
    ax.text(50, 22, "iterate — test insights re-shape the problem",
            ha="center", fontsize=9, color=CORAL, style="italic")
    save(fig, "dt_process.png", FIG)


def double_diamond():
    fig, ax = new_ax(11, 5.6)
    title(ax, "The Double Diamond", y=96,
          sub="Alternating divergent (explore) and convergent (focus) thinking")
    y0, h = 45, 26
    # diamond 1
    d1 = Polygon([(10, y0), (32, y0 + h/2), (54, y0), (32, y0 - h/2)],
                 closed=True, facecolor=BLUE, alpha=0.85, ec="white", lw=2)
    d2 = Polygon([(54, y0), (76, y0 + h/2), (98, y0), (76, y0 - h/2)],
                 closed=True, facecolor=ORANGE, alpha=0.9, ec="white", lw=2)
    ax.add_patch(d1); ax.add_patch(d2)
    ax.text(22, y0, "DISCOVER", ha="center", fontsize=11, weight="bold",
            color="white")
    ax.text(43, y0, "DEFINE", ha="center", fontsize=11, weight="bold",
            color="white")
    ax.text(65, y0, "DEVELOP", ha="center", fontsize=11, weight="bold",
            color="white")
    ax.text(87, y0, "DELIVER", ha="center", fontsize=11, weight="bold",
            color="white")
    # diverge / converge halves
    for xx, lbl in [(22, "diverge"), (43, "converge"),
                    (65, "diverge"), (87, "converge")]:
        ax.text(xx, y0 - h/2 - 4, lbl, ha="center", fontsize=8.5,
                color="#5B6B73", style="italic")
    ax.text(32, y0 - h/2 - 9.5, "Right problem", ha="center", fontsize=9.5,
            color=BLUE, weight="bold")
    ax.text(76, y0 - h/2 - 9.5, "Right solution", ha="center", fontsize=9.5,
            color=ORANGE, weight="bold")
    chip(ax, 32, 82, 30, 9, BLUE, "PROBLEM SPACE", fs=10)
    chip(ax, 76, 82, 30, 9, ORANGE, "SOLUTION SPACE", fs=10)
    ax.text(54, y0 + h/2 + 5, "◆ brief", ha="center", fontsize=9.5, color=NAVY,
            weight="bold")
    save(fig, "double_diamond.png", FIG)


def divergent_convergent():
    fig, ax = new_ax(10.5, 5.6)
    title(ax, "Brainstorming — Divergent then Convergent Thinking", y=96)
    # divergent fan
    ax.text(14, 50, "Seed\nproblem", ha="center", va="center", fontsize=10,
            weight="bold", color="white",
            bbox=dict(boxstyle="round", fc=NAVY, ec=NAVY))
    ends = np.linspace(20, 80, 7)
    for i, ey in enumerate(ends):
        arrow(ax, (20, 50), (46, ey), color=CYCLE[i % len(CYCLE)], lw=2, mut=15)
        chip(ax, 52, ey, 12, 6, CYCLE[i % len(CYCLE)], "idea", fs=8.5)
    # converge
    for ey in ends:
        arrow(ax, (58, ey), (82, 50), color="#9AA5AB", lw=1.6, mut=13)
    ax.text(90, 50, "Best\nconcept", ha="center", va="center", fontsize=10,
            weight="bold", color="white",
            bbox=dict(boxstyle="round", fc=CORAL, ec=CORAL))
    ax.text(33, 12, "DIVERGE — generate many ideas, defer judgement, go wild",
            ha="center", fontsize=10, color=BLUE, weight="bold")
    ax.text(72, 6, "CONVERGE — group, evaluate & select",
            ha="center", fontsize=10, color=CORAL, weight="bold")
    ax.text(33, 88, "Rules: quantity over quality · build on others · "
            "one conversation · stay visual", ha="center", fontsize=9.2,
            style="italic", color="#5B6B73")
    save(fig, "divergent_convergent.png", FIG)


def creative_problem_solving():
    fig, ax = new_ax(10.5, 5.4)
    title(ax, "Creative Problem-Solving Process", y=95)
    steps = [
        ("Clarify", "Explore,\ngather data,\nframe the\nquestion", BLUE),
        ("Ideate", "Generate,\ndevelop &\nrefine ideas", TEAL),
        ("Develop", "Evaluate,\nselect &\nstrengthen\nsolution", ORANGE),
        ("Implement", "Plan, gain\nbuy-in &\ntake action", CORAL),
    ]
    xs = np.linspace(16, 84, 4)
    y = 52
    for i, (nm, desc, col) in enumerate(steps):
        x = xs[i]
        badge(ax, x, y + 16, 5.5, col, str(i + 1), fs=15)
        rbox(ax, x, y - 7, 20, 26, "white", ec=col, tc=INK,
             text="", lw=2.2)
        ax.text(x, y + 1, nm, ha="center", va="center", fontsize=11,
                weight="bold", color=col)
        ax.text(x, y - 10, desc, ha="center", va="center", fontsize=8,
                color="#42525A", weight="normal")
        if i < 3:
            arrow(ax, (x + 6.5, y + 16), (xs[i + 1] - 6.5, y + 16),
                  color=NAVY, lw=2.2)
    ax.text(50, 12, "Testing creative problem solving: judge originality, "
            "fluency, flexibility & elaboration of ideas", ha="center",
            fontsize=9.5, style="italic", color="#5B6B73")
    save(fig, "creative_problem_solving.png", FIG)


# ======================================================================
#  UNIT III  —  PROCESS OF PRODUCT DESIGN
# ======================================================================
def product_design_process():
    fig, ax = new_ax(11.5, 5.4)
    title(ax, "Engineering Product-Design Process", y=95)
    steps = ["Identify\nNeed", "Define\nProblem", "Research\n& Specs",
             "Concept\nGen.", "Detailed\nDesign", "Prototype\n& Test",
             "Make &\nLaunch"]
    xs = np.linspace(9, 91, 7)
    y = 55
    for i, s in enumerate(steps):
        col = CYCLE[i % len(CYCLE)]
        # chevron
        w = 13.5
        chev = Polygon([(xs[i]-w/2, y+8), (xs[i]+w/2-2.5, y+8),
                        (xs[i]+w/2+2.5, y), (xs[i]+w/2-2.5, y-8),
                        (xs[i]-w/2, y-8), (xs[i]-w/2+2.5, y)],
                       closed=True, facecolor=col, ec="white", lw=1.5)
        ax.add_patch(chev)
        ax.text(xs[i] + 1, y, s, ha="center", va="center", fontsize=7.5,
                weight="bold", color="white")
        ax.text(xs[i], y + 13, "%d" % (i + 1), ha="center", fontsize=10,
                weight="bold", color=col)
    # feedback loop
    arrow(ax, (xs[5], y - 13), (xs[2], y - 13), color=CORAL, lw=1.8,
          ls="--", rad=0.28, mut=15)
    ax.text((xs[2]+xs[5])/2, 30, "iterate on test results", ha="center",
            fontsize=8.5, color=CORAL)
    ax.text(50, 22, "design-thinking approach keeps the user in the loop at every stage",
            ha="center", fontsize=9.5, style="italic", color="#5B6B73")
    save(fig, "product_design_process.png", FIG)


def prototype_fidelity():
    fig, ax = new_ax(10, 5.8)
    title(ax, "Prototype Fidelity Ladder", y=96,
          sub="From cheap & rough to refined & functional")
    rungs = [
        ("Sketches", "pen & paper concepts", SKY, 18),
        ("Paper / cardboard", "physical mock-ups", TEAL, 32),
        ("Wireframes / models", "layout & form", BLUE, 46),
        ("3-D printed / functional", "looks & works", ORANGE, 60),
        ("Pilot / production-ready", "near-final product", CORAL, 74),
    ]
    for nm, desc, col, y in rungs:
        w = 30 + (y - 18) * 0.75
        rbox(ax, 30, y, w, 10, col, text=nm, fs=11)
        ax.text(30 + w/2 + 3, y, desc, ha="left", va="center", fontsize=9,
                color="#42525A", style="italic")
    ax.annotate("", xy=(12, 80), xytext=(12, 12),
                arrowprops=dict(arrowstyle="->", color=INK, lw=2))
    ax.text(9, 46, "increasing fidelity, cost & time →", rotation=90,
            ha="center", va="center", fontsize=9.5, color=NAVY, weight="bold")
    save(fig, "prototype_fidelity.png", FIG)


def rapid_prototyping():
    fig, ax = new_ax(9.6, 6.4)
    title(ax, "Rapid Prototyping Cycle", y=97,
          sub="Fail fast, learn faster — CAD to physical part in hours")
    cx, cy, R = 50, 45, 28
    steps = [("Design\n(CAD)", BLUE, 90), ("Slice /\nProgram", TEAL, 18),
             ("Fabricate\n(print / laser)", ORANGE, 306),
             ("Test with\nusers", CORAL, 234), ("Refine", PLUM, 162)]
    radial_cycle(ax, cx, cy, R, steps, box_w=24, box_h=13, fs=10,
                 arrow_color=NAVY)
    badge(ax, cx, cy, 9, YELLOW, "", tc=NAVY, ec=NAVY, lw=2)
    ax.text(cx, cy, "ITERATE", ha="center", va="center", fontsize=11,
            weight="bold", color=NAVY, zorder=6)
    ax.text(50, 8, "Sample: laser-cut acrylic housing → test-group marketing → refine",
            ha="center", fontsize=9.2, style="italic", color="#5B6B73")
    save(fig, "rapid_prototyping.png", FIG)


# ======================================================================
#  UNIT IV  —  DESIGN THINKING & CUSTOMER CENTRICITY
# ======================================================================
def feedback_loop():
    fig, ax = new_ax(10, 6.0)
    title(ax, "Feedback → Re-Design → Re-Create Loop", y=96,
          sub="Continuous improvement centred on user experience")
    cx, cy, R = 50, 45, 28
    steps = [("Release /\nUse", BLUE, 90), ("Collect\nFeedback", TEAL, 18),
             ("Analyse &\nRe-Design", ORANGE, 306),
             ("Re-Create /\nRebuild", CORAL, 234),
             ("Validate\nwith Users", PLUM, 162)]
    radial_cycle(ax, cx, cy, R, steps, box_w=25, box_h=13, fs=10.5,
                 center_fc=NAVY, center_text="USER\nEXPERIENCE", arrow_color=NAVY)
    ax.text(50, 8, "Address ergonomic challenges · close the gap between "
            "expectation and experience", ha="center", fontsize=9.2,
            style="italic", color="#5B6B73")
    save(fig, "feedback_loop.png", FIG)


def cx_radar():
    labels = ["Usability", "Aesthetics", "Reliability", "Ergonomics",
              "Affordability", "Delight"]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    before = [4, 6, 5, 3, 7, 3]
    after = [8, 8, 9, 8, 7, 8]
    before += before[:1]; after += after[:1]
    fig, ax = plt.subplots(figsize=(8.4, 6.2), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")
    ax.plot(angles, before, color=CORAL, lw=2.4, label="Before re-design")
    ax.fill(angles, before, color=CORAL, alpha=0.15)
    ax.plot(angles, after, color=TEAL, lw=2.4, label="After re-design")
    ax.fill(angles, after, color=TEAL, alpha=0.18)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11, weight="bold", color=NAVY)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=8, color="#8a949a")
    ax.set_ylim(0, 10)
    ax.set_title("Parameters of Product Experience", fontsize=15,
                 weight="bold", color=NAVY, pad=24)
    ax.legend(loc="upper right", bbox_to_anchor=(1.22, 1.12), frameon=False,
              fontsize=10)
    fig.tight_layout()
    save(fig, "cx_radar.png", FIG)


def expectation_alignment():
    fig, ax = new_ax(10.5, 5.2)
    title(ax, "Aligning Customer Expectations with the Product", y=95)
    # two overlapping circles (venn)
    ax.add_patch(Circle((38, 48), 22, facecolor=BLUE, alpha=0.35, ec=BLUE, lw=2))
    ax.add_patch(Circle((62, 48), 22, facecolor=ORANGE, alpha=0.35, ec=ORANGE, lw=2))
    ax.text(28, 48, "Customer\nExpectations", ha="center", va="center",
            fontsize=11, weight="bold", color=NAVY)
    ax.text(72, 48, "Product\nExperience", ha="center", va="center",
            fontsize=11, weight="bold", color=NAVY)
    ax.text(50, 48, "SATIS-\nFACTION", ha="center", va="center", fontsize=11,
            weight="bold", color=CORAL)
    ax.text(50, 14, "Gap too wide → disappointment  ·  aligned → "
            "loyalty & advocacy", ha="center", fontsize=10, style="italic",
            color="#5B6B73")
    save(fig, "expectation_alignment.png", FIG)


# ======================================================================
#  UNIT V  —  FABRICATION LABORATORY
# ======================================================================
def route_map():
    fig, ax = new_ax(11, 6.4)
    title(ax, "Fab-Lab Route Map — From Survey to Service Blueprint", y=97)
    steps = [
        ("1  Conduct surveys", "individual or group observe & interview", BLUE),
        ("2  Identify a problem", "spot a real, felt pain point", TEAL),
        ("3  Frame problem statement", "clear, user-centred, actionable", MOSS),
        ("4  Apply CREATE tool", "Combine, Rearrange, Enhance, Adapt,\nTurn-around, Eliminate", ORANGE),
        ("5  Draw product / system", "sketch after applying triggers", CORAL),
        ("6  Build Customer Journey Map", "before, during & after the scenario", PLUM),
        ("7  Frame 2–3 HMW questions", "How Might We… re-open the problem", BLUE),
        ("8  Design Service Blueprint", "identify touch-points from the CJM", NAVY),
    ]
    y = 88
    dy = 10.2
    for i, (nm, desc, col) in enumerate(steps):
        yy = y - i * dy
        rbox(ax, 26, yy, 40, 8.2, col, text=nm, fs=11, ha="center")
        ax.text(50, yy, desc, ha="left", va="center", fontsize=8.8,
                color="#42525A")
        if i < len(steps) - 1:
            arrow(ax, (26, yy - 4.1), (26, yy - dy + 4.1), color="#9AA5AB",
                  lw=1.8, mut=14)
    save(fig, "route_map.png", FIG)


def create_tool():
    fig, ax = new_ax(9.2, 7.2)
    title(ax, "The CREATE Ideation Tool", y=98,
          sub="Six trigger words to transform an existing product")
    cx, cy, R = 50, 46, 23
    items = [
        ("C", "Combine", "merge parts,\nfeatures or functions", BLUE),
        ("R", "Rearrange", "reorder, reverse\nlayout or sequence", TEAL),
        ("E", "Enhance", "magnify, add\nvalue or strength", MOSS),
        ("A", "Adapt", "borrow ideas from\nother contexts", ORANGE),
        ("T", "Turn-around", "invert, do the\nopposite", CORAL),
        ("E", "Eliminate", "remove, simplify\nor minimise", PLUM),
    ]
    n = len(items)
    for i, (ltr, nm, desc, col) in enumerate(items):
        a = math.radians(90 - i * 360 / n)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        badge(ax, x, y, 6.6, col, ltr, fs=18)
        # label outside, extra horizontal push for the side positions
        stretch = 1.0 + 0.5 * abs(math.cos(a))
        lx = cx + (R + 13 * stretch) * math.cos(a)
        ly = cy + (R + 13) * math.sin(a)
        ax.text(lx, ly + 2, nm, ha="center", va="center", fontsize=11,
                weight="bold", color=col)
        ax.text(lx, ly - 3.5, desc, ha="center", va="center", fontsize=8,
                color="#42525A")
        arrow(ax, (cx + 9.5*math.cos(a), cy + 9.5*math.sin(a)),
              (x - 6.8*math.cos(a), y - 6.8*math.sin(a)), color=col, lw=1.6,
              mut=12)
    ax.add_patch(Circle((cx, cy), 9, facecolor=NAVY, ec="white", lw=2))
    ax.text(cx, cy, "CREATE", ha="center", va="center", fontsize=13,
            weight="bold", color="white")
    save(fig, "create_tool.png", FIG)


def cjm():
    fig, ax = new_ax(12, 6.2)
    title(ax, "Customer Journey Map (CJM)", y=97,
          sub="Mapping the experience — before, during & after")
    phases = ["BEFORE\n(Awareness)", "DURING\n(Engagement)", "DURING\n(Use)",
              "AFTER\n(Support)", "AFTER\n(Loyalty)"]
    xs = np.linspace(28, 90, 5)
    # phase headers
    for i, p in enumerate(phases):
        col = CYCLE[i % len(CYCLE)]
        rbox(ax, xs[i], 82, 14.5, 10, col, text=p, fs=8)
    # rows
    rows = [("Actions", 66, "#42525A"),
            ("Touch-\npoints", 54, "#42525A"),
            ("Emotion", 40, "#42525A"),
            ("Pain points\n→ HMW", 22, CORAL)]
    for nm, y, c in rows:
        ax.text(4, y, nm, ha="left", va="center", fontsize=9, weight="bold",
                color=c)
        ax.plot([18, 97], [y + 6.5, y + 6.5], color=GRID, lw=1)
    # emotion curve
    emo = [55, 66, 30, 48, 70]
    emo_y = [40 + (e - 50) * 0.28 for e in emo]
    ax.plot(xs, emo_y, color=CORAL, lw=2.6, marker="o", ms=9,
            markerfacecolor="white", markeredgecolor=CORAL, zorder=5)
    # sample cells
    actions = ["Sees ad /\nhears review", "Visits store /\nsite", "Uses the\nproduct",
               "Contacts\nsupport", "Recommends\nto friends"]
    touch = ["Social, word\nof mouth", "Website,\nstaff", "Product,\nmanual",
             "Helpline,\nFAQ", "Community,\nemail"]
    pains = ["Unclear\nvalue", "Choice\noverload", "Hard to\nassemble",
             "Slow\nresponse", "No loyalty\nreward"]
    for i in range(5):
        ax.text(xs[i], 66, actions[i], ha="center", va="center", fontsize=8,
                color="#42525A")
        ax.text(xs[i], 54, touch[i], ha="center", va="center", fontsize=8,
                color="#42525A")
        ax.text(xs[i], 22, pains[i], ha="center", va="center", fontsize=7.8,
                color=CORAL,
                bbox=dict(boxstyle="round", fc="#FBEAE4", ec=CORAL, lw=0.8))
    ax.text(50, 10, "Touch-points feed the Service Blueprint · pain points "
            "become How-Might-We questions", ha="center", fontsize=9,
            style="italic", color="#5B6B73")
    save(fig, "cjm.png", FIG)


def hmw():
    fig, ax = new_ax(9.6, 5.6)
    title(ax, "How Might We (HMW) Questions", y=96,
          sub="Turning pain points into springboards for ideation")
    # funnel
    ax.add_patch(Polygon([(20, 78), (80, 78), (62, 40), (38, 40)],
                         closed=True, facecolor=CLOUD, ec=GRID, lw=1.5))
    ax.text(50, 82, "Observed pain point", ha="center", fontsize=10.5,
            weight="bold", color=NAVY)
    ax.text(50, 60, "“Users find the product\nhard to assemble”",
            ha="center", va="center", fontsize=10, style="italic", color=INK)
    arrow(ax, (50, 39), (50, 31), color=NAVY, lw=2.4)
    hmws = [
        "How might we make assembly feel effortless?",
        "How might we guide the user step-by-step?",
        "How might we remove the need to assemble at all?",
    ]
    for i, q in enumerate(hmws):
        rbox(ax, 50, 26 - i * 8.5, 66, 6.6, CYCLE[i], text=q, fs=10)
    ax.text(50, 2, "Frame 2–3 HMW questions — broad enough to inspire, "
            "narrow enough to act", ha="center", fontsize=8.8, style="italic",
            color="#5B6B73")
    save(fig, "hmw.png", FIG)


def service_blueprint():
    fig, ax = new_ax(13, 6.6)
    title(ax, "Service Blueprint", y=98,
          sub="Layering the customer journey with what happens behind the scenes")
    lanes = [
        ("Physical\nEvidence", 82, SKY, ["Store /\napp", "Product\nbox",
         "Setup\nguide", "Support\nportal", "Loyalty\ncard"]),
        ("Customer\nActions", 68, BLUE, ["Discover", "Purchase", "Set up",
         "Get help", "Re-buy"]),
        ("Frontstage\n(visible)", 54, TEAL, ["Ad /\ndemo", "Checkout",
         "Onboard-\ning", "Live\nagent", "Rewards"]),
        ("Backstage\n(hidden)", 40, ORANGE, ["Marketing", "Payment\nsystem",
         "Fulfilment", "Ticketing", "CRM"]),
        ("Support\nProcesses", 26, PLUM, ["Analytics", "Logistics", "QA /\ntest",
         "Knowledge\nbase", "Data\nplatform"]),
    ]
    xs = np.linspace(37, 92, 5)
    # lines of interaction / visibility / internal interaction
    line_ys = {"Line of interaction": 61, "Line of visibility": 47,
               "Line of internal interaction": 33}
    for nm, y, col, cells in lanes:
        rbox(ax, 15, y, 22, 10, col, text=nm, fs=9.5)
        for i, c in enumerate(cells):
            rbox(ax, xs[i], y, 11, 10, "white", ec=col, tc=INK, text=c,
                 fs=8, lw=1.6, weight="normal")
    for nm, y in line_ys.items():
        ax.plot([4, 98], [y, y], color="#9AA5AB", ls="--", lw=1.2)
        ax.text(4, y, nm, ha="left", va="center", fontsize=7.4,
                color="#7C878E", style="italic",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    save(fig, "service_blueprint.png", FIG)


# ======================================================================
if __name__ == "__main__":
    funcs = [cover, course_map,
             kolb_cycle, kolb_styles, memory_process, forgetting_curve, empathy,
             dt_process, double_diamond, divergent_convergent,
             creative_problem_solving,
             product_design_process, prototype_fidelity, rapid_prototyping,
             feedback_loop, cx_radar, expectation_alignment,
             route_map, create_tool, cjm, hmw, service_blueprint]
    for f in funcs:
        f()
    print("\nAll %d figures generated." % len(funcs))
