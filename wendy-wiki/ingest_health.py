#!/usr/bin/env python3
"""Interactive health & wellness journal ingest."""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
RAW = ROOT / "raw" / "health"
LOG = ROOT / "wiki" / "master-log.md"

FIELDS = [
    ("sleep", "Sleep quality (1-5)"),
    ("energy", "Physical energy (1-5)"),
    ("ignored_signals", "Body signals I haven't been listening to"),
    ("habit", "Habit or pattern that showed up today"),
    ("low_trigger", "What triggered a low-energy state"),
    ("energy_source", "What brought me energy today"),
    ("micro", "Micro-commitment to my body for tomorrow"),
    ("learned", "What I learned today"),
    ("takeaway", "Biggest takeaway"),
]


def ask(prompt: str) -> str:
    print(f"\n{prompt}")
    return input("> ").strip()


def main() -> None:
    today = date.today().isoformat()
    print(f"Health journal — {today}")
    print("(Press Enter to skip a field.)")

    answers = {key: ask(label) for key, label in FIELDS}

    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{today}.md"
    lines = [f"# Health Journal — {today}", ""]
    for key, label in FIELDS:
        lines.append(f"- **{label}:** {answers[key]}")
    out.write_text("\n".join(lines) + "\n")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"- {today} health — {out.relative_to(ROOT)}\n")

    print(f"\nSaved: {out}")
    print("Next: in Claude Code, say  Update the health wiki from today's entry.")


if __name__ == "__main__":
    main()
