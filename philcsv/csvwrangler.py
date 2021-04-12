import pandas as pd
import philcsv.csvhelper as csvhelper
import logging

class Order:

    def __init__(self, order_id, order_date, product_id, product_name, quantity, unit):
        self.OrderID = order_id
        self.OrderDate = order_date
        self.ProductId = product_id
        self.ProductName = product_name
        self.Quantity = quantity
        self.Unit = unit

    def __repr__(self):
        return f"{self.OrderID} | {self.OrderDate} | {self.ProductId} | {self.ProductName} | {self.Quantity} | {self.Unit}"

# Main wrangling function
def wrangle( csvFile ):

    # Read the .csv file
    df = pd.read_csv( csvFile,
                      error_bad_lines=False,
                      usecols=["Order Number", "Year", "Month", "Day", "Product Number", "Product Name", "Count"],
                      dtype={ 'Order Number': str, 'Year': str, 'Month': str, 'Day': str, 'Product Number': str, 'Product Name': str, 'Count': str } )

    order_list = []

    # Loop through rows
    for i in range(len(df)):
        # Process Order Number
        order_id = csvhelper.processOrderNumber( df["Order Number"][i] )
        if order_id == -1:
            logging.warning( df.iloc[[i]] )
            continue

        # Process Year, Month, Day
        order_date = csvhelper.processOrderDate( df["Year"][i], df["Month"][i], df["Day"][i] )
        if order_date == -1:
            logging.warning( df.iloc[[i]] )
            continue

        # Process Count
        quantity = csvhelper.processCount( df["Count"][i] )
        if quantity == -1:
            logging.warning( df.iloc[[i]] )
            continue

        # Convert to OrderModel database object
        order_list.append ( Order( order_id, order_date, df["Product Number"][i],
                                   df["Product Name"][i].title(), quantity, 'kg' ) )

    # Return order list
    return order_list