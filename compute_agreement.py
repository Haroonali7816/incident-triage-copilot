import csv
import json
import sys
from collections import Counter

LABELLING_SHEET_PATH = "eval/labelling_sheet.csv"
LLM_PREDICTIONS_PATH = "eval/llm_predictions.json"
RESULTS_PATH = "eval/eval_results.md"


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> float:
    """
    Chance-corrected agreement between two labelers.

    Plain accuracy can look artificially high when one label dominates
    (e.g. most issues genuinely being "low" severity) -- a classifier that
    always guesses the majority label would score well on raw accuracy while
    having learned nothing. Kappa discounts the agreement you'd expect from
    each label's frequency alone, so what's left reflects real agreement.

    Rough interpretation (Landis & Koch scale):
      < 0.20 slight, 0.21-0.40 fair, 0.41-0.60 moderate,
      0.61-0.80 substantial, 0.81-1.00 almost perfect.
    """
    n = len(labels_a)
    po = sum(a == b for a, b in zip(labels_a, labels_b)) / n

    count_a = Counter(labels_a)
    count_b = Counter(labels_b)
    categories = set(labels_a) | set(labels_b)
    pe = sum((count_a[c] / n) * (count_b[c] / n) for c in categories)

    if pe == 1:
        return 1.0  # avoid division by zero in the (rare) all-agree-by-chance case
    return (po - pe) / (1 - pe)


def compute_agreement(predictions_path: str = LLM_PREDICTIONS_PATH, results_path: str = RESULTS_PATH) -> None:
    with open(predictions_path, "r", encoding="utf-8") as f:
        llm_predictions = json.load(f)

    with open(LABELLING_SHEET_PATH, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    missing = [r["github_number"] for r in rows if not r["human_severity"] or not r["human_category"]]
    if missing:
        print(f"Note: {len(missing)} row(s) still unlabeled: {missing}")
        print("Fill in every row of labelling_sheet.csv for a complete evaluation.\n")

    human_severity, llm_severity = [], []
    human_category, llm_category = [], []
    disagreements = []

    for row in rows:
        number = row["github_number"]
        if number not in llm_predictions:
            continue
        if not row["human_severity"] or not row["human_category"]:
            continue

        pred = llm_predictions[number]
        h_sev, h_cat = row["human_severity"].strip(), row["human_category"].strip()

        human_severity.append(h_sev)
        llm_severity.append(pred["severity"])
        human_category.append(h_cat)
        llm_category.append(pred["category"])

        if h_sev != pred["severity"] or h_cat != pred["category"]:
            disagreements.append(
                {
                    "github_number": number,
                    "title": row["title"],
                    "human_severity": h_sev,
                    "llm_severity": pred["severity"],
                    "human_category": h_cat,
                    "llm_category": pred["category"],
                    "notes": row["notes"],
                }
            )

    n = len(human_severity)
    if n == 0:
        print("No labeled rows found yet -- fill in labelling_sheet.csv first.")
        return

    severity_accuracy = sum(a == b for a, b in zip(human_severity, llm_severity)) / n
    category_accuracy = sum(a == b for a, b in zip(human_category, llm_category)) / n
    severity_kappa = cohen_kappa(human_severity, llm_severity)
    category_kappa = cohen_kappa(human_category, llm_category)

    lines = [
        "# Evaluation Results\n",
        f"Sample size: {n} hand-labeled incidents (random seed 42, see `generate_eval_sample.py`)\n",
        "## Methodology\n",
        "Labels were assigned **blind** — the labeler did not see the LLM's "
        "predictions while labeling (see `LABELING_GUIDE.md`), to avoid biasing "
        "judgment toward agreeing with the model.\n",
        "## Agreement\n",
        f"- Severity exact-match accuracy: {severity_accuracy:.1%}",
        f"- Severity Cohen's kappa: {severity_kappa:.3f}",
        f"- Category exact-match accuracy: {category_accuracy:.1%}",
        f"- Category Cohen's kappa: {category_kappa:.3f}\n",
        "## Disagreements\n",
    ]

    if disagreements:
        for d in disagreements:
            lines.append(
                f"- **#{d['github_number']}** {d['title']}\n"
                f"  - Human: severity=`{d['human_severity']}`, category=`{d['human_category']}`\n"
                f"  - LLM: severity=`{d['llm_severity']}`, category=`{d['llm_category']}`\n"
                f"  - Notes: {d['notes'] or '(none)'}\n"
            )
    else:
        lines.append("No disagreements found.\n")

    with open(results_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Severity: {severity_accuracy:.1%} accuracy, kappa={severity_kappa:.3f}")
    print(f"Category: {category_accuracy:.1%} accuracy, kappa={category_kappa:.3f}")
    print(f"Full results written to {results_path}")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        compute_agreement(predictions_path=sys.argv[1], results_path=sys.argv[2])
    else:
        compute_agreement()