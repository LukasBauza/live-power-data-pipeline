from entsoe.entsoe import EntsoePandasClient
import pandas
import time

# Connect to the client using the API key.
client = EntsoePandasClient(api_key="944ec6ae-94a0-4508-9198-d85bd9d09cdc")

# NOTE: Optional parameters available only for Outages.
start = pandas.Timestamp("2026-08-17", tz="Europe/Dublin")
end = pandas.Timestamp("2026-08-18", tz="Europe/Dublin")
country_code = "IE"


def main():
    while True:
        now = pandas.Timestamp.now(tz="Europe/Dublin").floor("h")
        start = now - pandas.Timedelta("1h")
        end = now

        df = client.query_load("IE", start=start, end=end)
        print(f"Data at {now}:\n", df)

        time.sleep(3600)


if __name__ == "__main__":
    main()
