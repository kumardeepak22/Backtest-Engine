import typing
from datetime import datetime, time, date
from typing import Union

import numpy as np

from backtest.data import data
import os
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"
YY_MM_DD_FORMAT = "%Y-%m-%d"
BNF_WEEKLY_EXP_START_DATE = date(2016, 6, 27)
NF_WEEKLY_EXP_START_DATE = date(2019, 2, 11)
BANKNIFTY_SYMBOL = "BANKNIFTY"
NIFTY_SYMBOL = "NIFTY"
BANKNIFTY_LOT_SIZE = 25
NIFTY_LOT_SIZE = 50
BANKNIFTY_MARGIN_REQUIRED = 180000
NIFTY_MARGIN_REQUIRED = 130000
NOTIONAL_VALUE_ASSUMED = 1000000
BUY = "BUY"
SELL = "SELL"
OPTION_TYPE_CE = "CE"
OPTION_TYPE_PE = "PE"
INT_MAX = 1e18
INT_MIN = -1e18


def string_to_datetime(date_string: str) -> datetime:
    #Converts a string to a datetime object
    return datetime.strptime(date_string, YY_MM_DD_FORMAT)


def datetime_to_str(date_obj: datetime.date) -> str:
    #Converts a datetime object to a string.
    return date_obj.strftime(YY_MM_DD_FORMAT)


def str_to_time_obj(input_str: str) -> Union[datetime.time, None]:
    #Convert string of format "hh:mm" to time object
    try:
        hours, minutes = map(int, input_str.split(":"))
        time_obj = time(hour=hours, minute=minutes)
    except ValueError:
        print("Invalid input format. Please enter a string in the format 'hh:mm'")
        return None
    return time_obj


def get_opt_symbol(instrument: str, expiry_comp: str, strike: int, opt_type: str) -> str:
    """
    Returns Option symbol given instrument, strike, expiry component and option type(CE/PE)
    Args:
        instrument(str): instrument(ex: NIFTY/BANKNIFTY)
        expiry_comp(str): five letter expiry keyword(ex: 16JAN, 16609, 17N23)
        strike(int): strike
        opt_type(str): option type(CE/PE)

    Returns:
        str: returns option symbol
    """
    opt_symbol = f"{instrument.upper()}{expiry_comp}{strike}{opt_type}"
    return opt_symbol