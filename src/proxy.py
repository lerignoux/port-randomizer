import asyncio
import logging
import random
import re


log = logging.getLogger(__name__)


class Proxy:

    def __init__(self, src, dst, seed=0, jump_frequency=1):
        self.random = random.Random(seed)
        self.jumps = 24 * jump_frequency  # port jumps per hour

        src_parsed = re.match('(?P<address>%d):(?P<ports>%d)', src)
        self.src_address = src_parsed.group('address')
        try:
            self.src_port = int(src_parsed.group('ports'))
        except TypeError:
            # A range of port is provided
            self.src_port = None
            self.src_port_range = self.parse_port_range(src_parsed.group('ports'))

        dst_parsed = re.match('(?P<address>%d):(?P<ports>%d)', dst)
        self.dst_address = dst_parsed.group('address')
        try:
            self.dst_port = int(dst_parsed.group('ports'))
        except TypeError:
            # A range of port is provided
            self.dst_port = None
            self.dst_port_range = self.parse_port_range(src_parsed.group('ports'))

    def parse_port_range(self, range_def):
        try:
            ports = re.match('(?P<low>%d)-(?P<high>%d)', range_def)
            return (int(ports.group('low')), int(ports.group('high')))
        except TypeError:
            raise Exception(f"Invalid port range definition: {range_def}")

    @property
    def src_port(self):
        if self.src_port is not None:
            return self.src_port
        else:
            return self.current_port(self.src_port_range)

    def dst_port(self):
        if self.dst_port is not None:
            return self.dst_port
        else:
            return self.current_port(self.dst_port_range)

    def current_port(self, range):
        """
        The port to use right now
        """
        return random.randint(*range)

    def prng(self):
        """
        return a random number depending on the seed and current time
        the actual jump and port generation are based on it
        """
        return 0

    def time_until_jump(self):
        """
        the time before our next jump
        """
        raise NotImplementedError()

    def start(self):
        """
        We start the proxy and jumping cycle
        """
        raise NotImplementedError()

    def jump(self):
        """
        Time to switch port
        """
        raise NotImplementedError()

    async def _start_proxy():
        """
        Actual proxy binding coroutine
        """
        raise NotImplementedError()

    async def check_jump(self):
        """
        It would be more performant to not actively wait
        """
        current = self.prng()
        while 1:
            safe_time = min(0.01, self.time_until_jump() * 0.75)
            await asyncio.sleep(safe_time)
            if self.prng() != current:
                # only one source of truth to ensure everything switch smoothly
                self.jump()
