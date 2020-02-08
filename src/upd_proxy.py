import asyncio
import logging

from .proxy import Proxy


log = logging.getLogger(__name__)


class UdpProxy(Proxy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        log.info(f"Starting udp proxy on port {self.port}")
        loop = asyncio.get_event_loop()
        self.transport, _ = loop.run_until_complete(self._start_proxy())
        print("Datagram proxy is running...")

    def jump(self):
        log.debug(f"Switching port to port {self.port}")
        loop = asyncio.get_event_loop()
        new_transport, _ = loop.run_until_complete(self._start_proxy())
        self.transport.close()
        self.transport = new_transport

    async def _start_proxy(self):
        loop = asyncio.get_event_loop()
        protocol = ProxyDatagramProtocol((self.dst_addr, self.dst_port))
        return await loop.create_datagram_endpoint(lambda: protocol, local_addr=(self.src_addr, self.src_port))


class ProxyDatagramProtocol(asyncio.DatagramProtocol):
    """
    under MIT license, thanks to VXGMichel: https://gist.github.com/vxgmichel/b2cf8536363275e735c231caef35a5df
    """

    def __init__(self, remote_address):
        self.remote_address = remote_address
        self.remotes = {}
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if addr in self.remotes:
            self.remotes[addr].transport.sendto(data)
            return
        loop = asyncio.get_event_loop()
        self.remotes[addr] = RemoteDatagramProtocol(self, addr, data)
        coro = loop.create_datagram_endpoint(lambda: self.remotes[addr], remote_addr=self.remote_address)
        asyncio.ensure_future(coro)


class RemoteDatagramProtocol(asyncio.DatagramProtocol):

    def __init__(self, proxy, addr, data):
        self.proxy = proxy
        self.addr = addr
        self.data = data
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.data)

    def datagram_received(self, data, _):
        self.proxy.transport.sendto(data, self.addr)

    def connection_lost(self, exc):
        self.proxy.remotes.pop(self.attr)
