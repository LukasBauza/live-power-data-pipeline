from entsoe.entsoe import EntsoePandasClient
import pandas

# Connect to the client using the API key.
# TODO: Check if this is the best way to use the api key.
client = EntsoePandasClient(api_key="944ec6ae-94a0-4508-9198-d85bd9d09cdc")

start = pandas.Timestamp("2025-08-17", tz="Europe/Dublin")
end = pandas.Timestamp("2025-08-18", tz="Europe/Dublin")
country_code = "IE"

out = client.query_load(country_code, start=start, end=end)

print(out)
