import argparse

from aiohttp import web
from prometheus_client.core import REGISTRY

from cloudflare_exporter.config import DEFAULT_HOST, DEFAULT_PORT
from cloudflare_exporter.handlers import (handle_metrics,
                                          handle_health)
from cloudflare_exporter.collector import CloudflareCollector


def parse_args():
    parser = argparse.ArgumentParser(description='Cloudfalre prometheus exporter')
    parser.add_argument('-t', '--token', type=str, required=True,
                        help='Cloudflare API Token')
    parser.add_argument('--host', type=str,
                        help='TCP/IP host for HTTP server',
                        default=DEFAULT_HOST)
    parser.add_argument('--port', type=int,
                        help="Port used to expose metrics for Prometheus",
                        default=DEFAULT_PORT)
    return parser.parse_args()


def main():
    args = parse_args()
    REGISTRY.register(CloudflareCollector(cloudflare_token=args.token))
    app = web.Application()
    app.router.add_get('/metrics', handle_metrics)
    app.router.add_get('/health', handle_health)
    web.run_app(app, host=args.host, port=args.port, access_log=None)


if __name__ == '__main__':
    main()
