"""Miscellaneous functions for Genbabel package.
"""

import datetime


def getfilename():
    """Return the filename based on the datetime.

    :return: the filename in year-month-day_hour-minute
    :rtype: str
    """

    timenow = datetime.datetime.now()

    year = str(timenow.year % 100)
    month = str(timenow.month).zfill(2)
    day = str(timenow.day).zfill(2)
    hour = str(timenow.hour).zfill(2)
    minute = str(timenow.minute).zfill(2)

    filename = year + month + day + "_" + hour + minute

    return filename
