#!/usr/bin/env python3
"""
Interactive trading journal ingest.

Usage:
    python3 ingest_trading.py

Asks each field one at a time, writes a dated raw entry to
raw/trading/, and appends a line to wiki/master-log.md.

The wiki pages themselves (trading-psychology.md, etc.) are updated
by Claude Code when you run:  see README.md > "Daily flow".
"""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
RAW = ROOT / "raw" / "trading"
LOG = ROOT / "wiki" / "master-log.md"

FIELDS = [
    ("energy", "Pre-market energy (1-5)"),
    ("emotion", "Emotional state (calm/anxious/focused/distracted/confident)"),
    ("gut_read", "Gut read before session"),
    ("override", "Where I overrode my plan and why"),
    ("best", "Best decision of the day"),
    ("worst", "Worst decision of the day"),
    ("loop", "Unfinished emotional loop"),
    ("learned", "What I learned today"),
    ("takeaway", "Biggest takeaway"),
]


def ask(prompt: str) -> str:
    print(f"\n{prompt}")
    return input("> ").strip()


def main() -> None:
    today = date.today().isoformat()
    print(f"Trading journal — {today}")
    print("(Press Enter to skip a field.)")

    answers = {key: ask(label) for key, label in FIELDS}

    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{today}.md"
    lines = [f"# Trading Journal — {today}", ""]
    for key, label in FIELDS:
        lines.append(f"- **{label}:** {answers[key]}")
    out.write_text("\n".join(lines) + "\n")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"- {today} trading — {out.relative_to(ROOT)}\n")

    print(f"\nSaved: {out}")
    print("Next: in Claude Code, run  /update-wiki trading  (see README).")


if __name__ == "__main__":
    main()
