import uvloop
from pyrogram import Client

from core.lifespan import Lifespan
from core.settings import settings

uvloop.install()

app = Client(
    settings.name,
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    phone_number=settings.phone_number,
    workdir=settings.session_dir.absolute().as_posix(),
)


async def main() -> None:
    lifespan = Lifespan(app)
    await lifespan.start()


if __name__ == "__main__":
    app.run(main())
