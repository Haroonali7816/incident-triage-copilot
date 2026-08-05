# Labeling Guide

Use these definitions consistently while filling in `human_severity` and
`human_category` in `labeling_sheet.csv` — these are the **exact same
definitions given to the LLM classifier**. The evaluation only means
something if both are judged against the same criteria.

## Severity (pick exactly one)

- `critical` — system-breaking, no workaround, affects many users.
- `high` — major functionality broken, workaround may exist.
- `medium` — minor bug or missing feature, limited impact.
- `low` — cosmetic, typo, or trivial improvement.

## Category (pick exactly one)

- `bug`
- `feature_request`
- `question`
- `documentation`
- `other`

## Rules for fair labeling

- Judge only from the `title` and `body` columns — that's the same
  information the LLM had. Don't open the actual GitHub issue page or read
  comments unless you genuinely can't decide from the text alone — and if
  you do, note it in the `notes` column, since that's a sign the issue
  itself was ambiguous, which is worth writing up.
- Don't look at `llm_predictions.json` while labeling. That file is
  intentionally kept separate until scoring — seeing the LLM's answer first
  will bias your judgment toward agreeing with it.
- If an issue is genuinely ambiguous between two labels, pick your honest
  best judgment and note the ambiguity — don't leave it blank.
