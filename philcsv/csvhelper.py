import logging, datetime
from decimal import Decimal

# Helper functions to process CSV column values
def processOrderNumber( orderNo ):
    if orderNo.isdigit():
        return int(orderNo)
    else:
        logging.warning( "Invalid row entry: 'Order Number' must be a positive integer." )
        return -1

def processOrderDate( year, month, day ):
    if year.isdigit() == False or int(year) < 1:
        logging.warning( "Invalid row entry: 'Year' value is not valid" )
        return -1

    if month.isdigit() == False or int(month) < 1 or int(month) > 12:
        logging.warning( "Invalid row entry: 'Month' value is not valid" )
        return -1

    if day.isdigit() == False or int(day) < 1 or int(day) > 31:
        logging.warning( "Invalid row entry: 'Day' value is not valid" )
        return -1

    order_date = datetime.datetime( int(year), int(month), int(day) )
    return order_date

def processCount( qty ):
    qty = qty.replace(',', '')

    try:
        float(qty)
    except ValueError:
        logging.warning( "Invalid row entry: 'Count' is non-numeric." )
        return -1

    qty = Decimal(qty)

    if qty < 0:
        logging.warning( "Invalid row entry: 'Count' has a negative value." )
        return -1

    return qty
