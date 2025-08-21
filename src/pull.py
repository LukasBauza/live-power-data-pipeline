import asyncio
from entsoe.entsoe import EntsoePandasClient
import pandas

from .config import API_KEY, RAW_DIR
from .logger import log
from .file_handler import FileHandler


class LoadPuller:
    def __init__(self, country_code: str, time_zone: str):
        self.client: EntsoePandasClient = EntsoePandasClient(api_key=API_KEY)
        self.country_code: str = country_code
        self.time_zone: str = time_zone
        self.file_handler: FileHandler = FileHandler("load", country_code)

        if self.file_handler.file_empty():
            log.info("Initialising data from last 7 days.")
            end = pandas.Timestamp.now(tz=self.time_zone).floor("h")
            start = end - pandas.Timedelta(days=7)
            print("wowowow:", end)

            try:
                load_data = asyncio.run(self.pull_with_retries(start, end))
                if load_data.empty:
                    log.warning("No initial data retrieved for the last 7 days.")
                else:
                    self.file_handler.save_to_csv(load_data)
            except Exception as e:
                log.error(f"Failed to pull intial data: {e}")

    def pull_load(self, start: pandas.Timestamp, end: pandas.Timestamp):
        return self.client.query_load(self.country_code, start=start, end=end)

    async def pull_load_data_async(
        self, start: pandas.Timestamp, end: pandas.Timestamp
    ):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.pull_load, start, end)

    async def pull_with_retries(self, start, end, attempts: int = 3, delay: int = 300):
        for attempt in range(1, attempts + 1):
            try:
                load_data = await self.pull_load_data_async(start, end)
                if not load_data.empty:
                    return load_data
                log.warning(
                    f"Attempt {attempt} returned empty data for {start} to {end}"
                )
            except Exception as e:
                log.error(f"Attempt {attempt} failed: {e}")

            if attempt < attempts:
                log.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)

        log.error(f"All {attempts} attempts failed for {start} to {end}")
        return pandas.DataFrame()

    async def hourly_pull(self):
        while True:
            end = pandas.Timestamp.now(tz=self.time_zone).floor("h")
            last_saved = self.file_handler.read_last_entry()

            if last_saved is not None:
                last_saved = pandas.Timestamp(last_saved)
                last_saved = last_saved.tz_convert(tz=self.time_zone)
            else:
                last_saved = end - pandas.Timedelta(hours=1)

            log.info(f"Previous last entry {last_saved}")

            try:
                load_data = await self.pull_load_data_async(last_saved, end)
                if load_data.empty:
                    log.warning("No data returned")
                else:
                    log.info(f"Data retrieved\n {load_data}")
            except Exception as e:
                log.error(f"Error fetching data: {e}\n Time: {last_saved} to {end}")

            await asyncio.sleep(3600)
