import signal
from asyncio import get_running_loop, sleep
from logging import getLogger
from threading import Event
from types import FrameType

from pyrogram import Client

from core.funnel import Funnel
from core.settings import settings
from core.utils import setup_logging
from database.utils import db, set_triggers
from handlers.simple.handler import simple_handler

logger = getLogger(__name__)


class Lifespan:
    stop_event = Event()

    def __init__(self, app: Client) -> None:
        self.app = app
        self.funnel = Funnel(self.app)

    @classmethod
    def __sigint_handler(cls, sig: int, frame: FrameType) -> None:
        cls.stop_event.set()

        logger.warning("Received signal SIGINT. Grateful stopping...")

    async def on_startup(self) -> None:
        loop = get_running_loop()

        # ==================================|Logging|=================================== #
        setup_logging()

        # ==================================|Database|================================== #
        await db.init(engine_url=settings.db.url, echo_sql=settings.db.echo_sql)
        await set_triggers()

        # ==============================|Main application|============================== #
        signal.signal(signal.SIGINT, self.__sigint_handler)
        self.app.add_handler(simple_handler)
        loop.create_task(self.funnel.start())

        logger.info('Startup: app="%s"', settings.name)

    async def on_shutdown(self) -> None:
        await self.funnel.stop()
        await db.close()

        logger.info('Shutdown: app="%s"', settings.name)

    async def start(self) -> None:
        async with self.app:
            await self.on_startup()

            while not self.stop_event.is_set():
                await sleep(1)

            await self.on_shutdown()
