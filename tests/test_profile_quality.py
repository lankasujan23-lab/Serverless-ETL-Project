import csv
import os
import tempfile
import unittest

from src.ingest.download_dataset import EXPECTED_COLUMNS, missing_columns
from src.profiling.profile_quality import profile_csv

HEADER = EXPECTED_COLUMNS
ROWS = [
    ["536365", "85123A", "WHITE HANGING HEART", "6", "2010-12-01 08:26:00", "2.55", "17850", "United Kingdom"],  # clean
    ["536366", "22633", "HAND WARMER", "6", "2010-12-01 08:28:00", "1.85", "", "United Kingdom"],               # missing customer
    ["C536379", "D", "Discount", "-1", "2010-12-01 09:41:00", "27.50", "14527", "United Kingdom"],               # cancellation, negative qty
    ["536370", "22728", "", "3", "2010-12-01 08:45:00", "3.75", "12583", "France"],                              # missing description
    ["536371", "22086", "PAPER CHAIN KIT", "80", "2010-12-01 09:00:00", "0", "13748", "United Kingdom"],         # zero price
    ["536365", "85123A", "WHITE HANGING HEART", "6", "2010-12-01 08:26:00", "2.55", "17850", "United Kingdom"],  # exact duplicate of row 1
]


class ProfileTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(HEADER)
            w.writerows(ROWS)

    def tearDown(self):
        os.remove(self.path)

    def test_counts(self):
        s = profile_csv(self.path)
        self.assertEqual(s["total_rows"], 6)
        self.assertEqual(s["missing_customer_id"], 1)
        self.assertEqual(s["missing_description"], 1)
        self.assertEqual(s["cancellation_invoices"], 1)
        self.assertEqual(s["non_positive_quantity"], 1)
        self.assertEqual(s["non_positive_unit_price"], 1)
        self.assertEqual(s["exact_duplicate_rows"], 1)
        self.assertEqual(s["unparseable_numbers"], 0)

    def test_missing_columns_helper(self):
        self.assertEqual(missing_columns(EXPECTED_COLUMNS), [])
        self.assertEqual(missing_columns(["InvoiceNo"])[0], "StockCode")


if __name__ == "__main__":
    unittest.main()
