import tornado

from settings import settings
from urls import url_patterns


class CozyDataIndexer(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
