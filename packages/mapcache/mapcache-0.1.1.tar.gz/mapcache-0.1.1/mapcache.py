#!/usr/bin/env python3
'''Simple caching server. Forwards calls to
http://<server-address>/<external-server>/... to
http://<external-server>/... and caches the result locally.
Later requests to the same address will be served from cache.
'''

__version__ = '0.1.1'

import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from hashlib import sha256
from urllib.request import urlopen


class FilesInFolderCache:
    def __init__(self, folder='.', logger=None):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)
        self.logger = logger or logging.getLogger(__name__)

    def __getitem__(self, path):
        key = sha256(path.encode('UTF8'))
        cache_filename = os.path.join(self.folder, key.hexdigest())
        if os.path.exists(cache_filename):
            self.logger.info('{} available in cache'.format(path))
            with open(cache_filename, 'rb') as f:
                return f.read()
        else:
            self.logger.info('{} missing in cache'.format(path))
            url = 'http:/{}'.format(path)
            try:
                with urlopen(url) as f:
                    data = f.read()
            except Exception as e:
                self.logger.error('Could not retrieve {}'.format(url))
                raise e
            with open(cache_filename, 'wb') as f:
                f.write(data)
            return data


class CacheHandler(BaseHTTPRequestHandler):
    def __init__(self, cache, *args, **kwargs):
        self.cache = cache
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            data = self.cache[self.path]
        except Exception as e:
            self.send_error(404)
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(data)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--folder',
                        help='folder for storing cache files, \
                              defaults to ./cache',
                        default='./cache',
                        required=False)
    parser.add_argument('-i', '--interface',
                        help='network interface to listen on, \
                              defaults to localhost',
                        default='localhost',
                        required=False)
    parser.add_argument('-p', '--port',
                        help='server port, defaults to 8000',
                        default=8000, type=int, required=False)

    args = parser.parse_args()
    server_address = (args.interface, args.port)
    logger = logging.getLogger('mapcache')
    logger.level = logging.DEBUG
    cache = FilesInFolderCache(folder=args.folder, logger=logger)

    def create_handler(*args, **kwargs):
        return CacheHandler(cache, *args, **kwargs)

    httpd = HTTPServer(server_address, create_handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
