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

Call the wrangle function with input .csv file and optional .ini configuration file:
```
orders = wrangler.wrangle( "groceryOrders.csv" )
orders = wrangler.wrangle( "groceryOrders.csv", "config.ini" )
```

The function will return a list of Order class objects (as defined in wrangler.py). Take the following
python program as an example which uses the [orders.csv](https://gist.githubusercontent.com/daggerrz/99e766b4660e3c0ed26517beaea6449a/raw/e2d3a3e42ad1895baa430612f921bc87cfff651c/orders.csv) file as input:

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
config.ini:
```
[schema]
order_id = Order ID
year = YYYY
month = MM
day = DD
product_id = ProductNo
product_name = Product Name
quantity = Qty
```

The above configuration specifies that the order_id can be found in the "Order ID" column, the year can be found in the "YYYY" column, etc... The contents of the configuration file are case-sensitive, if any one of the above keys cannot be found, then the program will default to a pre-defined default value. The default values are listed below:

```
order_id = "Order Number"
year = "Year"
month = "Month"
day = "Day"
product_id = "Product Number"
product_name =  "Product Name"
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
The input .csv file is being read using the pandas read_csv() function. This was chosen because we could easily improve upon the design by reading in large .csv files using the chunksize parameter. The current design does not handle very large .csv files (100,000+ rows) because we attempt to read the entire file in one go. For very large input .csv files, this will cause the system to crash due to 'Out Of Memory' errors. These issues can be resolved by reading in the .csv file in separate chunks.

Due to the ambiguity of what should be done with the output data, the API returns the data as a list of Order class objects. Most likely, the API would need to be extended to store the output data in a database.

## Next steps
- For large .csv files, split up the reading of the file into manageable chunks.
- Determine where the output data should be stored and extend the API to store the output data in the database of your choosing.
- Improve the capabilities of the configuration file to be less restrictive on the form of the input CSV file, e.g. a particular partner may be storing the date in a single column called "YYYY-MM-DD". The current design would not be able to handle this case.
