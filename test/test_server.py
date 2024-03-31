from asyncio import get_event_loop
from pynacl_middleware_canonical_example.manager import EngineServerManager, ServerStatus
from pynacl_middleware_canonical_example.config import ServerConfig
from pynacl_middleware_canonical_example.logger import log
from .client import Client

server_config = ServerConfig('./config.json')
esm = EngineServerManager()

async def status_change_listener(status) -> None:
    if status == ServerStatus.Running:
        client = Client(server_config.host, server_config.port, server_config.public_key, True if server_config.ssl else False)
        data = await client.sendMessage({'messageOne': 'testOne'})
        assert data == f'ws{client.protocol()}://'
        await client.connectToWebsocket({'messageTwo': 'testTwo'})
        await client.sendWebSocketMessage({'name': 'Georgia'})
        await client.disconnectWebsocket()
        esm.stop()

async def server_loop_handler() -> None:
    esm.add_listener(status_change_listener)
    esm.start()
    esm.join()
    log.info('Joining main thread...')

def test_middleware() -> None:
    loop = get_event_loop()
    loop.run_until_complete(
        server_loop_handler()
    )
    log.info('Joined!')
