from weboob.core import WebNip


class Connector():
    '''
    Connector is a tool that connects to common websites like bank website,
    phone operator website... and that grabs personal data from there.
    Credentials are required to make this operation.

    Technically, connectors are weboob backend wrappers.
    '''

    def __init__(self, connector, parameters):
        '''
        Constructor: initialize connector, set up the weboob backend.
        '''
        weboob = WebNip()
        self.backend = weboob.build_backend(connector, parameters)

    def get_results(self):
        '''
        Grab results returned by connector after activation.

        Issue: connectors are blocking, they should not.
        '''
        results = []
        for account in self.backend.iter_accounts():
            results.append({
                "label": account.label,
                "balance": unicode(account.balance)
            })
        return results
