#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from app import CozyDataSystem

app = CozyDataSystem()

def main():
    logger = logging.getLogger("")
    logger.info("Cozy Data System started on port %d." % options.port)
    try:
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port, address="127.0.0.1")
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        print ""
        logger.info("Cozy Data System stopped.")

if __name__ == "__main__":
    main()
