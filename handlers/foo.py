from handlers.base import BaseHandler

import logging
logger = logging.getLogger('cozy-data-system.' + __name__)

class FooHandler(BaseHandler):
    def get(self):
        self.write("Cozy Data System v0.1.0")

class ExistsHandler(BaseHandler):

    
    @tornado.web.asynchronous
    def post(self):
        dataType = self.get_field("dataType")
        _id = self.get_field("id")
        self.db.__getattr__(dataType).{'_id': _id}, limit=1, callback=self._on_response)


    def _on_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)
        self.writeok("ok")
        self.finish()
