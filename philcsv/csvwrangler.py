import pandas as pd
import philcsv.csvhelper as csvhelper
import logging
from configparser import ConfigParser

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
def wrangle( csvFile, cfgFile = None ):

    # Read the .csv file
    df = pd.read_csv( csvFile,
                      error_bad_lines=False,
                      usecols=["Order Number", "Year", "Month", "Day", "Product Number", "Product Name", "Count"],
                      dtype={ 'Order Number': str, 'Year': str, 'Month': str, 'Day': str, 'Product Number': str, 'Product Name': str, 'Count': str } )

    # Defaults
    unit_value = "kg"
    qty_as_int = False

    # Process configuration file if provided
    if cfgFile is not None:
        config = ConfigParser()
        config.read(cfgFile)
        if "order" in config:
            if "unit" in config["order"]:
                unit_value = config["order"]["unit"]

            if "quantity" in config["order"]:
                qty_value = config["order"]["quantity"]
                if qty_value == "int" or qty_value == "integer":
                    qty_as_int = True

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

        # Convert quantity to integer if specified in config
        if qty_as_int:
            quantity=int(quantity)

        # Convert to Order class object to list
        order_list.append ( Order( order_id, order_date, df["Product Number"][i],
                                   df["Product Name"][i].title(), quantity, unit_value ) )

    # Return order list
    return order_list
