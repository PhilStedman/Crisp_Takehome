from philcsv import csvwrangler
from pathlib import Path
import datetime

def test_samplecsv():
    file = Path(__file__).parent / "testcsvs/sample.csv"
    orders = csvwrangler.wrangle( file )

    expected = [ csvwrangler.OrderModel( OrderID = 1000, OrderDate = datetime.datetime(2018,1,1), ProductId = "P-10001",
                                         ProductName = "Arugola", Quantity = 5250.50, Unit = "kg" ),
                 csvwrangler.OrderModel( OrderID = 1001, OrderDate = datetime.datetime(2017,12,12), ProductId = "P-10002",
                                         ProductName = "Iceberg Lettuce", Quantity = 500.00, Unit = "kg" )  ]

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

    expected = [ csvwrangler.OrderModel( OrderID = 1000, OrderDate = datetime.datetime(2020,6,27), ProductId = "P-9001",
                                         ProductName = "Chocolate", Quantity = 5.25, Unit = "kg" ),
                 csvwrangler.OrderModel( OrderID = 1001, OrderDate = datetime.datetime(2019,12,12), ProductId = "P-10002",
                                         ProductName = "Bagel", Quantity = 15, Unit = "kg" )  ]

    i = 0
    for order in orders:
        assert ( order.OrderID == expected[i].OrderID )
        assert ( order.OrderDate == expected[i].OrderDate )
        assert ( order.ProductId == expected[i].ProductId )
        assert ( order.ProductName == expected[i].ProductName )
        assert ( order.Quantity == expected[i].Quantity )
        assert ( order.Unit == expected[i].Unit )
        i += 1