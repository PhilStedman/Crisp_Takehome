# Crisp - Back End Take Home Test

## How to Install
```
python3 setup.py bdist_wheel
pip3 install dist/*.whl
```

### Dependencies
Pandas module

## How to run test cases
`python3 setup.py pytest`

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
The external configuration file allows a user to change the default **Unit** value from its default value of "kg" to some other value. It also allows to change the **Quantity** value from its default *BigDecimal* type to an *Integer* type. This can be achieved by specifying a quantity value of either "int" or "integer" (case insensitive).

Sample config.ini file:
```
[order]
unit = lbs
quantity = Integer
```

## Architectural overview

## Next steps
