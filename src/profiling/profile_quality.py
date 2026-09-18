"""Profile data quality of the raw Online Retail CSV (standard library only).

Counts the problems the Lambda cleaning step (built later) must handle, so the
pipeline's before/after row counts can be checked against known numbers.
"""
import argparse
import csv
import json


def profile_csv(path: str) -> dict:
    stats = {
        "total_rows": 0,
        "missing_customer_id": 0,
        "missing_description": 0,
        "cancellation_invoices": 0,   # InvoiceNo starts with 'C'
        "non_positive_quantity": 0,
        "non_positive_unit_price": 0,
        "exact_duplicate_rows": 0,
        "unparseable_numbers": 0,
    }
    seen = set()

    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            stats["total_rows"] += 1

            if not (row.get("CustomerID") or "").strip():
                stats["missing_customer_id"] += 1
            if not (row.get("Description") or "").strip():
                stats["missing_description"] += 1
            if (row.get("InvoiceNo") or "").upper().startswith("C"):
                stats["cancellation_invoices"] += 1

            try:
                if float(row["Quantity"]) <= 0:
                    stats["non_positive_quantity"] += 1
                if float(row["UnitPrice"]) <= 0:
                    stats["non_positive_unit_price"] += 1
            except (TypeError, ValueError, KeyError):
                stats["unparseable_numbers"] += 1

            key = tuple(row.values())
            if key in seen:
                stats["exact_duplicate_rows"] += 1
            else:
                seen.add(key)

    return stats


def main() -> None:
    p = argparse.ArgumentParser(description="Profile data quality of the raw retail CSV.")
    p.add_argument("--input", default="data/online_retail_raw.csv")
    args = p.parse_args()
    print(json.dumps(profile_csv(args.input), indent=2))


if __name__ == "__main__":
    main()
