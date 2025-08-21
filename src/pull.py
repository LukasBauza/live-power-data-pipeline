import asyncio
from entsoe.entsoe import EntsoePandasClient
import pandas

from .config import API_KEY
from .logger import log
from .save import save_csv


class LoadPuller:
    def __init__(self, country_code: str, time_zone: str):
        self.client: EntsoePandasClient = EntsoePandasClient(api_key=API_KEY)
        self.country_code: str = country_code
        self.time_zone: str = time_zone

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
            # Make sure that it is at the current hour, minutes not needed
            end = pandas.Timestamp.now(tz=self.time_zone).floor("h")
            start = end - pandas.Timedelta(hours=24)

            log.info(f"Pulling load data for {start} to {end} at {self.country_code}")
            load_data = pandas.DataFrame()
            try:
                # TODO: Could make it try again a couple of times every 5 minutes.
                load_data = await self.pull_with_retries(start, end)
                if load_data.empty:
                    log.warning("No data returned")
                else:
                    load_data = load_data.tail(1)
                    log.info(f"Data retrieved\n {load_data}")
            except Exception as e:
                log.error(f"Error fetching data: {e}")

            if load_data.empty:
                log.warning(f"Couldn't save {load_data}")
            else:
                save_csv("load", self.country_code, load_data)

            await asyncio.sleep(3600)
