import json
from collections import Counter

with open("eval/llm_predictions.json", "r", encoding="utf-8") as f:
    v1 = json.load(f)

with open("eval/llm_predictions_v2.json", "r", encoding="utf-8") as f:
    v2 = json.load(f)

severity_changed = 0
category_changed = 0
unchanged = 0

for number in v1:
    if number not in v2:
        continue
    if v1[number]["severity"] != v2[number]["severity"]:
        severity_changed += 1
        print(f"#{number}: severity changed {v1[number]['severity']} -> {v2[number]['severity']}")
    if v1[number]["category"] != v2[number]["category"]:
        category_changed += 1
        print(f"#{number}: category changed {v1[number]['category']} -> {v2[number]['category']}")
    if v1[number] == v2[number]:
        unchanged += 1

print(f"\nSeverity changed: {severity_changed}/{len(v1)}")
print(f"Category changed: {category_changed}/{len(v1)}")
print(f"Fully unchanged: {unchanged}/{len(v1)}")

v1_categories = Counter(v["category"] for v in v1.values())
v2_categories = Counter(v["category"] for v in v2.values())
print(f"\nv1 category distribution: {dict(v1_categories)}")
print(f"v2 category distribution: {dict(v2_categories)}")