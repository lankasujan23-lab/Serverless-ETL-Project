"""Download the UCI "Online Retail" dataset and save it as a raw CSV.

Dataset: Chen, D. (2015). Online Retail. UCI Machine Learning Repository.
https://doi.org/10.24432/C5BW33  (licence: CC BY 4.0, attribution required)
~541,909 real transactions from a UK online gift retailer, 2010-12-01 to 2011-12-09.

Usage:
    # Option A: fetch directly from the UCI repository (needs internet + ucimlrepo)
    python -m src.ingest.download_dataset --output data/online_retail_raw.csv

    # Option B: convert an .xlsx you downloaded manually from
    # https://archive.ics.uci.edu/dataset/352/online-retail
    python -m src.ingest.download_dataset --from-xlsx "Online Retail.xlsx" --output data/online_retail_raw.csv
"""
import argparse
import sys
from pathlib import Path

UCI_DATASET_ID = 352
EXPECTED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]


def missing_columns(columns) -> list:
    """Return the expected columns that are absent from `columns`."""
    present = set(columns)
    return [c for c in EXPECTED_COLUMNS if c not in present]


def _fetch_from_uci():
    from ucimlrepo import fetch_ucirepo  # imported lazily so tests need no extra packages

    return fetch_ucirepo(id=UCI_DATASET_ID).data.original


def _read_xlsx(path: str):
    import pandas as pd

    return pd.read_excel(path)


def main() -> int:
    p = argparse.ArgumentParser(description="Download the UCI Online Retail dataset as CSV.")
    p.add_argument("--from-xlsx", help="path to a manually downloaded 'Online Retail.xlsx'")
    p.add_argument("--output", default="data/online_retail_raw.csv", help="output CSV path")
    args = p.parse_args()

    df = _read_xlsx(args.from_xlsx) if args.from_xlsx else _fetch_from_uci()

    missing = missing_columns(df.columns)
    if missing:
        print(f"ERROR: dataset is missing expected columns: {missing}", file=sys.stderr)
        return 1

    df = df[EXPECTED_COLUMNS].copy()
    df["CustomerID"] = df["CustomerID"].astype("Int64")  # avoid 17850.0 style ids

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} rows and {len(df.columns)} columns to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
