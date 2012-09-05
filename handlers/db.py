from handlers.base import BaseHandler

import logging
logger = logging.getLogger('cozy-data-system.' + __name__)

class VersionHandler(BaseHandler):
    '''
    Return current version of Data system.
    '''

    def get(self):
        self.write("Cozy Data System v0.1.0")

