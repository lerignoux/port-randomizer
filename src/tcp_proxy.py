import asyncio
import logging

from .proxy import Proxy


log = logging.getLogger(__name__)


class TcpProxy(Proxy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        log.info(f"Starting tcp proxy on port {self.port}")

    def jump(self):
        log.debug(f"Switching tcp port to {self.port}")

    async def _start_proxy(self):
        raise NotImplementedError()
