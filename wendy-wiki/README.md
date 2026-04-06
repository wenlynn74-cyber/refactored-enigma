# Wendy's Personal LLM Wiki

A compounding personal knowledge base. You journal each day, Claude
reads the entry and updates living wiki pages that get smarter about you
over time. Tone is direct and blunt — truth, not flattery.

Built first for the **Trading** domain. Health and Growth folders are
scaffolded and will be filled in next.

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
  ingest_trading.py
```

---

## Daily flow (Trading)

### 1. Add today's entry
In your terminal, from the `wendy-wiki/` folder:

```
python3 ingest_trading.py
```

It will ask you each field one at a time. Press Enter to skip any field.
It writes `raw/trading/YYYY-MM-DD.md` and appends to `master-log.md`.

### 2. Update the wiki
Open Claude Code in this folder and say:

> Update the trading wiki from today's entry.

Claude will:
1. Read the newest file in `raw/trading/`
2. Update each page in `wiki/trading/`:
   - `trading-psychology.md`
   - `trading-best-decisions.md`
   - `trading-worst-decisions.md`
   - `trading-patterns.md`
   - `trading-growth.md`
3. Refresh the "Current understanding", "Confidence", and
   "Last updated" sections at the top of each page
4. Append dated evidence below — never delete prior content

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

## What's next

Once the trading loop feels right, we add:
- `ingest_health.py` and the 5 health wiki pages
- `ingest_growth.py` and the 6 growth wiki pages
- `synthesis-weekly.md` — cross-domain pattern detection run weekly
