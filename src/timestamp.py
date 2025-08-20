import pandas

from config import TIME_ZONE
from logger import log


def create_timestamp(date: str, future: bool = False):
    try:
        now = pandas.Timestamp.now(tz=TIME_ZONE)
        timestamp = pandas.Timestamp(date, tz=TIME_ZONE)

        if timestamp > now and future == False:
            log.warning(f"Date {timestamp} is in the future.")

    except Exception as e:
        log.error(f"Error processing timestamp '{date}': {e}")
