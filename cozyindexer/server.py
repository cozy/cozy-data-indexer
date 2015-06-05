#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
import os
from tornado.options import options

current_directory = os.path.dirname(os.path.realpath(__file__))
for target_path in [current_directory,
                    os.path.join(current_directory, 'cozyindexer')]:
    if os.path.exists(target_path):
        if target_path not in sys.path:
            sys.path.insert(0, target_path)

from app import CozyDataIndexer

app = CozyDataIndexer()


def main():
    logger = logging.getLogger("")
    logger.info("Cozy Data Indexer started on port %d." % options.port)
    try:
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port, address=os.getenv('HOST',
                                                           '127.0.0.1'))
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        print ""
        logger.info("Cozy Data Indexer stopped.")

if __name__ == "__main__":
    main()
