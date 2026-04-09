#!/usr/bin/env python3
"""
Voice journal ingest — speak your daily entries.
Cross-platform (Mac / Windows / Linux).

Usage:
    python3 ingest_voice.py trading
    python3 ingest_voice.py health
    python3 ingest_voice.py growth

Requirements (one-time setup):
    pip install -r requirements.txt
    export OPENAI_API_KEY=sk-...          # Mac/Linux
    setx     OPENAI_API_KEY sk-...         # Windows

For each field:
    [Enter]      start recording
    [Enter]      stop recording (then auto-transcribes with Whisper)
    y            keep the transcription
    r            re-record
    e            edit the transcription by typing
    s            skip this field
    t            type this field instead (no recording)
"""
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

try:
    import numpy as np
    import sounddevice as sd
    import soundfile as sf
except ImportError as e:
    sys.exit(
        "Missing audio package. From the wendy-wiki folder run:\n"
        "    pip install -r requirements.txt\n"
        f"(error: {e})"
    )

try:
    from openai import OpenAI
except ImportError:
    sys.exit(
        "Missing openai package. From the wendy-wiki folder run:\n"
        "    pip install -r requirements.txt"
    )

ROOT = Path(__file__).parent
SAMPLE_RATE = 16000  # Whisper handles 16kHz mono cleanly

DOMAINS = {
    "trading": [
        ("energy", "Pre-market energy (1-5)"),
        ("emotion", "Emotional state (calm/anxious/focused/distracted/confident)"),
        ("gut_read", "Gut read before session"),
        ("override", "Where I overrode my plan and why"),
        ("best", "Best decision of the day"),
        ("worst", "Worst decision of the day"),
        ("loop", "Unfinished emotional loop"),
        ("learned", "What I learned today"),
        ("takeaway", "Biggest takeaway"),
    ],
    "health": [
        ("sleep", "Sleep quality (1-5)"),
        ("energy", "Physical energy (1-5)"),
        ("ignored_signals", "Body signals I haven't been listening to"),
        ("habit", "Habit or pattern that showed up today"),
        ("low_trigger", "What triggered a low-energy state"),
        ("energy_source", "What brought me energy today"),
        ("micro", "Micro-commitment to my body for tomorrow"),
        ("learned", "What I learned today"),
        ("takeaway", "Biggest takeaway"),
    ],
    "growth": [
        ("belief", "Limiting or empowering belief that showed up"),
        ("shrunk", "Where I shrunk or played small"),
        ("showed_up", "Where I showed up fully"),
        ("gap", "The gap between who I am and who I need to become"),
        ("lever", "Biggest lever I'm not pulling"),
        ("avoiding", "What I'm avoiding"),
        ("future_self", "What my future self would say about today"),
        ("learned", "What I learned today"),
        ("takeaway", "Biggest takeaway"),
    ],
}


def record_until_enter() -> "np.ndarray":
    """Record mono audio until the user presses Enter."""
    frames: list = []

    def callback(indata, _frames, _time, _status):
        frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback
    )
    stream.start()
    try:
        input()  # blocks until Enter
    finally:
        stream.stop()
        stream.close()

    if not frames:
        return np.zeros((0, 1), dtype="float32")
    return np.concatenate(frames, axis=0)


def transcribe(audio, client: OpenAI) -> str:
    if audio.size == 0:
        return ""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, audio, SAMPLE_RATE)
        tmp_path = tmp.name
    try:
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(model="whisper-1", file=f)
        return result.text.strip()
    finally:
        os.unlink(tmp_path)


def capture_field(label: str, client: OpenAI) -> str:
    while True:
        print(f"\n{label}")
        print("  [Enter] record  |  s skip  |  t type instead")
        cmd = input("> ").strip().lower()
        if cmd == "s":
            return ""
        if cmd == "t":
            return input("  type: ").strip()

        print("  Recording... press Enter to stop.")
        audio = record_until_enter()
        print("  Transcribing...")
        try:
            text = transcribe(audio, client)
        except Exception as e:
            print(f"  Whisper error: {e}")
            print("  Falling back to typed input.")
            return input("  type: ").strip()

        print(f'  Got: "{text}"')
        print("  [y] keep  |  r re-record  |  e edit  |  s skip")
        choice = input("> ").strip().lower()
        if choice in ("", "y"):
            return text
        if choice == "s":
            return ""
        if choice == "e":
            return input("  edit: ").strip()
        # any other key => loop and re-record


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in DOMAINS:
        sys.exit(f"Usage: python3 {Path(sys.argv[0]).name} {{trading|health|growth}}")

    domain = sys.argv[1]
    fields = DOMAINS[domain]

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit(
            "Missing OPENAI_API_KEY.\n"
            "  Mac/Linux: export OPENAI_API_KEY=sk-...\n"
            "  Windows:   setx OPENAI_API_KEY sk-..."
        )

    client = OpenAI()
    today = date.today().isoformat()
    print(f"Voice journal — {domain} — {today}")
    print("Speak naturally. Whisper transcribes each field after you press Enter to stop.\n")

    answers = {key: capture_field(label, client) for key, label in fields}

    raw_dir = ROOT / "raw" / domain
    raw_dir.mkdir(parents=True, exist_ok=True)
    out = raw_dir / f"{today}.md"
    lines = [f"# {domain.title()} Journal — {today}", ""]
    for key, label in fields:
        lines.append(f"- **{label}:** {answers[key]}")
    out.write_text("\n".join(lines) + "\n")

    log = ROOT / "wiki" / "master-log.md"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as f:
        f.write(f"- {today} {domain} (voice) — {out.relative_to(ROOT)}\n")

    print(f"\nSaved: {out}")
    print(f"Next: in Claude Code, say  Update the {domain} wiki from today's entry.")


if __name__ == "__main__":
    main()
