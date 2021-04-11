# Crisp_Takehome

Using Pandas over CSV due to potentially large data sets

I will use SQLAlchemy over SQLite for better portability to a real relational database if need be in the future.

For larger CSV files with hundreds of thousands of rows, we may want to consider splitting up the reading of the file
into separate same-sized chunks.

# How to use library:
from philcsv import csvwrangler

orders = csvwrangler.wrangle( "csvfile" )

for order in orders:
   print (order)
