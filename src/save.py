from os import makedirs, stat
from os.path import dirname, isfile
import pandas

from .config import RAW_DIR
from .logger import log


def ensure_dir_exists(dir: str):
    try:
        makedirs(dir, exist_ok=True)
    except Exception as e:
        log.error(f"Error creating directory: {e}")


def save_csv(data_type: str, country_code: str, data: pandas.DataFrame):
    file_path = f"{RAW_DIR}/{data_type}_{country_code}.csv"

    ensure_dir_exists(RAW_DIR)

    try:
        # Only add the header if it doesn't exist
        header_exists = isfile(file_path)
        data.to_csv(file_path, mode="a", header=not header_exists, index=True)
        # Custom headers created, as for some reason the timestamp header is not created,
        # but timestamp data is written to file
        log.info(f"Data saved to {file_path}")
    except Exception as e:
        log.error(f"Failed writing to {file_path}: {e}")
