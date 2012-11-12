import logging

from weboob.core.modules import ModuleLoadError
from weboob.tools.browser import BrowserIncorrectPassword

from handlers.base import BaseHandler
from lib.connector import Connector

logger = logging.getLogger('cozy-data-indexer.' + __name__)


class BankHandler(BaseHandler):
    """
    This handler is dedicated to retrieve data from bank accounts.
    """

    def post(self, name):
        """
        Grab data from a given bank account.

        Bank type is given as URL parameter, credentials are given in body.
        """

        self.load_json()
        login = self.get_field("login")
        password = self.get_field("password")

        try:
            connector = Connector(name, {'login': login, 'password': password})
            results = {}
            results[name] = connector.get_results()
        except ModuleLoadError:
            self.raise_error("Could not load module: %s" % name)
        except BrowserIncorrectPassword:
            self.raise_error("Wrong credentials")

        self.return_json(results)
