from dataclasses import dataclass, field
from functools import cached_property
from os import environ
from pathlib import Path
from typing import Literal

from sqlalchemy import URL

BASE_DIR = Path(__file__).parent.parent


@dataclass
class DBSettings:
    drivername: str = environ["DRIVERNAME"]

    db_user: str = environ["DB_USER"]
    db_password: str = environ["DB_PASSWORD"]

    db_host: str = environ["DB_HOST"]
    db_port: int = int(environ["DB_PORT"])

    db_name: str = environ["DB_NAME"]

    echo_sql: bool = environ["ECHO_SQL"].lower() == "true"

    @cached_property
    def url(self) -> URL:
        return URL.create(
            drivername=self.drivername,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


@dataclass
class LoggingSettings:
    loglevel: Literal[
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    log_format: str = (
        "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | <%(message)s>"
    )

    log_datetime_format: str = "%Y-%m-%d %H:%M:%S"

    dict_conf: dict = field(
        default_factory=lambda: {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "base": {
                    "format": LoggingSettings.log_format,
                    "datefmt": LoggingSettings.log_datetime_format,
                },
                "colour": {
                    "()": "core.formatters.ColourFormatter",
                    "fmt": LoggingSettings.log_format,
                    "datefmt": LoggingSettings.log_datetime_format,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": LoggingSettings.loglevel,
                    "formatter": "colour",
                },
            },
            "root": {
                "level": LoggingSettings.loglevel,
                "handlers": [
                    "console",
                ],
            },
        },
    )


@dataclass
class Settings:
    # ======================================|Main|====================================== #
    name: str = "Telegram-APP-Bck"

    debug: bool = environ.get("DEBUG", "").lower() == "true"

    api_id: int = int(environ["API_ID"])
    api_hash: str = environ["API_HASH"]

    phone_number: str = environ["PHONE_NUMBER"]

    session_dir: Path = BASE_DIR / "session"

    # ====================================|Messages|==================================== #
    msg1: str = environ["MSG1"]
    msg2: str = environ["MSG2"]
    msg3: str = environ["MSG3"]

    # ====================================|Database|==================================== #
    db: DBSettings = field(default_factory=lambda: DBSettings())

    # ====================================|Logging|===================================== #
    logging: LoggingSettings = field(default_factory=lambda: LoggingSettings())


settings = Settings()
