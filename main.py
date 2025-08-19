from entsoe.entsoe import EntsoePandasClient
import pandas
import time

from src import config

# Connect to the client using the API key.
client = EntsoePandasClient(api_key=config.API_KEY)


def main():
    while True:
        now = pandas.Timestamp.now(tz=config.TIME_ZONE).floor("h")
        start = now - pandas.Timedelta("1h")
        end = now

        df = client.query_load(config.COUNTRY_CODE, start=start, end=end)
        print(f"Data at {now}:\n", df)

        time.sleep(3600)


if __name__ == "__main__":
    main()
