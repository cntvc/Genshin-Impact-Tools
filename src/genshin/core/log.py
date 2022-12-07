"""log"""
import sys

from loguru import logger

from genshin.config import settings

config = {
    # format DOC：https://loguru.readthedocs.io/en/stable/api/logger.html#record
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{message}</level>",
            "level": "INFO",
            "colorize": True,
        },
        {
            "sink": settings.APP_LOG_PATH,
            "format": (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level}"
                " | {file}:{line} | {function}() | message:   {message}"
            ),
            "level": "DEBUG",
        },
    ],
}

logger.configure(**config)
