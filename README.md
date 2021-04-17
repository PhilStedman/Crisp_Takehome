# CSV wrangler

## How to Install
```
pip install wheel
python setup.py bdist_wheel
pip install dist/*.whl
```

### Dependencies
Pandas module

## How to run test cases
`pytest -v`

## How to use code
Import the library as follows:
`from philcsv import wrangler`

Call the wrangle function with input .csv file and optional .json configuration file:
```
orders = wrangler.wrangle( "groceryOrders.csv" )
orders = wrangler.wrangle( "groceryOrders.csv", "config.json" )
```

The function will return a list of Order class objects (as defined in wrangler.py). Take the following
Python program as an example which uses the [orders.csv](https://gist.githubusercontent.com/daggerrz/99e766b4660e3c0ed26517beaea6449a/raw/e2d3a3e42ad1895baa430612f921bc87cfff651c/orders.csv) file as input:

**test.py**
```
from philcsv import wrangler

orders = wrangler.wrangle("orders.csv")

for order in orders:
    print(order)
```

When run, the above program outputs the following:
```
1000 | 2018-01-01 00:00:00 | P-10001 | Arugola | 5250.50 | kg
1001 | 2017-12-12 00:00:00 | P-10002 | Iceberg Lettuce | 500.00 | kg
```

### Configuration file criteria
The external configuration file allows a user to adjust the expected column names in the input CSV file. Take the following configuration file for example:

**config.json**
```
{
    "schema":{
        "order_id": "Order ID",
        "year": "YYYY",
        "month": "MM",
        "day": "DD",
        "product_id": "ProductNo",
        "product_name": "Product Name",
        "quantity": "Qty"
    }
}
```

The above configuration specifies that the order_id can be found in the "Order ID" column, the year can be found in the "YYYY" column, etc... The contents of the configuration file are case-sensitive, if any one of the above keys cannot be found, then the program will default to a pre-defined value. The default values are listed below:

```
order_id = "Order Number"
year = "Year"
month = "Month"
day = "Day"
product_id = "Product Number"
product_name = "Product Name"
quantity = "Count"
```

## Assumptions made
For this project, I assume we are working with a static target schema, that is we have a database and it has the following schema:

Column name | Type
--- | ---
OrderID | Integer
OrderDate | Date
ProductId | String
ProductName | String (proper cased)
Quantity | BigDecimal
Unit | String

The goal here is to have a program that can read input CSV files provided by partners which could have varying headers. In order to accomodate varying input CSV files, we provide a config file which can be used to specify where to look for each column value of interest.

## Architectural decisions
The input .csv file is being read using the pandas read_csv() function. This was chosen because it gives us the ability to read in the .csv file in separate chunks, this allows to be able to handle very large .csv files (100,000+ rows) which would otherwise cause us to hit an 'Out of Memory' error.

Furthermore, the configuration file is specified in JSON format as this provides us with the flexibility to expand the configuration file capabilities to support more complicated configurations in the future.

Due to the ambiguity of what should be done with the output data, the API returns the data as a list of Order class objects. Most likely, the API would need to be extended to store the output data in a database. (Note: that for very large input .csv files returning the result as an object list would also cause us to hit 'Out of Memory' conditions, but in production we would be storing the result in a database and not in memory.)

## Next steps
- Determine where the output data should be stored and extend the API to store the output data in the database of your choosing.
- Improve the capabilities of the configuration file to be less restrictive on the form of the input CSV file, e.g. a particular partner may be storing the date in a single column called "YYYY-MM-DD". The current design would not be able to handle this case.
- Another useful config would be to allow changing the unit value from "kg" to something else (trivial to implement).
