from tornado.web import HTTPError
from tornado.escape import json_encode
from whoosh.writing import IndexingError

from handlers.base import BaseHandler
from lib.indexer import Indexer


import logging
logger = logging.getLogger('cozy-data-system.' + __name__)

class VersionHandler(BaseHandler):
    '''
    Return current version of Data system.
    '''

    def get(self):
        self.write("Cozy Data System v0.1.0")


class IndexHandler(BaseHandler):
    '''
    Index given content for given fields. 
    
    Expected fields:

    * doc: a document with an id and a docType
    * fields: fields to index
    '''

    def post(self):
        self.load_json()
        doc = self.get_field("doc")
        fields = self.get_field("fields")

        id = doc.get("id", None)
        docType = doc.get("docType", None)

        if id is None:
            self.raise_argument_error("doc.id")
        elif docType is None:
            self.raise_argument_error("doc.docType")
        if not len(fields):
            self.raise_argument_error("fields")
        else:
            indexer = Indexer()
            indexer.index_doc(docType, doc, fields)
            self.write("indexation succeeds")

    def delete(self, id):
        indexer = Indexer()
        indexer.remove_doc(unicode(id))
        self.set_status(204)
        self.write("index deletion succeeds")



class SearchHandler(BaseHandler):
    '''
    Returns a list of ids that matches document results of given query search.

    Expected fields:

    * query: the search query string 
    * docType: the type of document to look for 
    '''

    def post(self):
        self.load_json()
        query = self.get_field("query")
        docType = self.get_field("docType")

        indexer = Indexer()
        result = indexer.search_doc(query, docType)
        self.write(json_encode({ "ids": result }))
