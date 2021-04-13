from philcsv import csvwrangler
from pathlib import Path
import datetime


def test_samplecsv():
    file = Path(__file__).parent / "resources/sample.csv"
    orders = csvwrangler.wrangle(file)

    expected = [
        csvwrangler.Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250.50, "kg"),
        csvwrangler.Order(
            1001,
            datetime.datetime(2017, 12, 12),
            "P-10002",
            "Iceberg Lettuce",
            500.00,
            "kg",
        ),
    ]

    i = 0
    for order in orders:
        assert order.order_id == expected[i].order_id
        assert order.order_date == expected[i].order_date
        assert order.product_id == expected[i].product_id
        assert order.product_name == expected[i].product_name
        assert order.quantity == expected[i].quantity
        assert order.unit == expected[i].unit
        i += 1


def test_samplecsv_withcfg():
    file = Path(__file__).parent / "resources/sample.csv"
    cfg_file = Path(__file__).parent / "resources/config1.ini"

    orders = csvwrangler.wrangle(file, cfg_file)

    expected = [
        csvwrangler.Order(1000, datetime.datetime(2018, 1, 1), "P-10001", "Arugola", 5250, "lbs"),
        csvwrangler.Order(
            1001,
            datetime.datetime(2017, 12, 12),
            "P-10002",
            "Iceberg Lettuce",
            500,
            "lbs",
        ),
    ]

    i = 0
    for order in orders:
        assert order.order_id == expected[i].order_id
        assert order.order_date == expected[i].order_date
        assert order.product_id == expected[i].product_id
        assert order.product_name == expected[i].product_name
        assert order.quantity == expected[i].quantity
        assert order.unit == expected[i].unit
        i += 1


def test_errorcsv():
    file = Path(__file__).parent / "resources/erroneous.csv"
    orders = csvwrangler.wrangle(file)

    expected = [
        csvwrangler.Order(1000, datetime.datetime(2020, 6, 27), "P-9001", "Chocolate", 5.25, "kg"),
        csvwrangler.Order(1001, datetime.datetime(2019, 12, 12), "P-10002", "Bagel", 15, "kg"),
    ]

    i = 0
    for order in orders:
        assert order.order_id == expected[i].order_id
        assert order.order_date == expected[i].order_date
        assert order.product_id == expected[i].product_id
        assert order.product_name == expected[i].product_name
        assert order.quantity == expected[i].quantity
        assert order.unit == expected[i].unit
        i += 1
