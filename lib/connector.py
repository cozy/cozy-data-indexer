from weboob.core import Weboob

class Connector():

    def __init__(self, connector, parameters):
         weboob = Weboob()
         self.backend = weboob.build_backend(connector, parameters)

    def get_results(self):
        results = []
        for account in self.backend.iter_accounts():
            results.append({ 
                "label": account.label, 
                "balance": unicode(account.balance)
            })
        return results
