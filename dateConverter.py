from datetime import datetime
from pymongo import MongoClient


def convert_date(date_str: str) -> datetime:
    # Polish month names mapping
    months_pl = {
        "stycznia": 1,
        "lutego": 2,
        "marca": 3,
        "kwietnia": 4,
        "maja": 5,
        "czerwca": 6,
        "lipca": 7,
        "sierpnia": 8,
        "września": 9,
        "października": 10,
        "listopada": 11,
        "grudnia": 12
    }

    # Parse string
    date_arr = date_str.split()
    time_arr = date_arr[3].split(":")

    day_str = date_arr[0]
    month_str = date_arr[1]
    year_str = date_arr[2]
    hour = time_arr[0]
    minute = time_arr[1]

    day = int(day_str)
    month = months_pl[month_str]
    year = int(year_str)
    hour = int(hour)
    minute = int(minute)

    # Convert to Python datetime
    date_obj = datetime(year, month, day, hour, minute)
    return date_obj
