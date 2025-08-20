import asyncio
from entsoe.entsoe import EntsoePandasClient
import pandas

from .config import API_KEY
from .logger import log


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

    async def hourly_pull(self):
        while True:
            # Make sure that it is at the current hour, minutes not needed
            end = pandas.Timestamp.now(tz=self.time_zone).floor("h")
            start = end - pandas.Timedelta(hours=1)

            log.info(f"Pulling load data for {start} to {end} at {self.country_code}")
            try:
                load_data = await self.pull_load_data_async(start, end)
                if load_data.empty:
                    log.warning("No data returned")
                else:
                    log.info("Data retrieved")
                    print(load_data)
            except Exception as e:
                log.error(f"Error fetching data: {e}")

            await asyncio.sleep(3600)
