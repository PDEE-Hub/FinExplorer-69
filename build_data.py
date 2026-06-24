"""
One-off script: aggregate Power BI_8 Months_69.xlsx (raw line-item export)
into a nested JSON tree for the Financial Explorer dashboard, then emit it
as a `const PAT_DATA = {...};` JS literal to be pasted into index.html.

Not shipped with the dashboard — run manually whenever the source Excel
is refreshed with a new month of data.
"""
import json
import openpyxl

SRC = "../Financial Dashboard/Power BI_8 Months_69.xlsx"
OUT = "pat_data.js"

FY_LABELS = {2025: "fy2568", 2026: "fy2569"}
ENTITIES = ["กทท.", "ทกท.", "ทลฉ.", "ทรน.", "ทชส."]

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb["Sheet1"]

# tree[entity][cat1][cat2][cat3][item][fy_label] = [12 period amounts, 0-indexed]
tree = {}
bad_rows = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    port = row[0]
    if port is None:
        continue
    fy, month, period, code, c1, c2, c3, item, amt = row[1:10]
    if fy not in FY_LABELS:
        continue
    try:
        amt = float(amt) if amt is not None else 0.0
    except (TypeError, ValueError):
        bad_rows += 1
        amt = 0.0

    fy_label = FY_LABELS[fy]
    node = tree.setdefault(port, {}).setdefault(c1, {}).setdefault(c2, {}).setdefault(c3, {}).setdefault(item, {})
    periods = node.setdefault(fy_label, [0.0] * 12)
    periods[period - 1] += amt

print(f"bad amount cells coerced to 0: {bad_rows}")

# ---- sanity check: order-of-magnitude totals per entity per fy ----
print("\nSanity check — net (รายได้ - ค่าใช้จ่าย) by entity, FY2569 periods 1-8 (MB):")
for entity in ENTITIES:
    cats = tree.get(entity, {})
    net = 0.0
    for cat1, c2map in cats.items():
        sign = 1 if cat1 == "รายได้" else -1
        for c2, c3map in c2map.items():
            for c3, itemmap in c3map.items():
                for item, fymap in itemmap.items():
                    periods = fymap.get("fy2569", [0.0] * 8)
                    net += sign * sum(periods[:8])
    print(f"  {entity}: {net/1e6:,.1f} MB")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("const PAT_DATA = ")
    json.dump({"entities": ENTITIES, "tree": tree}, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")

print(f"\nWrote {OUT}")
