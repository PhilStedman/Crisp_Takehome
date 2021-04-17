import pandas as pd
import logging
import datetime
import json
from decimal import Decimal

SCHEMA = "schema"


# Class definition for Order object returned by API
class Order:
    ORDER_ID = "order_id"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    PRODUCT_ID = "product_id"
    PRODUCT_NAME = "product_name"
    QUANTITY = "quantity"

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


class Parser:
    def __init__(self, data_frame: dict, cfg_param: dict):
        self.data_frame = data_frame
        self.cfg_param = cfg_param

    def next(self):
        for idx in range(len(self.data_frame)):
            order = self.parse_line(idx)
            if order:
                yield order


class OrderParser(Parser):
    def __init__(self, data_frame: dict, cfg_params: dict):
        self.data_frame = data_frame
        self.cfg_params = cfg_params

    def parse_line(self, idx):
        errors = []
        # Process Order Number
        order_id = self._parse_order_id(idx, errors)
        order_date = self._parse_order_date(idx, errors)
        quantity = self._parse_quantity(idx, errors)

        if errors:
            # Log invalid row
            logging.warning("Error on line {idx}: {errors}\n{dump}".format(
                idx=idx + 2,
                errors=",".join(errors),
                dump=self.data_frame.iloc[1])
            )
            return None
        else:
            return Order(
                order_id,
                order_date,
                self.data_frame[self.cfg_params[Order.PRODUCT_ID]][idx],
                self.data_frame[self.cfg_params[Order.PRODUCT_NAME]][idx].title(),
                quantity,
                "kg",  # I think this default value should be dynamic, not hardcoded
            )

    def _parse_order_id(self, idx: int, errors: list) -> int:
        order_id = self.data_frame[self.cfg_params[Order.ORDER_ID]][idx]
        if order_id.isdigit():
            return int(order_id)
        else:
            errors.append("OrderID must be a positive integer.")
            return -1

    def _parse_order_date(self, idx: int, errors: list) -> datetime:
        year = self.data_frame[self.cfg_params[Order.YEAR]][idx]
        month = self.data_frame[self.cfg_params[Order.MONTH]][idx]
        day = self.data_frame[self.cfg_params[Order.DAY]][idx]

        valid = True
        if year.isdigit() is False or int(year) < 1:
            errors.append("'Year' value is not valid")
            valid = False

        if month.isdigit() is False or int(month) < 1 or int(month) > 12:
            errors.append("'Month' value is not valid")
            valid = False

        if day.isdigit() is False or int(day) < 1 or int(day) > 31:
            errors.append("'Day' value is not valid")
            valid = False

        return datetime.datetime(int(year), int(month), int(day)) if valid else None

    def _parse_quantity(self, idx: int, errors: list) -> Decimal:
        qty = self.data_frame[self.cfg_params[Order.QUANTITY]][idx]
        qty = qty.replace(",", "")
        try:
            float(qty)
        except ValueError:
            errors.append("'Quantity' is non-numeric.")
            return -1

        quantity = Decimal(qty)

        if quantity < 0:
            errors.append("Invalid row entry: 'Quantity' has a negative value.")
            return -1

        return quantity


# Main wrangle API function
def wrangle(csv_file, cfg_file=None) -> list:
    cfg_params = _parse_config_file(cfg_file)

    # Read the .csv file
    df = pd.read_csv(
        csv_file,
        error_bad_lines=False,
        usecols=cfg_params.values(),
        dtype={v: str for v in cfg_params.values()},
    )

    parser = OrderParser(df, cfg_params)
    return [order for order in parser.next()]


# Get field value from JSON config
def _get_column_name(config: dict, field: str) -> str:
    return config[SCHEMA][field] if field in config[SCHEMA] else CFG_DEFAULT[field]


# Config default values
CFG_DEFAULT = {
    Order.ORDER_ID: "Order Number",
    Order.YEAR: "Year",
    Order.MONTH: "Month",
    Order.DAY: "Day",
    Order.PRODUCT_ID: "Product Number",
    Order.PRODUCT_NAME: "Product Name",
    Order.QUANTITY: "Count",
}


# JSON Configuration file parser
def _parse_config_file(cfg_file: str) -> dict:
    result = CFG_DEFAULT.copy()
    if cfg_file:
        with open(cfg_file) as f:
            config = json.load(f)

        if config[SCHEMA]:
            result.update(config[SCHEMA])

    return result
