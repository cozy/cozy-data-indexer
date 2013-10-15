import logging

from weboob.core.modules import ModuleLoadError
from weboob.tools.browser import BrowserIncorrectPassword

from handlers.base import BaseHandler
from lib.connector import Connector

logger = logging.getLogger('cozy-data-indexer.' + __name__)


class BaseBankHandler(BaseHandler):
    '''
    Base class to handle utility methods.
    '''

    def load_from_connector(self, name, method_name):
        '''
        Load given connector (name) and apply the given method on it.
        Supported method: get_accounts and get_history.
        '''
        self.load_json()
        login = self.get_field("login")
        password = self.get_field("password")

        try:
            connector = Connector(name, {'login': login, 'password': password})
            results = {}
            callback = getattr(connector, method_name)
            results[name] = callback()
        except ModuleLoadError:
            self.raise_error("Could not load module: %s" % name)
        except BrowserIncorrectPassword:
            self.raise_error("Wrong credentials")

        return results


class BankHandler(BaseBankHandler):
    """
    This handler is dedicated to retrieve data from bank accounts.
    """

    def post(self, name):
        """
        Grab data about all accounts from a given bank identifier.

        Bank type is given as URL parameter, credentials are given in body.
        For available bank type check: http://weboob.org/modules
        """

        self.return_json(self.load_from_connector(name, 'get_balances'))

class BankHistoryHandler(BaseBankHandler):
    """
    This handler is dedicated to retrieve transaction history of bank accounts.
    """


    def post(self, name):
        """
        Grab history of all accounts from a given bank identifier.

        Bank type is given as URL parameter, credentials are given in body.
        For available bank type check: http://weboob.org/modules
        """
        self.return_json(self.load_from_connector(name, 'get_history'))

