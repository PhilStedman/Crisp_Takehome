from philcsv import wrangler
from philcsv.wrangler import Order
from pathlib import Path
import datetime


def test_wrangle():

    test_cases = [
        {
            "name": "Happy path (Sample CSV)",
            "csv_file_path": "resources/sample.csv",
            "cfg_file_path": "",
            "expected": [
                Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250.50, "kg"),
                Order(1001, datetime.datetime(2017, 12, 12), "P-10002", "Iceberg Lettuce", 500.00, "kg"),
            ],
        },
        {
            "name": "Happy path (Sample CSV with config)",
            "csv_file_path": "resources/sample.csv",
            "cfg_file_path": "resources/config1.ini",
            "expected": [
                Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250, "lbs"),
                Order(1001, datetime.datetime(2017, 12, 12), "P-10002", "Iceberg Lettuce", 500, "lbs"),
            ],
        },
        {
            "name": "Bad CSV",
            "csv_file_path": "resources/erroneous.csv",
            "cfg_file_path": "",
            "expected": [
                Order(1000, datetime.datetime(2020, 6, 27), "P-9001", "Chocolate", 5.25, "kg"),
                Order(1001, datetime.datetime(2019, 12, 12), "P-10002", "Bagel", 15, "kg"),
            ],
        },
    ]

    for test_case in test_cases:
        csv_file = Path(__file__).parent / test_case["csv_file_path"]
        cfg_file = ""
        if test_case["cfg_file_path"]:
            cfg_file = Path(__file__).parent / test_case["cfg_file_path"]

        # Ensure the result matches the expected result
        assert test_case["expected"] == wrangler.wrangle(csv_file, cfg_file), test_case["name"]
