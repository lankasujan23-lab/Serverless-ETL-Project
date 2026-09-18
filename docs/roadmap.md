# Roadmap

Each step is built, tested, documented in `docs/worklog/`, and committed separately.

| Step | Goal | Status |
|---|---|---|
| 01 | Project scaffold and a synthetic data generator | Done (superseded by Step 02) |
| 02 | Use the real UCI Online Retail dataset: download script, data-quality profiler, unit tests | Done: run on the real data (541,909 rows profiled) |
| 03 | AWS account safety: budget alert, dedicated IAM user, AWS CLI setup | Planned |
| 04 | Create S3 raw and curated buckets; upload the raw CSV | Planned |
| 05 | Write the cleaning and transformation logic as pure Python functions with unit tests (runs locally) | Planned |
| 06 | Package and deploy the Lambda function; add the S3 event trigger | Planned |
| 07 | Create the Athena database and external table; write analytical SQL queries | Planned |
| 08 | Add CloudWatch logging, SNS failure alerts, and raw-vs-curated row-count checks | Planned |
| 09 | Final documentation: architecture diagram, results, lessons learned, cost notes | Planned |

## Cost guardrails

- The full dataset is a few tens of MB as CSV, which fits comfortably in the free tier.
- Create an AWS Budget alert before creating any resource.
- Delete or empty buckets and functions when finished.
