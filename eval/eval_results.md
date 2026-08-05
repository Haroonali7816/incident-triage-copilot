# Evaluation Results

## Methodology

40 incidents were randomly sampled (fixed seed, `random.seed(42)` in
`generate_eval_sample.py`) from the 300 classified incidents. Labels were
assigned **blind** — the labeler filled in `human_severity`/`human_category`
in `labeling_sheet.csv` without seeing the LLM's predictions (kept separate
in `llm_predictions.json`), to avoid anchoring judgment toward agreeing with
the model. Both labeler and model used the identical severity/category
definitions (see `LABELING_GUIDE.md` and the `Field` descriptions in
`classifier.py`).

## Run 1 (baseline prompt)

| Metric | Accuracy | Cohen's kappa |
|---|---|---|
| Severity | 40.0% | 0.068 |
| Category | 50.0% | 0.378 |

Kappa interpretation (Landis & Koch): severity agreement was essentially at
chance level; category agreement was "fair."

### Diagnosis

Reviewing all disagreements by hand surfaced two distinct, explainable
failure patterns rather than random noise:

**1. Severity: the model over-rated roughly 2:1.** Of 24 severity
disagreements, 16 were the LLM rating *higher* than the human label, only 8
rating lower. Several of the worst cases (e.g. issues titled "Performance
issue" with no real content beyond the title) were rated `low` by the human
and `high` by the model — the model appears to have been reacting to
alarming-sounding titles rather than weighing how little concrete evidence
the body actually contained.

**2. Category: the model under-used `other` relative to the human
labeler.** Across the 40 issues, the human applied `other` to at least 11
(27.5%, counting only cases visible in the disagreement list — the true
total may be slightly higher), while the LLM applied it to only 4 (10%)
total. Rather than being a *literal* zero-usage problem, this was an
under-calibration: the model defaulted low-signal, vague, or spam-like
issues to `bug` or `question` far more often than a human judged
appropriate.

## Intervention

Based on this diagnosis, `classifier.py`'s `ClassificationResult` field
descriptions were revised:
- Added an explicit instruction to weigh the issue body's actual concrete
  content over the title's tone, and to default toward lower severity when
  the body is thin or vague.
- Added an explicit definition of `other` ("spam, duplicate reports, vague
  or low-signal issues with no real content, non-technical content, or
  automated/bot-generated reports"), rather than leaving it as an
  undifferentiated fifth option.

The same 40 incidents were then **re-classified only** (human labels were
not touched) using `reclassify_eval_sample.py`, and scored separately
against the same human labels.

## Run 2 (revised prompt)

| Metric | Accuracy | Cohen's kappa |
|---|---|---|
| Severity | 40.0% | 0.026 |
| Category | 50.0% | 0.378 |

### What actually changed between runs

Diffing the two prediction sets directly (`compare_v1_v2.py`) showed:
- **5/40 severity predictions changed**, all `high → medium` — the revised
  prompt pulled the model off its most extreme over-ratings (e.g. the
  "Performance issue" spam reports), but only by one level, not all the way
  down to the human's `low` rating. Only one of these five (`#12382`)
  actually flipped a mismatch into a match; the rest moved from "wrong by
  two levels" to "wrong by one level," which doesn't change accuracy.
- **2/40 category predictions changed**, and the `other` prediction count
  was identical before and after (4/40 both times) — the revised
  definition did not measurably change how often the model reached for
  `other`.
- Kappa for severity slightly *decreased* (0.068 → 0.026) despite identical
  accuracy. This is a real statistical effect, not noise: kappa corrects for
  label-frequency-driven chance agreement, and shifting several predictions
  from `high` toward `medium` changed the marginal distribution enough to
  slightly raise the expected-by-chance term.

## Honest conclusion

The targeted prompt revision produced a **partial, measurable, but
insufficient correction**. It succeeded at reducing the model's most
extreme over-ratings (moving several `high` misjudgments toward `medium`),
confirming the diagnosis was directionally correct, but a single rewritten
field description was not strong enough to fully close the gap on either
metric. Category calibration for `other` did not move at all.


