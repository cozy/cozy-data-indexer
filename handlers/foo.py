from handlers.base import BaseHandler

import logging
logger = logging.getLogger('cozy-data-system.' + __name__)


class FooHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")
