from handlers import indexer
from handlers import connectors

url_patterns = [
    (r"/$", indexer.VersionHandler),
    (r"/index/$", indexer.IndexHandler),
    (r"/index/(.*)/$", indexer.IndexHandler),
    (r"/search/$", indexer.SearchHandler),
    (r"/connectors/bank/([0-9a-z]+)/$", connectors.BankHandler),
    (r"/clear-all/$", indexer.ClearHandler),
]
