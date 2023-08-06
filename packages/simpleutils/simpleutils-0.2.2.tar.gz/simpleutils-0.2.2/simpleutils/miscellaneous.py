# -*- coding: utf-8 -*-
"""
Created on 2017-5-7

@author: cheng.li
"""

import sys
import os
import datetime as dt
from typing import Union
import pendulum


def add_parent_path(name: str, level: int):
    """
    Add the target folder to the python search path

    :param name: str, file name
    :param level: int, how many level of parents folder should go up
    :return:
    """
    current_path = os.path.abspath(name)
    sys.path.append(os.path.sep.join(current_path.split(os.path.sep)[:-level]))


def to_datetime(date: Union[dt.datetime, dt.date]):
    """
    Parse a datetime/date object to datetime. Only keep the resolution to seconds

    :param date: Union[dt.datetime, dt.date]
    :return: dt.datetime
    """
    if isinstance(date, dt.datetime):
        return dt.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)
    elif isinstance(date, dt.date):
        return dt.datetime(date.year, date.month, date.day)
    else:
        raise ValueError("<{0}>'s type is not recognized. Its type is <{1}>".format(date, type(date)))


def dt2unix(time_stamp: str, tz: str = None) -> int:
    if len(time_stamp) == 25:
        date_time = pendulum.parse(time_stamp, tz=time_stamp[-6:])
    else:
        date_time = pendulum.parse(time_stamp, tz=tz)
    return int(date_time.timestamp())


def unix2dt(unix_stamp: int, tz: str = None) -> str:
    date_time = pendulum.from_timestamp(unix_stamp, tz=tz)
    return date_time.isoformat()


def list_eq(lhs: list, rhs: list):
    """
    Check the equality of 2 lists

    :param lhs: list
    :param rhs: list
    :return: bool
    """

    if not lhs and not rhs:
        return True

    if len(lhs) != len(rhs):
        return False

    for i, v1 in enumerate(lhs):
        if v1 != rhs[i]:
            return False
    return True
