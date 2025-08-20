import logging

format = "%(asctime)s %(levelname)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(format=format, datefmt=datefmt)

log = logging.getLogger("entsoe")
