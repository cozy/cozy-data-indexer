from whoosh.qparser import QueryParser
from whoosh.query import Variations
from server import app

class Indexer():

    def index_doc(self, docType, doc, fields):
        """
        Add given doc to index, tag and given fields are stored.
        """

        content = " ".join([doc[field] for field in fields])
        self.writer = app.index.writer()
        self.writer.update_document(content=unicode(content),
                                    docType=unicode(docType),
                                    docId=unicode(doc["id"]),
                                    tags=doc["tags"])
        self.writer.commit()


    def search_doc(self, word):
        """
        Return a list of docs that contains given word.
        """

        parser = QueryParser("content", schema=app.schema, termclass=Variations)
        query = parser.parse(word)

        with app.index.searcher() as searcher:
            results = searcher.search(query)
            return [result["docId"] for result in results]
