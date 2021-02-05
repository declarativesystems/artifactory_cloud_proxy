import os
import validators
import sys
from loguru import logger

ARTIFACTORY_URL = "ARTIFACTORY_URL"
CHUNK_SIZE = "CHUNK_SIZE"


def setup_logging(level, logger_name=None):
    logger_name = logger_name or __name__.split(".")[0]

    logger.add(sys.stdout, format="{time} {level} {message}", filter=logger_name, level=level)
    logger.debug("====[debug mode enabled]====")


def get_config():
    setup_logging("DEBUG")
    config = {
        ARTIFACTORY_URL: os.environ.get(ARTIFACTORY_URL, ""),
        #"https://declarativesystems.jfrog.io/artifactory/"
        CHUNK_SIZE: 1024,
    }

    if not validators.url(config[ARTIFACTORY_URL]):
        raise RuntimeError(f"missing or invalid Artifactory URL in environment variable ARTIFACTORY_URL: {config['artifactory_url']}")

    return config
