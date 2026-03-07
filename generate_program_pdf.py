#!/usr/bin/env python3
"""
Compile program.tex to PDF using pdflatex.

Reads data/program.json and data/conference.json for validation,
then calls pdflatex on program.tex. If the output PDF is locked,
optionally generates a second copy with a different jobname.

Usage:
    python generate_program_pdf.py
    python generate_program_pdf.py --jobname program_copy
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEX_FILE = BASE_DIR / "program.tex"


def load_json(filename: str):
    path = DATA_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return None


def run_pdflatex(jobname: str | None = None) -> bool:
    """Run pdflatex on program.tex. Returns True on success."""
    if not TEX_FILE.exists():
        print(f"ERROR: {TEX_FILE} not found.")
        return False

    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-output-directory", str(BASE_DIR),
    ]
    if jobname:
        cmd.extend(["-jobname", jobname])
    cmd.append(str(TEX_FILE))

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BASE_DIR))

    # Check for errors
    errors = []
    for line in result.stdout.splitlines():
        if line.startswith("!"):
            errors.append(line)

    if result.returncode != 0 and errors:
        print("FAILED with errors:")
        for e in errors:
            print(f"  {e}")
        return False

    out_name = jobname if jobname else "program"
    pdf_path = BASE_DIR / f"{out_name}.pdf"
    if pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"SUCCESS: {pdf_path} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"WARNING: pdflatex ran but {pdf_path} was not created.")
        if errors:
            for e in errors:
                print(f"  {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Compile program.tex to PDF")
    parser.add_argument(
        "--jobname",
        default=None,
        help="Alternative jobname if the default PDF is locked (e.g. program_copy)",
    )
    args = parser.parse_args()

    # Validate data files exist
    program_data = load_json("program.json")
    conf_data = load_json("conference.json")

    if program_data:
        days = program_data.get("days", [])
        items = sum(len(d.get("items", [])) for d in days)
        print(f"Program data: {len(days)} day(s), {items} schedule item(s)")
    else:
        print("WARNING: data/program.json not found (TeX may use hardcoded data)")

    if conf_data:
        print(f"Conference: {conf_data.get('name', 'N/A')}")
    else:
        print("WARNING: data/conference.json not found")

    # First attempt
    success = run_pdflatex(args.jobname)

    if not success and not args.jobname:
        print("\nFirst attempt failed. Trying with alternative jobname 'program_copy'...")
        success = run_pdflatex("program_copy")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
