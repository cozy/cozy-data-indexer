#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from settings import settings
from urls import url_patterns

class CozyDataSystem(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)

def main():
    logger = logging.getLogger("")
    logger.info("Cozy Data System started on port %d." % options.port)
    try:
        app = CozyDataSystem()
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
        print ""
        logger.info("Cozy Data System stopped.")

if __name__ == "__main__":
    main()
