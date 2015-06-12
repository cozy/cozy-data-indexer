import os

import json
from dateutil.parser import parse as stringToDate
from distutils.util import strtobool

from whoosh.qparser import MultifieldParser
from whoosh.query import FuzzyTerm, Or

from whoosh import index
from whoosh.fields import Schema, ID, KEYWORD, TEXT, DATETIME, NUMERIC, BOOLEAN

from whoosh.support.charset import accent_map
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import CharsetFilter, LowercaseFilter, StopFilter

from lib.stopwords import stoplists

import logging
logger = logging.getLogger('cozy-data-indexer.' + __name__)


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
        keywordType = KEYWORD(lowercase=True, scorable=True)
        self.schema = Schema(content=TEXT(analyzer=analyzer),
                             docType=TEXT,
                             docId=ID(stored=True, unique=True),
                             tags=keywordType)

        # Adds dynamic fields so each documents can index its fields in the
        # same Whoosh index
        self.schema.add('*_string', TEXT(analyzer=analyzer), glob=True)
        self.schema.add('*_date', DATETIME, glob=True)
        self.schema.add('*_number', NUMERIC, glob=True)
        self.schema.add('*_boolean', BOOLEAN, glob=True)

        # Creates the index folder and Whoosh index files if it doesn't exist
        # And loads the index in any case
        if not os.path.exists("indexes"):
            os.mkdir("indexes")
            self.index = index.create_in("indexes", self.schema)
        else:
            self.index = index.open_dir("indexes")

        # Creates the doctypes folder if it doesn't exist
        if not os.path.exists("doctypes"):
            os.mkdir("doctypes")

        # Creates the doctypes default schema file if it doesn't exist
        if not os.path.exists('doctypes/doctypes_schema.json'):
            with open('doctypes/doctypes_schema.json', 'w') as defaultFile:
                defaultFile.write("{}")

        '''
        Loads the doctypes schema if it's valid, otherwise recreates it
        Doctypes schema is a dictionary of doctypes with their fields created
        and updated when a document is indexed.
        That way, we can tell Whoosh which fields to search by default, because
        there is apparently no way to say "search in all fields".
        '''
        with open('doctypes/doctypes_schema.json', 'r+') as rawJSON:
            try:
                self.doctypesSchema = json.load(rawJSON)
            except ValueError:
                rawJSON.write("{}")
                self.doctypesSchema = {}

    def update_doctypes_schema(self, schemaToUpdate):
        """
        Updates and persists the doctypes schema in its file
        """
        self.doctypesSchema.update(schemaToUpdate)

        with open('doctypes/doctypes_schema.json', 'w') as fileObject:
            fileObject.write(json.dumps(self.doctypesSchema))

    def clear_index(self):
        """
        Clear index: whoosh indexe create, create a new index in the directory
        even if an index exists.
        """

        if os.path.exists("indexes"):
            index.create_in("indexes", self.schema)

        if os.path.exists("doctypes"):
            with open('doctypes/doctypes_schema.json', 'w') as defaultFile:
                defaultFile.write("{}")


class Indexer():

    def get_field_type(self, field, fieldsType):
        """"
        Determines the field type based on the field name (convention)
        """

        supportedTypes = ['string', 'number', 'date', 'boolean']

        # Checks if the field type has been passed
        fieldType = fieldsType.get(field, None)
        if fieldType is not None and fieldType in supportedTypes:
            return fieldType

        # To ensure backwards compatibility, we have a default type that
        # will be interepreted like "do the previous version way"
        else:
            return "default"

    def get_typed_field_name(self, field, fieldType):
        """
        Returns the field name with its Whoosh type appended
        """

        typedFieldName = "%s_%s" % (field, fieldType)
        return typedFieldName.lower()

    def get_formatted_data(self, data, fieldType):
        """
        Converts the data from string to the relevant type
        """

        if fieldType == 'string':
            return data.decode("utf-8")
        elif fieldType == 'number':
            return float(data)
        elif fieldType == 'date':
            return stringToDate(data)
        elif fieldType == 'boolean':
            return strtobool(data)

    def index_doc(self, docType, doc, fields, fieldsType):
        """
        Add given doc to index, tag and given fields are stored.
        """

        indexSchema = IndexSchema()

        # The document that will be indexed
        indexedDoc = {}

        # Support for old way of indexing
        contents = []

        # caching the result to avoid calling it from the loop
        fieldsInDoc = doc.keys()

        # the fields that the indexer will store as schema of the doctype
        fieldsInSchema = []

        # Normalize docType
        docType = unicode(docType.lower())

        # Extracts and formats every doc field to be indexed
        for field in fields:

            # Process the field only if it exists and if it's not a special one
            if field in fieldsInDoc and field not in ['id', 'docType', 'tags']:

                data = doc[field]

                # Field type is needed to convert the data into the proper type
                # from string
                fieldType = self.get_field_type(field, fieldsType)

                # To ensure backwards compatibility, we use a "default"
                # field tye that act like previous version (putting everything
                # in a field)
                if fieldType == "default":
                    logger.warning("Field %s is going to be indexed the "
                                   "old way" % field)

                    # Only strings are supported in BC mode
                    if isinstance(data, basestring):
                        contents.append(data)
                    else:
                        logger.warning("Data type not supported for field "
                                       "%s (%s)" % (field, data))
                else:
                    typedFieldName = self.get_typed_field_name(field,
                                                               fieldType)
                    fieldsInSchema.append(typedFieldName)
                    indexedDoc[typedFieldName] = \
                        self.get_formatted_data(data,
                                                fieldType)

            # Handles error cases
            elif field not in fieldsInDoc:
                logger.warning("Cannot found field %s in document" % field)
            else:
                logger.warning("Field %s is automatically indexed" % field)

        # Adds the doctype as a tag
        tags = doc["tags"].append(docType)
        tags = u" ".join(doc["tags"][0::1])

        # Adds special fields
        indexedDoc["docId"] = unicode(doc["id"])
        indexedDoc["tags"] = tags
        indexedDoc["docType"] = docType
        indexedDoc["content"] = u" ".join(contents)

        logger.info("About to index %s" % indexedDoc.keys())
        writer = indexSchema.index.writer()
        writer.update_document(**indexedDoc)
        writer.commit()

        logger.info("Update schema for doctype %s with %s"
                    % (docType, fieldsInSchema))
        schemaToUpdate = {docType: fieldsInSchema}
        indexSchema.update_doctypes_schema(schemaToUpdate)

    def search_doc(self, word, docTypes, numPage=1, numByPage=10,
                   showNumResults=False):
        """
        Return a list of docs that contains given word and that matches
        given type.
        """

        indexSchema = IndexSchema()

        # Retrieves the fields to search from the doctypes schema
        fieldsToSearch = []
        for docType in docTypes:
            docType = docType.lower()
            try:
                schema = indexSchema.doctypesSchema[docType]
                fieldsToSearch = fieldsToSearch + schema
            except:
                logger.warning("Schema not found for %s" % docType)

        # By default we search "content" (for BC) and "tags"
        fields = ['content', 'tags'] + fieldsToSearch
        logger.info("Search will be performed on fields %s" % fields)

        # Creates the query parser.
        # MultifieldParser allows search on multiple fields.
        # We use a custom FuzzyTerm class to set the Levenstein distance to 2
        parser = MultifieldParser(fields, schema=indexSchema.schema,
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

            resultsID = [result["docId"] for result in results]
            logger.info("Results: %s" % resultsID)

            # Ensures BC if the number of results is not requested
            if showNumResults:
                return {'ids': resultsID, 'numResults': len(results)}
            else:
                return {'ids': resultsID}

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
