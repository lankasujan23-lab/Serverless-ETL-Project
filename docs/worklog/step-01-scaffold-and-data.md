# Step 01: Project scaffold and synthetic data

> **Note:** the synthetic generator described here was replaced by the real UCI Online Retail dataset in [Step 02](step-02-real-dataset.md). This page is kept as a record of the work.

## Goal
Create the repository structure and a reproducible source of test data, so every
later step (cleaning, Lambda, Athena) has realistic input to work with.

## What was done
1. Created the folder layout: `src/`, `tests/`, `docs/`, `data/`.
2. Wrote `src/data_generator/generate_data.py`, a standard-library-only generator
   of fake retail orders with columns:
   `order_id, customer_id, order_ts, product_category, quantity, unit_price, country, payment_type`.
3. Added controlled **data-quality issues** (a share of rows controlled by `--bad-rate`):
   - `duplicate`: a repeated order row (same `order_id`)
   - `missing_customer`: empty `customer_id`
   - `negative_quantity`: quantity below zero
   - `bad_timestamp`: malformed `order_ts` value
4. Wrote unit tests in `tests/test_generate_data.py`.
5. Added `.gitignore` (generated CSVs, caches, secrets), `requirements.txt`, and this documentation.

## Why these choices
- **Synthetic data** avoids licensing questions and lets the data size be chosen to stay in the AWS free tier.
- **Deliberate dirty rows** give the Lambda cleaning logic real work, and let the pipeline's quality checks be tested against known counts.
- **Seeded randomness** makes the same command always produce the same file, so results are reproducible.
- **Standard library only** keeps Step 1 dependency-free.

## How to run
```bash
python -m src.data_generator.generate_data --rows 10000 --seed 42 --bad-rate 0.05 --output data/orders_raw.csv
python -m unittest discover -v
```

## Verification (actual output)
```
Wrote 10129 rows to data/orders_raw.csv
Injected issues: {'duplicate': 129, 'missing_customer': 114, 'negative_quantity': 116, 'bad_timestamp': 141}
```
The output CSV has 10,130 lines (a header plus 10,129 rows: 10,000 base rows plus 129 duplicates).

Unit tests: 5 tests, all passing (`Ran 5 tests ... OK`). They check row counts, column order,
seed reproducibility, validity of clean rows, exact counts of each injected issue, and argument validation.

## Suggested commit
```
git add .
git commit -m "Step 1: project scaffold, synthetic order data generator, and tests"
```

## Next
Step 02: AWS account safety (budget alert, IAM user, CLI configuration).
