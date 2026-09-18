# Serverless Batch ETL and Analytics on AWS

An event-driven, low-cost data pipeline built with **Python, SQL, and AWS**,
using a **real public dataset**: the UCI Online Retail data (about 540,000
transactions from a UK online gift retailer). A CSV uploaded to Amazon S3
triggers an AWS Lambda function that validates and cleans the data and writes
partitioned Parquet files. The curated data is queried with SQL in Amazon
Athena, with logging and failure alerts through CloudWatch and SNS.

> **Status:** in progress. See the [roadmap](docs/roadmap.md) and the
> [work log](docs/worklog/) for what has been built so far.

## Dataset

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5BW33 (licence: CC BY 4.0). Columns: `InvoiceNo`,
`StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`,
`CustomerID`, `Country`. The data is genuinely messy (missing customer IDs,
cancellations, negative quantities, zero prices, duplicates), which is what the
cleaning step is designed to handle.

## Architecture (target)

```
 online_retail_raw.csv ──► S3 raw bucket ──(ObjectCreated event)──► Lambda (Python + Pandas)
                                                                       │
                              CloudWatch logs + SNS email alert ◄──────┤ validate / clean / dedupe
                                                                       ▼
                                                          S3 curated bucket (partitioned Parquet)
                                                                       │
                                                                       ▼
                                                          Athena external table ──► SQL analytics
```

## Tech stack

| Area | Tools |
|---|---|
| Language | Python 3 (Pandas for transformation) |
| Storage | Amazon S3 (raw and curated buckets), Parquet |
| Compute | AWS Lambda (S3 trigger) |
| Query | Amazon Athena (SQL: joins, CTEs, window functions, aggregations) |
| Monitoring | Amazon CloudWatch, Amazon SNS |
| Security | Least-privilege IAM roles |
| Testing | unittest / pytest |

## Repository layout

```
src/ingest/        download the real dataset as a raw CSV
src/profiling/     data-quality profiling of the raw CSV
tests/             unit tests
docs/              roadmap and per-step work log
data/              local data files (git-ignored)
```

## Quick start

```bash
pip install -r requirements.txt
python -m src.ingest.download_dataset --output data/online_retail_raw.csv
python -m src.profiling.profile_quality --input data/online_retail_raw.csv
python -m unittest discover -v
```

## Documentation

- [Roadmap](docs/roadmap.md)
- [Step 01: Project scaffold and synthetic data (superseded)](docs/worklog/step-01-scaffold-and-data.md)
- [Step 02: Switch to the real UCI dataset](docs/worklog/step-02-real-dataset.md)
