import logging
import os
from logging.handlers import RotatingFileHandler


PROJECT_HOME = "/home/tijay/Projects/ProjectAtlas"
LOG_DIR = os.path.join(PROJECT_HOME, "logs")

os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Persistent log file
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "projectatlas.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
