#!/usr/bin/env python3
"""Interactive personal & professional growth journal ingest."""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
RAW = ROOT / "raw" / "growth"
LOG = ROOT / "wiki" / "master-log.md"

FIELDS = [
    ("belief", "Limiting or empowering belief that showed up"),
    ("shrunk", "Where I shrunk or played small"),
    ("showed_up", "Where I showed up fully"),
    ("gap", "The gap between who I am and who I need to become"),
    ("lever", "Biggest lever I'm not pulling"),
    ("avoiding", "What I'm avoiding"),
    ("future_self", "What my future self would say about today"),
    ("learned", "What I learned today"),
    ("takeaway", "Biggest takeaway"),
]


def ask(prompt: str) -> str:
    print(f"\n{prompt}")
    return input("> ").strip()


def main() -> None:
    today = date.today().isoformat()
    print(f"Growth journal — {today}")
    print("(Press Enter to skip a field.)")

    answers = {key: ask(label) for key, label in FIELDS}

    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{today}.md"
    lines = [f"# Growth Journal — {today}", ""]
    for key, label in FIELDS:
        lines.append(f"- **{label}:** {answers[key]}")
    out.write_text("\n".join(lines) + "\n")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"- {today} growth — {out.relative_to(ROOT)}\n")

    print(f"\nSaved: {out}")
    print("Next: in Claude Code, say  Update the growth wiki from today's entry.")


if __name__ == "__main__":
    main()
