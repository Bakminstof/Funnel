from datetime import datetime
from enum import StrEnum, auto
from typing import Annotated

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import mapped_column

# =====================================|Annotated|====================================== #
created_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    ),
]

status_updated_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    ),
]

datetime_utc = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
    ),
]

str_200 = Annotated[str, 200]


# ========================================|Enum|======================================== #
class Status(StrEnum):
    alive = auto()
    dead = auto()
    finished = auto()
