from os import makedirs
from os.path import dirname
from .config import RAW_DIR
from .logger import log


def save_csv(data_type: str, country_code: str, data):
    file_path = f"{RAW_DIR}/{data_type}_{country_code}.csv"

    try:
        # NOTE: dirname() needed?
        makedirs(dirname(RAW_DIR), exist_ok=True)
    except Exception as e:
        log.error(f"Error creating directory")

    try:
        data.to_csv(file_path, mode="a")
        log.info(f"Data saved to {file_path}")
    except Exception as e:
        log.error(f"Failed writing to {file_path}: {e}")
