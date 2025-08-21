# from calendar import week
from fastapi import FastAPI

# from ..src.config import COUNTRY_CODE
from src.config import PROCESSED_DIR
from src.logger import log

api = FastAPI()


week_average_load = week_peak_load = ""

try:
    with open(f"{PROCESSED_DIR}/week_average_load.txt") as file:
        week_average_load = file.read()

except Exception as e:
    log.warning(f"Error opening {week_average_load}: {e}")

try:
    with open(f"{PROCESSED_DIR}/week_peak_load.txt") as file:
        week_peak_load = file.read()

except Exception as e:
    log.warning(f"Error opening {week_peak_load}: {e}")


@api.get("/")
def load_summary():
    return {
        "average load for week": f"{week_average_load}",
        "peak load for week": f"{week_peak_load}",
    }
