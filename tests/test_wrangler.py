from philcsv import wrangler
from philcsv.wrangler import Order
from pathlib import Path
import datetime


def test_wrangle():

    test_cases = [
        {
            "name": "Happy path (Default CSV)",
            "csv_file_path": "resources/default.csv",
            "cfg_file_path": "",
            "expected": [
                Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250.50, "kg"),
                Order(1001, datetime.datetime(2017, 12, 12), "P-10002", "Iceberg Lettuce", 500.00, "kg"),
            ],
        },
        {
            "name": "Happy path (User defined CSV with all configs)",
            "csv_file_path": "resources/user_defined1.csv",
            "cfg_file_path": "resources/config1.json",
            "expected": [
                Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250.50, "kg"),
                Order(1001, datetime.datetime(2017, 12, 12), "P-10002", "Iceberg Lettuce", 500.00, "kg"),
            ],
        },
        {
            "name": "Happy path (User defined CSV with partial configs)",
            "csv_file_path": "resources/user_defined2.csv",
            "cfg_file_path": "resources/config2.json",
            "expected": [
                Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250.50, "kg"),
                Order(1001, datetime.datetime(2017, 12, 12), "P-10002", "Iceberg Lettuce", 500.00, "kg"),
            ],
        },
        {
            "name": "Happy path (CSV file with rows > CHUNK_SZ)",
            "csv_file_path": "resources/large.csv",
            "cfg_file_path": "",
            "expected": [
                Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250.5, "kg"),
                Order(1001, datetime.datetime(2017, 12, 12), "P-10002", "Spinach", 500.0, "kg"),
                Order(1002, datetime.datetime(2018, 1, 2), "P-10003", "Chocolate", 5250.5, "kg"),
                Order(1003, datetime.datetime(2017, 12, 11), "P-10004", "Nutella", 500.00, "kg"),
                Order(1004, datetime.datetime(2018, 1, 1), "P-10005", "Butter", 5250.50, "kg"),
                Order(1005, datetime.datetime(2017, 12, 12), "P-10006", "Milk", 500.00, "kg"),
                Order(1006, datetime.datetime(2018, 1, 1), "P-10007", "Bread", 5250.50, "kg"),
                Order(1007, datetime.datetime(2017, 12, 12), "P-10008", "Bagel", 500.00, "kg"),
                Order(1008, datetime.datetime(2018, 1, 1), "P-10009", "Apple", 5250.50, "kg"),
                Order(1009, datetime.datetime(2017, 12, 12), "P-10010", "Pear", 500.00, "kg"),
                Order(1010, datetime.datetime(2018, 1, 1), "P-10011", "Banana", 5250.50, "kg"),
                Order(1011, datetime.datetime(2017, 12, 12), "P-10012", "Kiwi", 500.00, "kg"),
                Order(1012, datetime.datetime(2018, 1, 1), "P-10013", "Carrot", 5250.50, "kg"),
                Order(1013, datetime.datetime(2017, 12, 12), "P-10014", "Celery", 500.00, "kg"),
                Order(1014, datetime.datetime(2018, 1, 1), "P-10015", "Broccoli", 5250.50, "kg"),
                Order(1015, datetime.datetime(2017, 12, 12), "P-10016", "Asparagus", 500.00, "kg"),
                Order(1016, datetime.datetime(2018, 1, 1), "P-10017", "Orange", 5250.50, "kg"),
                Order(1017, datetime.datetime(2017, 12, 12), "P-10018", "Grapefruit", 500.0, "kg"),
                Order(1018, datetime.datetime(2018, 1, 1), "P-10019", "Grapes", 5250.50, "kg"),
                Order(1019, datetime.datetime(2017, 12, 12), "P-10020", "Cereal", 500.00, "kg"),
                Order(1020, datetime.datetime(2018, 1, 1), "P-10021", "Mango", 5250.50, "kg"),
                Order(1021, datetime.datetime(2017, 12, 12), "P-10022", "Onions", 500.00, "kg"),
                Order(1022, datetime.datetime(2018, 1, 1), "P-10023", "Salt", 5250.50, "kg"),
                Order(1023, datetime.datetime(2017, 12, 12), "P-10024", "Pepper", 500.00, "kg"),
                Order(1024, datetime.datetime(2018, 1, 1), "P-10025", "Cajun Spice", 5250.50, "kg"),
                Order(1025, datetime.datetime(2017, 12, 12), "P-10026", "Paprika", 500.00, "kg"),
                Order(1026, datetime.datetime(2018, 1, 1), "P-10027", "Honey", 5250.50, "kg"),
                Order(1027, datetime.datetime(2017, 12, 12), "P-10028", "Sugar", 500.00, "kg"),
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
