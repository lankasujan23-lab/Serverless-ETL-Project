# Step 02: Switch to the real UCI Online Retail dataset

## Goal
Replace the synthetic data with a real public dataset, so the pipeline is tested
against genuine data-quality problems and the project is more credible.

## What was done
1. Chose the **UCI Online Retail** dataset (541,909 transactions, 8 columns,
   1 Dec 2010 to 9 Dec 2011, CC BY 4.0).
2. Added `src/ingest/download_dataset.py`. It fetches the dataset with the
   `ucimlrepo` package (or converts a manually downloaded `Online Retail.xlsx`),
   checks that all 8 expected columns are present, and saves `data/online_retail_raw.csv`.
3. Added `src/profiling/profile_quality.py`, which counts: missing `CustomerID`,
   missing `Description`, cancellation invoices (`InvoiceNo` starting with `C`),
   non-positive quantity, non-positive unit price, exact duplicate rows, and unparseable numbers.
4. Added unit tests (`tests/test_profile_quality.py`) using a small fixture CSV
   with one example of each problem. The tests pass.
5. Removed the synthetic generator and its tests (superseded). They remain in git history from Step 01.
6. Updated `requirements.txt`, `.gitignore`, the README, and the roadmap (later steps renumbered).

## Why
- Real data is messier and less predictable than synthetic data, and it can be shown honestly in interviews.
- Profiling the raw data first gives known "before" numbers to compare against after the Lambda cleaning step.
- The dataset licence (CC BY 4.0) allows reuse with attribution, which is included in the README.

## How to run
```bash
pip install -r requirements.txt
python -m src.ingest.download_dataset --output data/online_retail_raw.csv
# If the automatic download fails, download "Online Retail.xlsx" from
# https://archive.ics.uci.edu/dataset/352/online-retail and run:
# python -m src.ingest.download_dataset --from-xlsx "Online Retail.xlsx" --output data/online_retail_raw.csv
python -m src.profiling.profile_quality --input data/online_retail_raw.csv
python -m unittest discover -v
```

## Verification
- Unit tests: 2 tests, all passing (`Ran 2 tests ... OK`).
- The download script and the profiler were run on the full real dataset; results are below.

## Results on the real dataset
Download output: `Wrote 541909 rows and 8 columns to data/online_retail_raw.csv`

Profiler output:
```json
{
  "total_rows": 541909,
  "missing_customer_id": 135080,
  "missing_description": 1454,
  "cancellation_invoices": 9288,
  "non_positive_quantity": 10624,
  "non_positive_unit_price": 2517,
  "exact_duplicate_rows": 5268,
  "unparseable_numbers": 0
}
```

| Issue | Rows | Share of total |
|---|---|---|
| Missing CustomerID | 135,080 | 24.9% |
| Non-positive quantity | 10,624 | 2.0% |
| Cancellation invoices (InvoiceNo starts with C) | 9,288 | 1.7% |
| Exact duplicate rows | 5,268 | 1.0% |
| Non-positive unit price | 2,517 | 0.5% |
| Missing Description | 1,454 | 0.3% |
| Unparseable numbers | 0 | 0% |

Row count matches the 541,909 instances documented by UCI. These figures are the "before" baseline for the cleaning step.

### Planned handling (to be confirmed in Step 05)
These are design intentions, not yet implemented:
- Duplicates: drop exact duplicate rows.
- Missing CustomerID: keep the rows but flag them, because they still carry valid sales data; exclude them only from customer-level analysis.
- Cancellations and non-positive quantity: separate them into their own output so revenue figures are not distorted.
- Non-positive unit price: treat as invalid and quarantine.

## Suggested commit
```
git rm -r src/data_generator tests/test_generate_data.py
git add .
git commit -m "Step 2: use real UCI Online Retail dataset; add download script and data-quality profiler"
```

## Next
Step 03: AWS account safety (budget alert, IAM user, CLI configuration).
