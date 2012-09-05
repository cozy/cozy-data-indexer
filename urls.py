from handlers import db

url_patterns = [
    (r"/$", db.VersionHandler),
]
