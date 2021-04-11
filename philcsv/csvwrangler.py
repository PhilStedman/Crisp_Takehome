from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import logging
import philcsv.csvhelper as csvhelper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class OrderModel(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True)
    OrderDate = db.Column(db.DateTime, nullable=False)
    ProductId = db.Column(db.String(25), nullable=False)
    ProductName = db.Column(db.String(100), nullable=False)
    Quantity = db.Column(db.Numeric, nullable=False)
    Unit = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.OrderID} | {self.OrderDate} | {self.ProductId} | {self.ProductName} | {self.Quantity} | {self.Unit}"

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
        order_list.append ( OrderModel( OrderID = order_id,
                                        OrderDate = order_date,
                                        ProductId = df["Product Number"][i],
                                        ProductName = df["Product Name"][i].title(),
                                        Quantity = quantity,
                                        Unit = 'kg' ) )

    # Return order list, ready to be stored in SQLAlchemy database
    return order_list
