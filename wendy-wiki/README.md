# Wendy's Personal LLM Wiki

A compounding personal knowledge base. You journal each day, Claude
reads the entry and updates living wiki pages that get smarter about you
over time. Tone is direct and blunt — truth, not flattery.

All three domains are live: **Trading**, **Health**, **Growth**, plus a
weekly cross-domain synthesis.

---

## Folder layout

```
wendy-wiki/
  raw/
    trading/   ← one dated markdown file per day (the journal entries)
    health/
    growth/
  wiki/
    trading/   ← living synthesis pages, updated by Claude
    health/
    growth/
    master-log.md
  queries/     ← saved answers to questions you ask
    synthesis-weekly.md
  ingest_trading.py
  ingest_health.py
  ingest_growth.py
```

---

## Daily flow

### 1. Add today's entries
From the `wendy-wiki/` folder, run any of:

```
python3 ingest_trading.py
python3 ingest_health.py
python3 ingest_growth.py
```

Each one asks the fields one at a time. Press Enter to skip a field.
Each writes `raw/<domain>/YYYY-MM-DD.md` and appends to `master-log.md`.

### 2. Update the wiki
Open Claude Code in this folder and say one of:

> Update the trading wiki from today's entry.
> Update the health wiki from today's entry.
> Update the growth wiki from today's entry.

Claude will:
1. Read the newest file in `raw/<domain>/`
2. Update each page in `wiki/<domain>/`
3. Refresh the "Current understanding", "Confidence", and
   "Last updated" sections at the top of each page
4. Append dated evidence below — never delete prior content

### 3. Weekly cross-domain synthesis
Once a week, in Claude Code:

> Run the weekly cross-domain synthesis.

Claude reads the last 7 days across all three domains and the current
wiki state, then appends a new dated section to
`wiki/synthesis-weekly.md` naming the concrete cause-and-effect chains
that connect trading, health, and growth.

### 3. Ask questions any time
In Claude Code, ask things like:

- "What patterns keep showing up on my worst trading days?"
- "What emotional state precedes my best decisions?"
- "How has my override behavior changed this month?"
- "What is the single biggest lever in my trading right now?"

Claude answers by reading the **wiki pages**, not re-reading every raw
entry. Save answers worth keeping into `queries/` with a dated filename.

---

## Tone rules for the wiki

- Direct and blunt. Name patterns plainly.
- No hedging, no flattery, no generic self-help language.
- If evidence is thin, say "confidence: low" and stop — don't fabricate.
- Quote Wendy's own words when they're sharper than a paraphrase.

---

## Wiki pages

**Trading** — psychology, best-decisions, worst-decisions, patterns, growth
**Health** — energy-patterns, habit-tracker, body-signals, sleep-patterns, wellness-growth
**Growth** — identity, playing-small, showing-up, the-gap, levers, growth-arc
**Cross-domain** — synthesis-weekly
