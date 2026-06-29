from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.bug_report_generator import generate_bug_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a heuristic bug report draft.")
    parser.add_argument("--transcripts-dir", default="transcripts")
    parser.add_argument("--output", default="bug_report_draft.md")
    args = parser.parse_args()
    output = generate_bug_report(args.transcripts_dir, args.output)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
