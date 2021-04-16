import pandas as pd
import logging
import datetime
import json
from decimal import Decimal

# Config file parameters
ORDER_ID = "order_id"
YEAR = "year"
MONTH = "month"
DAY = "day"
PRODUCT_ID = "product_id"
PRODUCT_NAME = "product_name"
QUANTITY = "quantity"

# Other constants
SCHEMA = "schema"

# Config default values
CFG_DEFAULT = {
    ORDER_ID: "Order Number",
    YEAR: "Year",
    MONTH: "Month",
    DAY: "Day",
    PRODUCT_ID: "Product Number",
    PRODUCT_NAME: "Product Name",
    QUANTITY: "Count",
}


# Class definition for Order object returned by API
class Order:
    def __init__(
        self,
        order_id: int,
        order_date: datetime.datetime,
        product_id: str,
        product_name: str,
        quantity: Decimal,
        unit: str,
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

    # Process configuration file if provided
    if cfg_file:
        cfg_params = _parse_config_file(cfg_file)
    else:
        cfg_params = CFG_DEFAULT

    # Read the .csv file
    df = pd.read_csv(
        csv_file,
        error_bad_lines=False,
        usecols=[
            cfg_params[ORDER_ID],
            cfg_params[YEAR],
            cfg_params[MONTH],
            cfg_params[DAY],
            cfg_params[PRODUCT_ID],
            cfg_params[PRODUCT_NAME],
            cfg_params[QUANTITY],
        ],
        dtype={
            cfg_params[ORDER_ID]: str,
            cfg_params[YEAR]: str,
            cfg_params[MONTH]: str,
            cfg_params[DAY]: str,
            cfg_params[PRODUCT_ID]: str,
            cfg_params[PRODUCT_NAME]: str,
            cfg_params[QUANTITY]: str,
        },
    )

    order_list = []

    # Loop through rows
    for i in range(len(df)):
        # Process Order Number
        order_id = _process_order_number(df[cfg_params[ORDER_ID]][i])
        if order_id == -1:
            # Log invalid row
            logging.warning(df.iloc[[i]])
            continue

        # Process Year, Month, Day
        order_date = _process_order_date(df[cfg_params[YEAR]][i], df[cfg_params[MONTH]][i], df[cfg_params[DAY]][i])
        if order_date == -1:
            # Log invalid row
            logging.warning(df.iloc[[i]])
            continue

        # Process Count
        quantity = _process_count(df[cfg_params[QUANTITY]][i])
        if quantity == -1:
            # Log invalid row
            logging.warning(df.iloc[[i]])
            continue

        # Convert to Order class object to list
        order_list.append(
            Order(
                order_id,
                order_date,
                df[cfg_params[PRODUCT_ID]][i],
                df[cfg_params[PRODUCT_NAME]][i].title(),
                quantity,
                "kg",
            )
        )

    # Return order list
    return order_list


# Get field value from JSON config
def _get_column_name(config: dict, field: str) -> str:
    return config[SCHEMA][field] if field in config[SCHEMA] else CFG_DEFAULT[field]


# JSON Configuration file parser
def _parse_config_file(cfg_file: str) -> dict:

    with open(cfg_file) as f:
        config = json.load(f)

    if SCHEMA in config:
        return {
            ORDER_ID: _get_column_name(config, ORDER_ID),
            YEAR: _get_column_name(config, YEAR),
            MONTH: _get_column_name(config, MONTH),
            DAY: _get_column_name(config, DAY),
            PRODUCT_ID: _get_column_name(config, PRODUCT_ID),
            PRODUCT_NAME: _get_column_name(config, PRODUCT_NAME),
            QUANTITY: _get_column_name(config, QUANTITY),
        }
    else:
        return CFG_DEFAULT


# Helper functions to process CSV column values
def _process_order_number(order_no: str) -> int:
    if order_no.isdigit():
        return int(order_no)
    else:
        logging.warning("Invalid row entry: 'OrderID' must be a positive integer.")
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
        logging.warning("Invalid row entry: 'Quantity' is non-numeric.")
        return -1

    quantity = Decimal(qty)

    if quantity < 0:
        logging.warning("Invalid row entry: 'Quantity' has a negative value.")
        return -1

    return quantity
