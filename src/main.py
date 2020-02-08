import argparse
import asyncio
import logging

from .udp_proxy import UdpProxy
from .tcp_proxy import TcpProxy


log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Proxy TCP and UDP traffic from/to a random range of ports.')
parser.add_argument('-s', '--src', dest='src', type=str, required=True, default='127.0.0.1:80',
                    help='Source address:port/range. i.e `127.0.0.1:1443-2443`, lower and higher bounds included if provided.')
parser.add_argument('-d', '--dst', dest='dst', type=str, required=True, default='127.0.0.1:80',
                    help='Destination address:port/range. i.e `127.0.0.1:1443-2443`, lower and higher bounds included.')
parser.add_argument('-f', 'frequency', '--jump_frequency', dest='jump_frequency', required=False, default=1,
                    help='port jump frequency (per hour). default: change port every hour')
parser.add_argument('--seed', dest='output', type=int, required=False, default=0,
                    help='the seed for the randomizer.')


if __name__ == "main":
    args = parser.parse_args()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler()]
    )

    loop = asyncio.get_event_loop()
    udp_proxy = UdpProxy(args.src, args.dst, args.seed, args.jump_frequency)
    udp_proxy.start()
    tcp_proxy = TcpProxy(args.src, args.dst, args.seed, args.jump_frequency)
    tcp_proxy.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()
