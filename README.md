# Crisp - Back End Take Home Test

## How to Install
```
pip install wheel
python setup.py bdist_wheel
pip install dist/*.whl
```

### Dependencies
Pandas module

## How to run test cases
`python setup.py pytest`

## How to use code
Import the library as follows:    
`from philcsv import csvwrangler`

Call the wrangle function with input .csv file and optional .ini configuration file:  
```
orders = csvwrangler.wrangle( "groceryOrders.csv" )
orders = csvwrangler.wrangle( "groceryOrders.csv", "config.ini" )
```

The function will return a list of Order class objects (as defined in csvwrangler.py). Take the following 
python program as an example which uses the [orders.csv](https://gist.githubusercontent.com/daggerrz/99e766b4660e3c0ed26517beaea6449a/raw/e2d3a3e42ad1895baa430612f921bc87cfff651c/orders.csv) file as input:   

**test.py**
```
from philcsv import csvwrangler

orders = csvwrangler.wrangle("orders.csv")

for order in orders:
    print(order)
```

When run, the above program outputs the following:
```
1000 | 2018-01-01 00:00:00 | P-10001 | Arugola | 5250.50 | kg
1001 | 2017-12-12 00:00:00 | P-10002 | Iceberg Lettuce | 500.00 | kg
```

### Configuration file criteria
The external configuration file allows a user to change the **Unit** value from its default value of "kg" to some other value. It also allows to change the **Quantity** value from its default *BigDecimal* type to an *Integer* type. This can be achieved by specifying a quantity value of either "int" or "integer" (case insensitive).

Sample config.ini file (order, unit and quantity should all be lower-cased):
```
[order]
unit = lbs
quantity = Integer
```

## Architectural decisions
The input .csv file is being read using the pandas read_csv() function. This was chosen because we could easily improve upon the design by reading in large .csv files using the chunksize parameter. The current design does not handle very large .csv files (100,000+ rows) because we attempt to read the entire file in one go. For very large input .csv files, this will cause the system to crash due to 'Out Of Memory' errors. These issues can be resolved by reading in the .csv file in separate chunks. 

Due to the ambiguity of what should be done with the output data, the API returns the data as a list of Order class objects. Most likely, the API would need to be extended to store the output data in a database.

## Next steps
- For large .csv files, split up the reading of the file into manageable chunks.
- Determine where the output data should be stored and extend the API to store the output data in the database of your choosing.
- Gather information on what other configurations are necessary and extend the configuration file capabilities to support those.
