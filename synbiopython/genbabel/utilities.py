"""Miscellaneous functions.
"""

import datetime


def getfilename():
    """Generate the filename based on the datetime."""

    timenow = datetime.datetime.now()

    year = str(timenow.year % 100)
    month = str(timenow.month).zfill(2)
    day = str(timenow.day).zfill(2)
    hour = str(timenow.hour).zfill(2)
    minute = str(timenow.minute).zfill(2)

    filename = year + month + day + "_" + hour + minute

    return filename
