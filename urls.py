from handlers import db

url_patterns = [
    (r"/$", db.VersionHandler),
    (r"/db/exists/$", db.ExistsHandler),
    (r"/db/create/$", db.CreateHandler),
]
