"""Draw the same recovery figure for the report and presentation."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "report" / "final" / "figures"


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    font_folder = Path.home() / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts"
    for name in ("Poppins-Regular.ttf", "Poppins-Bold.ttf"):
        path = font_folder / name
        if path.exists():
            font_manager.fontManager.addfont(str(path))
    font_manager.findfont("Poppins", fallback_to_default=False)
    plt.rcParams.update({"font.family": "Poppins", "pdf.fonttype": 42})
    fig = plt.figure(figsize=(7.2, 1.6), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 7.2), ylim=(0, 1.6))
    ax.axis("off")
    ink, accent, border = "#111111", "#FF6B00", "#A8B0B6"
    lefts = (0.03, 1.89, 3.75, 5.61)
    width, bottom, height = 1.56, 0.55, 0.67
    labels = ("Harvest\nbroth", "Cell\nremoval", "Concentrate\nand diafilter", "Liquid enzyme\npreparation")
    for left, label in zip(lefts, labels):
        ax.add_patch(Rectangle((left, bottom), width, height, facecolor="white", edgecolor=border, linewidth=0.9))
        ax.text(left + width / 2, bottom + height / 2, label, ha="center", va="center",
                fontsize=12.6, fontweight="bold", color=ink, linespacing=1.25)
    for left in lefts[:-1]:
        ax.add_patch(FancyArrowPatch((left + width + 0.035, bottom + height / 2),
                                    (left + 1.86 - 0.035, bottom + height / 2),
                                    arrowstyle="-|>", mutation_scale=10, linewidth=1.6, color=accent))
    for left, label in ((lefts[1], "Cells and debris"), (lefts[2], "Salts and methanol")):
        center = left + width / 2
        ax.add_patch(FancyArrowPatch((center, bottom - 0.025), (center, 0.27),
                                    arrowstyle="-|>", mutation_scale=8, linewidth=0.9, color="#606970"))
        ax.text(center, 0.12, label, ha="center", va="center", fontsize=9.3, color="#465059")
    membrane_center = lefts[2] + width / 2
    ax.text(membrane_center, 1.49, "Wash buffer", ha="center", va="center", fontsize=9.3, color="#465059")
    ax.add_patch(FancyArrowPatch((membrane_center, 1.39), (membrane_center, 1.23),
                                arrowstyle="-|>", mutation_scale=7, linewidth=0.9, color="#606970"))
    for extension in ("pdf", "png"):
        output = FIGURES / f"recovery_process.{extension}"
        fig.savefig(output, dpi=320, facecolor="white", bbox_inches=None, pad_inches=0)
        print(output)
    plt.close(fig)


if __name__ == "__main__":
    main()
