import asyncio
import getpass

from src.pull import LoadPuller
from src.config import COUNTRY_CODE, TIME_ZONE, enter_api


def main():
    api_key = getpass.getpass("Please enter your API key: ")

    dublin_load_puller = LoadPuller(COUNTRY_CODE, TIME_ZONE, api_key)
    asyncio.run(dublin_load_puller.hourly_pull())


if __name__ == "__main__":
    main()
