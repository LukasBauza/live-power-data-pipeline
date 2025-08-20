import asyncio
import logging
from entsoe.entsoe import EntsoePandasClient
import pandas

from src.logging import log


class LoadPuller:
    def __init__(self, api_key: str, start: str, end: str, country_code: str):
        self.client: EntsoePandasClient = EntsoePandasClient(api_key=api_key)
        self.start: str = start
        self.end: str = end
        self.country_code: str = country_code
