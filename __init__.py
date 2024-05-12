"""Main Package."""

import logging
import sys

# Set up logging configuration
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format=LOGGER_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"
)

# Get the logger instance
logger = logging.getLogger(__name__)
