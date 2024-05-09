from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from database.tps import Status, created_at, datetime_utc, status_updated_at, str_200


class User(Base):
    __tablename__ = "user"

    tg_id: Mapped[int] = mapped_column(BIGINT)
    username: Mapped[str_200]
    created_at: Mapped[created_at]
    status: Mapped[Status] = mapped_column(default=Status.alive)
    status_updated_at: Mapped[status_updated_at]

    # ===========================|Message audit relationship|=========================== #
    msg_audit: Mapped[MessageAudit] = relationship(back_populates="user")

    # ===================================|Table args|=================================== #
    __table_args__ = (
        UniqueConstraint(
            "tg_id",
            name=f"{__tablename__}__tg_id__uc",
        ),
        UniqueConstraint(
            "username",
            name=f"{__tablename__}__username__uc",
        ),
    )


class MessageAudit(Base):
    __tablename__ = "message_audit"

    init_msg: Mapped[created_at]
    msg_1_timestamp: Mapped[datetime_utc | None]
    msg_2_timestamp: Mapped[datetime_utc | None]
    msg_3_timestamp: Mapped[datetime_utc | None]

    # ===============================|User relationship|================================ #
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="msg_audit", single_parent=True)
