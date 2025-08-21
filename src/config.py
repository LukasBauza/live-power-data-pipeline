import getpass

API_KEY = ""
COUNTRY_CODE = "IE"
TIME_ZONE = "Europe/Dublin"
DATA_DIR = "data"
RAW_DIR = f"{DATA_DIR}/raw"
PROCESSED_DIR = f"{DATA_DIR}/processed"


def enter_api():
    API_KEY = getpass.getpass("Please enter your API key: ")
