import os

from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import FuzzyTerm, And, Term, Or

from whoosh import index
from whoosh.fields import Schema, ID, KEYWORD, TEXT

from whoosh.support.charset import accent_map
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import CharsetFilter, LowercaseFilter, StopFilter

from lib.stopwords import stoplists


class CustomFuzzyTerm(FuzzyTerm):
    """
    Custom FuzzyTerm query parser to set a custom maxdist
    """

    def __init__(self, fieldname, text, boost=1.0, maxdist=1):
        FuzzyTerm.__init__(self, fieldname, text, 1.0, 2)


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

        # defines the schema
        # see http://pythonhosted.org/Whoosh/schema.html for reference
        self.schema = Schema(content=TEXT(analyzer=analyzer),
                             docType=TEXT,
                             docId=ID(stored=True, unique=True),
                             tags=KEYWORD(lowercase=True, scorable=True))

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

        # Since we can't know what fields the document is going to have
        # we can't use a custom index schema so we put all indexed fields
        # into one `content` field.
        contents = []
        for field in fields:
            data = doc[field]
            if isinstance(data, unicode):
                contents.append(data)
            elif data is not None:
                contents.append(data.decode("utf-8"))

        content = u" ".join(contents)

        # Adds the doctype as a tag
        tags = doc["tags"].append(docType)
        tags = u" ".join(doc["tags"][0::1])

        writer = indexSchema.index.writer()
        writer.update_document(content=content,
                               docType=unicode(docType),
                               docId=unicode(doc["id"]),
                               tags=doc["tags"])
        writer.commit()


    def search_doc(self, word, docTypes, numPage=1, numByPage=10):
        """
        Return a list of docs that contains given word and that matches
        given type.
        """

        indexSchema = IndexSchema()
        # Creates the query parser.
        # MultifieldParser allows search on multiple fields.
        # We use a custom FuzzyTerm class to set the Levenstein distance to 2
        parser = MultifieldParser(["content", "tags"], schema=indexSchema.schema,
                termclass=CustomFuzzyTerm)
        query = parser.parse(word)

        # Creates a filter on the doctype field
        doctypeFilterMatcher = []
        for docType in docTypes:
            term = FuzzyTerm("docType", unicode(docType.lower()), 1.0, 2)
            doctypeFilterMatcher.append(term)

        docTypeFilter = Or(doctypeFilterMatcher)

        # Processes the search (request the index, Whoosh magic)
        with indexSchema.index.searcher() as searcher:
            results = searcher.search_page(query, numPage, pagelen=numByPage,
                                                        filter=docTypeFilter)
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
