from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from handlers.simple.utils import get_user


async def msg_handler(client: Client, message: Message) -> None:
    user = await get_user(message.from_user)


simple_handler = MessageHandler(msg_handler)
