import pandas

from .config import TIME_ZONE
from .logger import log


def create_timestamp(date: str, future: bool = False) -> pandas.Timestamp:
    now = pandas.Timestamp.now(tz=TIME_ZONE)
    try:
        timestamp = pandas.Timestamp(date, tz=TIME_ZONE)

        if timestamp > now and future == False:
            log.warning(f"Date {timestamp} is in the future.")

        return timestamp

    except Exception as e:
        log.error(f"Issue processing timestamp '{date}': {e}")
        log.warning(f"Using current time '{now}'.")

        return now
