import asyncio

from src.pull import LoadPuller
from src.config import COUNTRY_CODE, TIME_ZONE, enter_api


def main():
    enter_api()

    dublin_load_puller = LoadPuller(COUNTRY_CODE, TIME_ZONE)
    asyncio.run(dublin_load_puller.hourly_pull())


if __name__ == "__main__":
    main()
