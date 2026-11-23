"""Render the LaTeX comments in math-model.md as portable Markdown images."""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT.parent / "build" / "matplotlib"))

import matplotlib
matplotlib.use("Agg")
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image


def main():
    source = (ROOT / "math-model.md").read_text(encoding="utf-8")
    formulas = re.findall(r"<!-- formula: ([a-z][a-z0-9-]*)\n(.*?)\n-->", source, re.S)
    if not formulas:
        raise ValueError("No formula sources found in math-model.md")
    if len({name for name, _ in formulas}) != len(formulas):
        raise ValueError("Formula names must be unique")

    output = ROOT / "formulas"
    output.mkdir(exist_ok=True)
    matplotlib.rcParams.update({
        "mathtext.fontset": "dejavusans",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    })
    for name, expression in formulas:
        math_to_image(
            "$" + " ".join(expression.splitlines()) + "$",
            output / (name + ".png"),
            prop=FontProperties(size=16),
            dpi=96,
            format="png",
            color="#19334c",
        )
    print(f"Rendered {len(formulas)} formulas.")


if __name__ == "__main__":
    main()
