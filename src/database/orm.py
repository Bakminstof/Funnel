from typing import Any, Sequence

from sqlalchemy import Table, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, noload

from database.models import MessageAudit, User
from database.tps import Status


class DataBase:
    __table__: Any = None

    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ORM obj={self.__table__})"

    async def update(self, instances: list[dict]) -> None:
        stmt = update(self.__table__)
        await self.async_session.execute(stmt, instances)
        await self.async_session.commit()

    async def create(self, instances: list[dict | Table]) -> Any:
        items = [
            self.__table__(**instance) if isinstance(instance, dict) else instance
            for instance in instances
        ]
        self.async_session.add_all(items)
        await self.async_session.commit()
        return items


class UserDatabase(DataBase):
    __table__ = User

    async def get_by_tg_id(
        self,
        tg_id: int,
        options: list | None = None,
    ) -> User | None:
        if options is None:
            options = []

        where = [User.tg_id == tg_id]

        options.extend(
            [
                load_only(
                    User.id,
                    User.tg_id,
                    User.username,
                    User.status,
                ),
                noload(User.msg_audit),
            ],
        )

        stmt = select(User).options(*options).where(*where).limit(1)
        result = await self.async_session.scalar(stmt)
        await self.async_session.commit()
        return result

    async def get_all_alive(
        self,
        options: list | None = None,
        load_msg_audit: bool = False,
    ) -> Sequence[User]:  # todo: Pagination
        if options is None:
            options = []

        where = [User.status == Status.alive]

        if not load_msg_audit:
            options.extend(
                [
                    load_only(
                        User.id,
                        User.tg_id,
                        User.username,
                        User.status,
                    ),
                    noload(User.msg_audit),
                ],
            )

        else:
            options.append(
                load_only(
                    User.id,
                    User.tg_id,
                    User.username,
                    User.status,
                ).joinedload(User.msg_audit, innerjoin=True),
            )

        stmt = select(User).options(*options).where(*where)
        result = await self.async_session.scalars(stmt)
        await self.async_session.commit()
        return result.all()


class MessageAuditDataBase(DataBase):
    __table__ = MessageAudit
