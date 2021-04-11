# Crisp - Back End Take Home Test

## How to Install
`python3 setup.py bdist_wheel`

`pip3 install /path/to/wheelfile.whl`

## Dependencies

Pandas, Flask, SQLAlchemy

## How to use code
Add the following import to your python code  
`from philcsv import csvwrangler`

Call the wrangle function as follows with input .csv file:
`orders = csvwrangler.wrangle( "csvfile" )`

The function will return a list of OrderModel class objects (function definition can be found in `csvwrangler.py`.

OrderModel class definition:
```
class OrderModel(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True)
    OrderDate = db.Column(db.DateTime, nullable=False)
    ProductId = db.Column(db.String(25), nullable=False)
    ProductName = db.Column(db.String(100), nullable=False)
    Quantity = db.Column(db.Numeric, nullable=False)
    Unit = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.OrderID} | {self.OrderDate} | {self.ProductId} | {self.ProductName} | {self.Quantity} | {self.Unit}"
```

## Architectural overview

## Next steps
