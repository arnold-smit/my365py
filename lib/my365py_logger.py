"""
my365py_logger.py

This module sets up a loguru logger to be used throughout the application.
Note that the logger is set to write to a file with name set in the module my365py_config.py

Example
-------
Import the same logger throughout the application like this:
from lib.my365py_logger import logger

Then the loguru logger is used like this (as driven by levels):
* logger.trace(): TRACE: 5
* logger.debug(): DEBUG: 10
* logger.info(): INFO: 20
* logger.success(): SUCCESS: 25
* logger.warning(): WARNING: 30
* logger.error(): ERROR: 40
* logger.critical(): CRITICAL: 50
"""

from loguru import logger
from lib.my365py_config import CNF

logger.remove()
logger.add( CNF["LOG_FILE"],
            rotation="1 MB",
            retention=CNF["LOG_RETENTION"],
            compression="zip",
            level=CNF["LOG_LEVEL"],
            format="{time}:{level}:{file}:{line} -> {message}"
          )
