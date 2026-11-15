from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from agents import build_runner
from report import render_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a technical review document from a requirement using a multi-agent workflow.")
    parser.add_argument("--input", "-i", required=True, help="Path to a text file containing the requirement.")
    parser.add_argument("--out", "-o", default="outputs/review.md", help="Markdown output path.")
    parser.add_argument("--json", default="outputs/result.json", help="JSON output path.")
    parser.add_argument("--mock", action="store_true", help="Use deterministic local mock agents instead of OpenAI.")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    requirement = Path(args.input).read_text(encoding="utf-8")
    runner = build_runner(mock=args.mock)
    document = runner.run(requirement)
    markdown = render_markdown(document)

    out_path = Path(args.out)
    json_path = Path(args.json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(document.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote markdown: {out_path}")
    print(f"Wrote json: {json_path}")


if __name__ == "__main__":
    main()
