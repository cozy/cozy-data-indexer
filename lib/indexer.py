import os

from whoosh.qparser import QueryParser
from whoosh.query import Variations

from whoosh import index
from whoosh.fields import Schema, ID, KEYWORD, TEXT


class IndexSchema():

    def __init__(self):
        self.schema = Schema(content=TEXT, 
                        docType=TEXT, 
                        docId=ID(stored=True), 
                        tags=KEYWORD)

        if not os.path.exists("indexes"):
            os.mkdir("indexes")
            self.index = index.create_in("indexes", self.schema)
        else:
            self.index = index.open_dir("indexes")



class Indexer():

    def index_doc(self, docType, doc, fields):
        """
        Add given doc to index, tag and given fields are stored.
        """

        indexSchema = IndexSchema()
        content = " ".join([doc[field] for field in fields])
        writer = indexSchema.index.writer()
        writer.update_document(content=unicode(content),
                                    docType=unicode(docType),
                                    docId=unicode(doc["id"]),
                                    tags=doc["tags"])
        writer.commit()


    def search_doc(self, word, docType):
        """
        Return a list of docs that contains given word.
        """

        indexSchema = IndexSchema()
        parser = QueryParser("content", schema=indexSchema.schema, 
                             termclass=Variations)
        query = parser.parse(word)

        with indexSchema.index.searcher() as searcher:
            results = searcher.search(query)
            return [result["docId"] for result in results]
        
    def remove_doc(self, id):
        """
        Remove given doc from index (doc of which docId is equal to id).
        """

        indexSchema = IndexSchema()

        writer = indexSchema.index.writer()
        writer.delete_by_term("docId", unicode(id))
        writer.commit()
