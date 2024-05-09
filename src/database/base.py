from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.tps import str_200


class Base(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {str_200: String(200)}

    # ====================================|Columns|===================================== #
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
