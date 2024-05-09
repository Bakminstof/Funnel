from asyncio import get_running_loop, sleep
from datetime import UTC, datetime, timedelta
from logging import getLogger
from re import search
from typing import Sequence

from pyrogram import Client

from core.settings import settings
from core.utils import send_mes
from database.models import User
from database.orm import MessageAuditDataBase, UserDatabase
from database.tps import Status
from database.utils import get_msg_audit_db, get_user_db

logger = getLogger(__name__)


class Funnel:
    __started = False

    def __init__(self, app: Client) -> None:
        self.app = app

    async def check_trigger(
        self,
        client: Client,
        user: User,
        limit_ch_msgs: int = 100,
    ) -> bool:
        async for msg in client.get_chat_history(user.tg_id, limit=limit_ch_msgs):
            if search("прекрасно|ожидать", msg.text.lower()):
                await self.exclude_user(user)
                return True

        return False

    @classmethod
    async def exclude_user(cls, user: User) -> None:
        async with get_user_db() as user_db:  # type: UserDatabase
            await user_db.update([{"id": user.id, "status": Status.finished}])

    @classmethod
    async def _get_alive_users(cls) -> Sequence[User]:
        async with get_user_db() as user_db:  # type: UserDatabase
            return await user_db.get_all_alive(load_msg_audit=True)

    async def send_1(self, user: User, chat_id: int) -> None:
        if await self.check_trigger(self.app, user):
            return

        check_send = await send_mes(self.app, user, chat_id, settings.msg1)
        if not check_send:
            return

        async with get_msg_audit_db() as msg_audit_db:  # type: MessageAuditDataBase
            await msg_audit_db.update(
                [{"id": user.msg_audit.id, "msg_1_timestamp": datetime.now(UTC)}],
            )

    async def send_2(self, user: User, chat_id: int) -> None:
        if await self.check_trigger(self.app, user):
            return

        check_send = await send_mes(self.app, user, chat_id, settings.msg2)
        if not check_send:
            return

        async with get_msg_audit_db() as msg_audit_db:  # type: MessageAuditDataBase
            await msg_audit_db.update(
                [{"id": user.msg_audit.id, "msg_2_timestamp": datetime.now(UTC)}],
            )

    async def send_3(self, user: User, chat_id: int) -> None:
        if await self.check_trigger(self.app, user):
            return

        check_send = await send_mes(self.app, user, chat_id, settings.msg3)
        if not check_send:
            return

        async with get_msg_audit_db() as msg_audit_db:  # type: MessageAuditDataBase
            await msg_audit_db.update(
                [{"id": user.msg_audit.id, "msg_3_timestamp": datetime.now(UTC)}],
            )

        await self.exclude_user(user)

    def __check_for_msg1(
        self,
        user: User,
        current_timestamp: datetime,
        delay: int = 360,
    ) -> bool:
        return (
            not user.msg_audit.msg_1_timestamp
            and user.msg_audit.init_msg + timedelta(seconds=delay) < current_timestamp
        )

    def __check_for_msg2(
        self,
        user: User,
        current_timestamp: datetime,
        delay: int = 2340,
    ) -> bool:
        return (
            user.msg_audit.msg_1_timestamp is not None
            and not user.msg_audit.msg_2_timestamp
            and user.msg_audit.msg_1_timestamp + timedelta(seconds=delay)
            < current_timestamp
        )

    def __check_for_msg3(
        self,
        user: User,
        current_timestamp: datetime,
        delay: int = 93600,
    ) -> bool:
        return (
            user.msg_audit.msg_2_timestamp is not None
            and not user.msg_audit.msg_3_timestamp
            and user.msg_audit.msg_2_timestamp + timedelta(seconds=delay)
            < current_timestamp
        )

    async def __timer(self, delay: int) -> None:
        counter = 0

        while self.__started:
            if counter == delay:
                break

            counter += 1

            await sleep(1)

    async def start(self, period: int = 10) -> None:
        self.__started = True

        loop = get_running_loop()

        logger.info("Funnel started")

        while self.__started:
            current_timestamp = datetime.now(UTC)

            for user in await self._get_alive_users():
                if self.__check_for_msg1(user, current_timestamp):
                    loop.create_task(self.send_1(user, user.tg_id))

                if self.__check_for_msg2(user, current_timestamp):
                    loop.create_task(self.send_2(user, user.tg_id))

                if self.__check_for_msg3(user, current_timestamp):
                    loop.create_task(self.send_3(user, user.tg_id))

            await self.__timer(period)

    async def stop(self) -> None:
        self.__started = False

        logger.info("Funnel stopped")
