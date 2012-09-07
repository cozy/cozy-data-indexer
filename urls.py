from handlers import indexer

url_patterns = [
    (r"/$", indexer.VersionHandler),
    (r"/index/$", indexer.IndexHandler),
    (r"/index/(.*)/$", indexer.IndexHandler),
    (r"/search/$", indexer.SearchHandler),
    (r"/clear-all/$", indexer.ClearHandler),
]
