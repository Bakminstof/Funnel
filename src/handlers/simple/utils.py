from pyrogram.types import User as PyroUser

from database.models import MessageAudit, User
from database.orm import UserDatabase
from database.utils import get_user_db


async def get_user(from_user: PyroUser) -> User:
    async with get_user_db() as user_db:  # type: UserDatabase
        user = await user_db.get_by_tg_id(from_user.id)

    if user is None:
        user = User(tg_id=from_user.id, username=from_user.username)
        user.msg_audit = MessageAudit()

        async with get_user_db() as user_db:  # type: UserDatabase
            await user_db.create([user])  # type: ignore

    return user
