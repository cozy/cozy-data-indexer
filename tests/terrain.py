import logging
import sys

import tornado.ioloop
import tornado.httpserver
import tornado.ioloop
import tornado.web

from threading import Thread
from lettuce import before, after, world




class Server(Thread):
    def __init__(self, app):
        self.http = tornado.httpserver.HTTPServer(app)
        Thread.__init__(self)

    def run(self):
        logger = logging.getLogger("")
        logger.info("Cozy Data System started on port 8888.")
        try:
            self.http.listen(8888)
            tornado.ioloop.IOLoop.instance().start()

        except KeyboardInterrupt:
            self.http.stop()
            tornado.ioloop.IOLoop.instance().stop()
            print ""
            logger.info("Cozy Data System stopped.")

@before.all
def run_server():
    sys.path.append("../")
    sys.path.append("../venv/lib/python2.7/site-packages/")
    from app import CozyDataSystem
    app = CozyDataSystem()
    world.server = Server(app)
    try:
        world.server.start()
        
    except KeyboardInterrupt:
        world.server.http.stop()
        tornado.ioloop.IOLoop.instance().stop()

@after.all
def kill_server(total):

    logger = logging.getLogger("")
    logger.info("Stop server.")

    world.server.http.stop()
    tornado.ioloop.IOLoop.instance().stop()

