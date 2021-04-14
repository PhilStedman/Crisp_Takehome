import pandas as pd
import logging
import datetime
from configparser import ConfigParser
from decimal import Decimal

# Constants
ORDER_NUMBER = "Order Number"
YEAR = "Year"
MONTH = "Month"
DAY = "Day"
PRODUCT_NUMBER = "Product Number"
PRODUCT_NAME = "Product Name"
COUNT = "Count"


# Class definition for Order object returned by API
class Order:
    def __init__(
        self, order_id: int, order_date: datetime.datetime, product_id: str, product_name: str, quantity, unit
    ):
        self.order_id = order_id
        self.order_date = order_date
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit = unit

    def __eq__(self, other):
        if not isinstance(other, Order):
            return NotImplemented

        return (
            self.order_id == other.order_id
            and self.order_date == other.order_date
            and self.product_id == other.product_id
            and self.product_name == other.product_name
            and self.quantity == other.quantity
            and self.unit == other.unit
        )

    def __repr__(self):
        return f"{self.order_id} | {self.order_date} | {self.product_id} | \
                 {self.product_name} | {self.quantity} | {self.unit}"


# Main wrangle API function
def wrangle(csv_file, cfg_file="") -> list:

    # Read the .csv file
    df = pd.read_csv(
        csv_file,
        error_bad_lines=False,
        usecols=[
            ORDER_NUMBER,
            YEAR,
            MONTH,
            DAY,
            PRODUCT_NUMBER,
            PRODUCT_NAME,
            COUNT,
        ],
        dtype={
            ORDER_NUMBER: str,
            YEAR: str,
            MONTH: str,
            DAY: str,
            PRODUCT_NUMBER: str,
            PRODUCT_NAME: str,
            COUNT: str,
        },
    )

    # Config default values
    cfg_params = {"unit": "kg", "qty_as_int": False}

    # Process configuration file if provided
    if cfg_file:
        _parse_config_file(cfg_file, cfg_params)

    order_list = []

    # Loop through rows
    for i in range(len(df)):
        # Process Order Number
        order_id = _process_order_number(df[ORDER_NUMBER][i])
        if order_id == -1:
            # Log invalid row
            logging.warning(df.iloc[[i]])
            continue

        # Process Year, Month, Day
        order_date = _process_order_date(df[YEAR][i], df[MONTH][i], df[DAY][i])
        if order_date == -1:
            # Log invalid row
            logging.warning(df.iloc[[i]])
            continue

        # Process Count
        quantity = _process_count(df[COUNT][i])
        if quantity == -1:
            # Log invalid row
            logging.warning(df.iloc[[i]])
            continue

        # Convert quantity to integer if specified in config
        if cfg_params["qty_as_int"]:
            quantity = int(quantity)

        # Convert to Order class object to list
        order_list.append(
            Order(
                order_id,
                order_date,
                df[PRODUCT_NUMBER][i],
                df[PRODUCT_NAME][i].title(),
                quantity,
                cfg_params["unit"],
            )
        )

    # Return order list
    return order_list


# Configuration file parser
def _parse_config_file(cfg_file: str, cfg_params: dict):
    config = ConfigParser()
    config.read(cfg_file)
    if "order" in config:
        if "unit" in config["order"]:
            cfg_params["unit"] = config["order"]["unit"]

        if "quantity" in config["order"]:
            qty_value = config["order"]["quantity"].lower()
            if qty_value == "int" or qty_value == "integer":
                cfg_params["qty_as_int"] = True


# Helper functions to process CSV column values
def _process_order_number(order_no: str) -> int:
    if order_no.isdigit():
        return int(order_no)
    else:
        logging.warning("Invalid row entry: 'Order Number' must be a positive integer.")
        return -1


def _process_order_date(year: str, month: str, day: str):
    if year.isdigit() is False or int(year) < 1:
        logging.warning("Invalid row entry: 'Year' value is not valid")
        return -1

    if month.isdigit() is False or int(month) < 1 or int(month) > 12:
        logging.warning("Invalid row entry: 'Month' value is not valid")
        return -1

    if day.isdigit() is False or int(day) < 1 or int(day) > 31:
        logging.warning("Invalid row entry: 'Day' value is not valid")
        return -1

    order_date = datetime.datetime(int(year), int(month), int(day))
    return order_date


def _process_count(qty: str):
    qty = qty.replace(",", "")

    try:
        float(qty)
    except ValueError:
        logging.warning("Invalid row entry: 'Count' is non-numeric.")
        return -1

    quantity = Decimal(qty)

    if quantity < 0:
        logging.warning("Invalid row entry: 'Count' has a negative value.")
        return -1

    return quantity
