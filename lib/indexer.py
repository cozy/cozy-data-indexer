import os

from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, And, Term

from whoosh import index
from whoosh.fields import Schema, ID, KEYWORD, TEXT

from whoosh.support.charset import accent_map
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import CharsetFilter, LowercaseFilter, StopFilter

from lib.stopwords import stoplists

class IndexSchema():
    """
    Init schema and build a custom analyzer.

    All data to index will be put inside the
    """

    def __init__(self):

        chfilter = CharsetFilter(accent_map)
        stoplist = stoplists["en"].union(stoplists["fr"])
        analyzer = RegexTokenizer() | LowercaseFilter() | \
                   StopFilter(stoplist=stoplist) | chfilter

        self.schema = Schema(content=TEXT(analyzer=analyzer),
                             docType=TEXT,
                             docId=ID(stored=True, unique=True),
                             tags=KEYWORD)

        if not os.path.exists("indexes"):
            os.mkdir("indexes")
            self.index = index.create_in("indexes", self.schema)
        else:
            self.index = index.open_dir("indexes")


    def clear_index(self):
        """
        Clear index: whoosh indexe create, create a new index in the directory
        even if an index exists.
        """

        if os.path.exists("indexes"):
            index.create_in("indexes", self.schema)


class Indexer():

    def index_doc(self, docType, doc, fields):
        """
        Add given doc to index, tag and given fields are stored.
        """

        indexSchema = IndexSchema()
        contents = []
        for field in fields:
            data = doc[field]
            if isinstance(data, unicode):
                contents.append(data)
            elif data is not None:
                contents.append(data.decode("utf-8"))

        content = u" ".join(contents)
        writer = indexSchema.index.writer()
        writer.update_document(content=content,
                               docType=unicode(docType),
                               docId=unicode(doc["id"]),
                               tags=doc["tags"])
        writer.commit()


    def search_doc(self, word, docType, numPage=1, numByPage=10):
        """
        Return a list of docs that contains given word and that matches
        given type.
        """

        indexSchema = IndexSchema()
        parser = QueryParser("content", schema=indexSchema.schema,
                termclass=FuzzyTerm)
        query = parser.parse(word)
        query = And([query, Term("docType", unicode(docType.lower()))])

        with indexSchema.index.searcher() as searcher:
            results = searcher.search_page(query, numPage, pagelen=numByPage)
            print [result["docId"] for result in results]
            return [result["docId"] for result in results]


    def remove_doc(self, id):
        """
        Remove given doc from index (doc of which docId is equal to id).
        """

        indexSchema = IndexSchema()
        writer = indexSchema.index.writer()
        writer.delete_by_term("docId", unicode(id))
        writer.commit()

    def remove_all(self):
        '''
        Remove all data from index.
        '''

        indexSchema = IndexSchema()
        indexSchema.clear_index()
