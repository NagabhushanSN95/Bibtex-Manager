# Shree KRISHNAya Namaha
# Utilities for handling month datatype
# Author: Nagabhushan S N
# Last Modified: 19/08/2022

import datetime
import time
import traceback
from pathlib import Path

this_filepath = Path(__file__)
this_filename = this_filepath.stem


def month_long_to_short(month_long: str):
    month_short = None
    if month_long is not None:
        month_short = datetime.datetime.strptime(month_long,'%B').strftime('%b').lower()
    return month_short


def month_short_to_long(month_short: str):
    month_long = None
    if month_short is not None:
        month_long = datetime.datetime.strptime(month_short, '%b').strftime('%B')
    return month_long


def month_to_long(month: str):
    """
    month could be either long or short
    :param month:
    :return:
    """
    month_long = None
    if month is not None:
        month_long = datetime.datetime.strptime(month[:3], '%b').strftime('%B')
    return month_long
