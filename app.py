import tornado
import os

from settings import settings
from urls import url_patterns

from whoosh import index
from whoosh.fields import Schema, ID, KEYWORD, TEXT

class CozyDataSystem(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)

        self.schema = Schema(content=TEXT, 
                        docType=TEXT, 
                        docId=ID(stored=True), 
                        tags=KEYWORD)

        if not os.path.exists("indexes"):
            os.mkdir("indexes")
            self.index = index.create_in("indexes", self.schema)
        else:
            self.index = index.open_dir("indexes")
