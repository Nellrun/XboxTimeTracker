import logging
import sys

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
