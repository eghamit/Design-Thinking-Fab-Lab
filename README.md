# Design Thinking & Fabrication Laboratory

A detailed, illustrated **LaTeX Beamer** presentation covering the complete
five-unit syllabus of the *Design Thinking and Fabrication Laboratory* course.

The deck (`main.tex`, 43 slides, 16:9) walks through every syllabus topic with
custom diagrams — Kolb's learning cycle, the memory model, the 5-stage design
thinking process, the double diamond, prototyping, customer journey maps, the
CREATE tool, How-Might-We questions, service blueprints and more.

All figures are generated programmatically with Python/Matplotlib and saved as
PNGs in the [`figures/`](figures/) folder.

## Contents

| Unit | Topic | Key figures |
|------|-------|-------------|
| I | An Insight to Learning | Kolb cycle & styles, memory model, forgetting curve, empathy |
| II | Basics of Design Thinking | 5-stage process, double diamond, brainstorming, creative problem solving |
| III | Process of Product Design | engineering design process, prototype ladder, rapid prototyping |
| IV | Design Thinking & Customer Centricity | experience radar, expectation alignment, feedback loop |
| V | Fabrication Laboratory | route map, CREATE tool, CJM, HMW, service blueprint |

## Building the slides

Requires a TeX distribution with `beamer`, `tikz`, `newunicodechar` and
`lmodern` (any recent TeX Live).

```bash
pdflatex main.tex      # run twice so the table of contents resolves
pdflatex main.tex
```

The result is `main.pdf`.

## Regenerating the figures

The figures are produced by a self-contained script:

```bash
pip install matplotlib numpy
python3 scripts/generate_figures.py
```

- `scripts/dtstyle.py` — shared colour palette and drawing helpers.
- `scripts/generate_figures.py` — one function per figure; writes to `figures/`.

Edit a figure function and re-run the script to refresh its PNG, then rebuild
the PDF.

## Repository layout

```
main.tex                     # the Beamer presentation
figures/                     # generated PNG figures used in the slides
scripts/generate_figures.py  # regenerates every figure
scripts/dtstyle.py           # palette + drawing primitives
```
