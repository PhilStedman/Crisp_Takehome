import pandas as pd
import logging
import datetime
import json
from decimal import Decimal
from typing import List


# Config file parameters
ORDER_ID = "order_id"
YEAR = "year"
MONTH = "month"
DAY = "day"
PRODUCT_ID = "product_id"
PRODUCT_NAME = "product_name"
QUANTITY = "quantity"


# Using 10 rows as proof of concept (realistically, you would read in much larger chunks)
CHUNK_SZ = 10
SCHEMA = "schema"


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
        return (
            f"{self.order_id} | {self.order_date} | {self.product_id} | "
            f"{self.product_name} | {self.quantity} | {self.unit}"
        )


class OrderParser:
    def __init__(self, data_frame, cfg_params: dict, chunk_num: int):
        self.data_frame = data_frame
        self.cfg_params = cfg_params
        self.chunk_num = chunk_num

    def parse_line(self, idx: int):
        errors = []  # type: List[str]
        idx += CHUNK_SZ * self.chunk_num

        # Process row
        order_id = self._parse_order_id(idx, errors)
        order_date = self._parse_order_date(idx, errors)
        quantity = self._parse_quantity(idx, errors)

        if errors:
            # Log invalid row
            logging.warning(
                "Error on line {line_num}: {errors}\n{dump}".format(
                    line_num=idx, errors=",".join(errors), dump=self.data_frame
                )
            )
            return None
        else:
            return Order(
                order_id,
                order_date,
                self.data_frame[self.cfg_params[PRODUCT_ID]][idx],
                self.data_frame[self.cfg_params[PRODUCT_NAME]][idx].title(),
                quantity,
                "kg",  # Note: we could make this dynamically configurable via config file
            )

    def next(self):
        for idx in range(len(self.data_frame)):
            result = self.parse_line(idx)
            if result:
                yield result

    # Helper functions to process CSV column values
    def _parse_order_id(self, idx: int, errors: list) -> int:
        order_id = self.data_frame[self.cfg_params[ORDER_ID]][idx]
        if order_id.isdigit():
            return int(order_id)
        else:
            errors.append("OrderID must be a positive integer.")
            return -1

    def _parse_order_date(self, idx: int, errors: list):
        year = self.data_frame[self.cfg_params[YEAR]][idx]
        month = self.data_frame[self.cfg_params[MONTH]][idx]
        day = self.data_frame[self.cfg_params[DAY]][idx]

        valid = True
        if year.isdigit() is False or int(year) < 1:
            errors.append("Year value is not valid")
            valid = False

        if month.isdigit() is False or int(month) < 1 or int(month) > 12:
            errors.append("Month value is not valid")
            valid = False

        if day.isdigit() is False or int(day) < 1 or int(day) > 31:
            errors.append("Day value is not valid")
            valid = False

        return datetime.datetime(int(year), int(month), int(day)) if valid else None

    def _parse_quantity(self, idx: int, errors: list):
        qty = self.data_frame[self.cfg_params[QUANTITY]][idx]
        qty = qty.replace(",", "")

        try:
            float(qty)
        except ValueError:
            errors.append("Quantity is non-numeric.")
            return -1

        quantity = Decimal(qty)

        if quantity < 0:
            errors.append("Quantity has a negative value.")
            return -1

        return quantity


# Main wrangle API function
def wrangle(csv_file, cfg_file="") -> list:

    cfg_params = _parse_config_file(cfg_file)

    order_list = []
    chunk_num = 0

    # Read the .csv file
    for df in pd.read_csv(
        csv_file,
        chunksize=CHUNK_SZ,
        error_bad_lines=False,
        usecols=cfg_params.values(),
        dtype={v: str for v in cfg_params.values()},
    ):
        parser = OrderParser(df, cfg_params, chunk_num)
        for order in parser.next():
            order_list.append(order)

        chunk_num += 1

    return order_list


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


# JSON Configuration file parser
def _parse_config_file(cfg_file: str) -> dict:

    result = CFG_DEFAULT.copy()

    if cfg_file:
        with open(cfg_file) as f:
            config = json.load(f)

        if config[SCHEMA]:
            result.update(config[SCHEMA])

    return result
