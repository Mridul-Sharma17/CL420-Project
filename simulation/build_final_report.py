"""Compile the final TeX source and export identical Group 21 report PDFs."""

from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "report" / "final"
OUTPUT = ROOT / "output" / "pdf" / "final"
REGISTRATIONS = ("23B0353", "23B0345", "23B0358")


def main() -> None:
    compiler = shutil.which("xelatex")
    if compiler is None:
        raise SystemExit("Install XeLaTeX and Times New Roman before compiling this report.")
    with tempfile.TemporaryDirectory(prefix="cl420-final-report-") as build:
        for _ in range(2):
            run = subprocess.run(
                [compiler, "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={build}", "CL420_final_report.tex"],
                cwd=SOURCE, capture_output=True, encoding="utf-8", errors="replace",
            )
            if run.returncode:
                raise SystemExit("\n".join(run.stdout.splitlines()[-60:]) + "\n" + run.stderr)
        log = (Path(build) / "CL420_final_report.log").read_text(encoding="utf-8", errors="replace")
        if re.search(r"^Overfull|undefined references|Citation .* undefined|Missing character", log, flags=re.MULTILINE):
            raise SystemExit("Fix layout, citation or font warnings before exporting the report.")
        pdf = Path(build) / "CL420_final_report.pdf"
        pages = len(PdfReader(pdf).pages)
        if pages > 12:
            raise SystemExit(f"Report has {pages} pages; the course limit is 12 including the cover.")
        OUTPUT.mkdir(parents=True, exist_ok=True)
        for registration in REGISTRATIONS:
            target = OUTPUT / f"Grp21_{registration}_Course_Project_Report.pdf"
            shutil.copyfile(pdf, target)
            print(target)
        print(f"Compiled {pages} pages. All three submission copies contain the same report.")


if __name__ == "__main__":
    main()
