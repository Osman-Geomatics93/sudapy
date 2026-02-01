#!/usr/bin/env python3
"""Build an offline wheelhouse for SudaPy.

Usage:
    python scripts/build_wheelhouse.py --out wheelhouse/

This downloads SudaPy and all its dependencies (including optional extras)
as wheel files into the specified directory.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a SudaPy offline wheelhouse.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("wheelhouse"),
        help="Output directory for wheels (default: wheelhouse/)",
    )
    parser.add_argument(
        "--extras",
        default="all",
        help='Comma-separated extras to include (default: "all")',
    )
    args = parser.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    project_root = Path(__file__).resolve().parent.parent
    install_spec = f"{project_root}[{args.extras}]"

    print(f"Downloading wheels for {install_spec} into {out_dir} ...")

    # Step 1: Build the project wheel itself
    subprocess.check_call(
        [sys.executable, "-m", "pip", "wheel", str(project_root), "--wheel-dir", str(out_dir), "--no-deps"],
    )

    # Step 2: Download all dependencies
    subprocess.check_call(
        [sys.executable, "-m", "pip", "download", install_spec, "--dest", str(out_dir)],
    )

    print(f"\nWheelhouse ready at: {out_dir.resolve()}")
    print(f"Files: {len(list(out_dir.glob('*.whl')))} wheels")
    print(f"\nTo install offline:\n  pip install --no-index --find-links {out_dir} sudapy[all]")


if __name__ == "__main__":
    main()
