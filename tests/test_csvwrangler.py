from philcsv import csvwrangler
from pathlib import Path
import datetime

def test_samplecsv():
    file = Path(__file__).parent / "testcsvs/sample.csv"
    orders = csvwrangler.wrangle( file )

    expected = [ csvwrangler.Order( 1000, datetime.datetime(2018,1,1), "P-10001", "Arugola", 5250.50, "kg" ),
                 csvwrangler.Order( 1001, datetime.datetime(2017,12,12), "P-10002", "Iceberg Lettuce", 500.00, "kg" ) ]

    i = 0
    for order in orders:
        assert ( order.OrderID == expected[i].OrderID )
        assert ( order.OrderDate == expected[i].OrderDate )
        assert ( order.ProductId == expected[i].ProductId )
        assert ( order.ProductName == expected[i].ProductName )
        assert ( order.Quantity == expected[i].Quantity )
        assert ( order.Unit == expected[i].Unit )
        i += 1

def test_errorcsv():
    file = Path(__file__).parent / "testcsvs/erroneous.csv"
    orders = csvwrangler.wrangle( file )

    expected = [ csvwrangler.Order( 1000, datetime.datetime(2020,6,27), "P-9001", "Chocolate", 5.25, "kg" ),
                 csvwrangler.Order( 1001, datetime.datetime(2019,12,12), "P-10002", "Bagel", 15, "kg" ) ]

    i = 0
    for order in orders:
        assert ( order.OrderID == expected[i].OrderID )
        assert ( order.OrderDate == expected[i].OrderDate )
        assert ( order.ProductId == expected[i].ProductId )
        assert ( order.ProductName == expected[i].ProductName )
        assert ( order.Quantity == expected[i].Quantity )
        assert ( order.Unit == expected[i].Unit )
        i += 1