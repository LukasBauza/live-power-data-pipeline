from os import makedirs, stat
from os.path import dirname, isfile, getsize
import pandas

from .config import RAW_DIR
from .logger import log


class FileHandler:
    def __init__(self, data_type: str, country_code: str):
        self.file_path: str = f"{RAW_DIR}/{data_type}_{country_code}.csv"

    def ensure_dir_exists(self):
        try:
            makedirs(RAW_DIR, exist_ok=True)
        except Exception as e:
            log.error(f"Error creating directory: {e}")

    def file_empty(self):
        if not isfile(self.file_path):
            return True
        if getsize(self.file_path) == 0:
            return True

        log.info(f"File '{self.file_path}' not empty")
        return False

    def save_to_csv(self, data: pandas.DataFrame):
        self.ensure_dir_exists()

        try:
            # Only add the header if it doesn't exist
            header_exists = isfile(self.file_path)
            data.to_csv(self.file_path, mode="a", header=not header_exists, index=True)
            log.info(f"Data saved to {self.file_path}")
        except Exception as e:
            log.error(f"Failed writing to {self.file_path}: {e}")
