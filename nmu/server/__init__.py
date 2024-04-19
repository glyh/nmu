import asyncio
from nmu.config import Config
from nmu.server.base import QuitableServer
from nmu.server.service import NeteaseService

async def run():
    conf = Config()
    server = QuitableServer((conf.server_address, conf.server_port))
    server.register_instance(await NeteaseService(server))
    server.serve_til_quit()
    print("Gracefully shutting down...")

def run_sync() -> None:
    asyncio.run(run())
