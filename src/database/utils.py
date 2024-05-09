from contextlib import AbstractAsyncContextManager, asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from database.helper import AsyncDatabase
from database.models import User
from database.orm import MessageAuditDataBase, UserDatabase
from database.triggers import create_on_update_trigger, create_on_update_trigger_func

db = AsyncDatabase()


@asynccontextmanager
async def get_async_session() -> AbstractAsyncContextManager[AsyncSession]:
    async with db.session() as async_session:  # type: AsyncSession
        yield async_session


@asynccontextmanager
async def get_user_db() -> AbstractAsyncContextManager[UserDatabase]:
    async with get_async_session() as async_session:  # type: AsyncSession
        yield UserDatabase(async_session)


@asynccontextmanager
async def get_msg_audit_db() -> AbstractAsyncContextManager[MessageAuditDataBase]:
    async with get_async_session() as async_session:  # type: AsyncSession
        yield MessageAuditDataBase(async_session)


async def set_triggers() -> None:
    async with get_async_session() as async_session:  # type: AsyncSession
        table = User.__tablename__
        trigger_func = create_on_update_trigger_func(table)

        await async_session.execute(trigger_func[1])
        await async_session.execute(
            create_on_update_trigger(table, func_name=trigger_func[0]),
        )
        await async_session.commit()
