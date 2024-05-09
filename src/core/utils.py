from logging import getLogger
from logging.config import dictConfig
from warnings import warn

from pyrogram import Client
from pyrogram.errors import UserIsBlocked, InputUserDeactivated, NotAcceptable

from core.settings import settings
from database.models import User
from database.orm import UserDatabase
from database.tps import Status
from database.utils import get_user_db

logger = getLogger(__name__)


def setup_logging() -> None:
    dictConfig(settings.logging.dict_conf)

    if settings.debug:
        msg = "Debug mode on"
        logger.warning(msg)
        warn(UserWarning(msg))


async def send_mes(app: Client, user: User, chat_id: int, text: str) -> bool:
    try:
        await app.send_message(chat_id, text)
        return True

    except (UserIsBlocked, InputUserDeactivated, NotAcceptable):
        async with get_user_db() as user_db:  # type: UserDatabase
            await user_db.update([{"id": user.id, "status": Status.dead}])

        return False
