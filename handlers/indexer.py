from tornado.escape import json_encode

from handlers.base import BaseHandler
from lib.indexer import Indexer

import logging
logger = logging.getLogger('cozy-data-indexer.' + __name__)


class VersionHandler(BaseHandler):
    '''
    Return current version of Data Indexer.
    '''

    def get(self):
        self.write("Cozy Data Indexer v1.0.0")


class IndexHandler(BaseHandler):
    '''
    Index given content for given fields.

    Expected fields:

    * doc: a document with an id and a docType
    * fields: fields to index
    '''

    def post(self):
        '''
        Add given document to index.
        '''

        self.load_json()
        doc = self.get_field("doc")
        fields = self.get_field("fields")

        if not "id" in doc:
            id = doc.get("_id", None)
            if id is None:
                self.raise_argument_error("doc.id")
            else:
                doc["id"] = id
        if not "tags" in doc:
            doc["tags"] = []

        docType = doc.get("docType", None)
        if docType is None:
            self.raise_argument_error("doc.docType")
        if not len(fields):
            self.raise_argument_error("fields")
        else:
            indexer = Indexer()
            indexer.index_doc(docType, doc, fields)
            self.write("indexation succeeds")

    def delete(self, id):
        """
        Remove document that matches id from index.
        """

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
        '''
        Perform search query.
        '''
        self.load_json()
        query = self.get_field('query')
        docTypes = self.get_field('docType', [])

        # For backward compatibility, it accepts a single string
        # but turn it into an array
        if isinstance(docTypes, basestring):
            docTypes = [docTypes]

        numPage = int(self.get_field('numPage', 1))
        numByPage = int(self.get_field('numByPage', 10))

        indexer = Indexer()
        result = indexer.search_doc(query, docTypes, numPage, numByPage)
        self.write(json_encode({ 'ids': result }))


class ClearHandler(BaseHandler):
    '''
    Remove all data from index.
    '''

    def delete(self):
        indexer = Indexer()
        indexer.remove_all()
        self.write('deletion succeeds')
