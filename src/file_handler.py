from datetime import timedelta
from os import makedirs, stat
from os.path import dirname, isfile, getsize
import pandas

from .config import PROCESSED_DIR, RAW_DIR, TIME_ZONE
from .logger import log


class FileHandler:
    def __init__(self, data_type: str, country_code: str):
        self.file_path: str = f"{RAW_DIR}/{data_type}_{country_code}.csv"

    def ensure_dir_exists(self, dir: str):
        try:
            makedirs(dir, exist_ok=True)
        except Exception as e:
            log.error(f"Error creating directory: {e}")

    def file_empty(self):
        if not isfile(self.file_path):
            return True
        if getsize(self.file_path) == 0:
            return True

        return False

    def save_to_csv(self, data: pandas.DataFrame):
        self.ensure_dir_exists(RAW_DIR)

        try:
            # Only add the header if it doesn't exist
            header_exists = isfile(self.file_path)
            data.to_csv(self.file_path, mode="a", header=not header_exists, index=True)
            log.info(f"Data saved to {self.file_path}")

        except Exception as e:
            log.error(f"Failed writing to {self.file_path}: {e}")

    def read_last_entry(self):
        if self.file_empty():
            log.info(
                f"No entries to read from '{self.file_path}' (file missing or empty)."
            )
            return None

        try:
            last_entry = pandas.read_csv(
                self.file_path, index_col=0, parse_dates=True
            ).index[-1]
            log.info(f"Read last entry timestamp {last_entry} from '{self.file_path}'.")

            return last_entry

        except Exception as e:
            log.error(f"Failed to read last entry from '{self.file_path}': {e}")

            return None

    def read_previous_days(self, days: int):
        if self.file_empty():
            log.info(
                f"No entries to read from '{self.file_path}' (file missing or empty)."
            )
            return None

        try:
            df = pandas.read_csv(self.file_path, index_col=0, parse_dates=True)

            if not isinstance(df.index, pandas.DatetimeIndex):
                df.index = pandas.to_datetime(df.index)

            today = pandas.Timestamp.now(tz=TIME_ZONE).normalize()
            start_date = today - timedelta(days=days)
            filtered_df = df[df.index >= start_date]

            log.info(
                f"Ready {len(filtered_df)} entries from '{self.file_path}' from {start_date} to now"
            )

            return filtered_df

        except Exception as e:
            log.error(
                f"Failed to read previous {days} days from '{self.file_path}': {e}"
            )
            return None

    def save_to_txt(self, data, txt_file_name: str):
        self.ensure_dir_exists(PROCESSED_DIR)
        txt_path = f"{PROCESSED_DIR}/{txt_file_name}.txt"

        try:
            with open(txt_path, "w") as file:
                file.write(str(data) + "\n")
        except Exception as e:
            log.error(f"Failed writing to {txt_path}: {e}")
