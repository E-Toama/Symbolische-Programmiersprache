from nltk import FreqDist, word_tokenize
from collections import defaultdict
import os, math


def dot(dictA, dictB):
    """ Returns Dot-product of two vectors (vectors are represented as dictionaries)
    >>> dot({"ceasar" : 1, "die" : 1, "in" : 1, "march" : 1} , {"the" : 1, "long" : 1, "march" : 1})
    1
    >>> dot({1:4,2:10,3:5},{1:2,2:15,3:2})
    168
    >>> dot({},{})
    0
    """
    return sum([dictA.get(tok) * dictB.get(tok, 0) for tok in dictA])


def normalized_tokens(text):
    """ Returns a list of lowercase tokens for the text
    >>> normalized_tokens("As thou art to thyself: Such was the very armour he had on When he the ambitious Norway combated;")
    ['as', 'thou', 'art', 'to', 'thyself', ':', 'such', 'was', 'the', 'very', 'armour', 'he', 'had', 'on', 'when', 'he', 'the', 'ambitious', 'norway', 'combated', ';']
    >>> normalized_tokens("")
    []
    """
    return [token.lower() for token in word_tokenize(text)]

# TODO: Docstring documentation for all member functions (including constructors) Ex.3.2
class TextDocument:
    def __init__(self, text, id=None):
        """Constructor for the TextDocument class.
        Also stores a dictionary with the frequency of each Token for the Text (self.token_counts)
        Args:
            text -- The Text for the TextDocument-Object
            id   -- An Optional ID for the TextDocument-Object
        """
        self.text = text
        self.token_counts = FreqDist(normalized_tokens(text))
        self.id = id

    @classmethod
    def from_file(cls, filename):
        """Creates a TextDocument object from a file.
        Opens the textfile in read only mode, removes default whitespace characters from beginning and end
        and calls the constructor with text as text and the filename as ID
        Args:
            filename -- Path of the file to import
        """
        with open(filename, 'r') as myfile:
            text = myfile.read().strip()
        return cls(text, filename)

# TODO: Docstring documentation for all member functions (including constructors) Ex.3.2
class DocumentCollection:
    def __init__(self, term_to_df, term_to_docids, docid_to_doc):
        """Constructor for the DocumentCollection class. A DocumentCollection is a Collection of certain
        metadata from different documents and parameters describing their relation The constructor is called with
        Args:
            term_to_df" -- A dictionary that maps each term(type) from all documents to the amount of documents they appear in.
            term_to_docids" -- A dictionary that maps each term to a set of all documents they appear in
            docid_to_doc -- A dictionary that maps docids to TextDocuments
        """
        # string to int
        self.term_to_df = term_to_df
        # string to set of string
        self.term_to_docids = term_to_docids
        # string to TextDocument
        self.docid_to_doc = docid_to_doc

    @classmethod
    def from_dir(cls, dir, file_suffix):
        """Collects document files from a folder and uses them to create a DocumentCollection object.
        All document files of a given filetype are collected from a given path and stored in a list which is then
        used to create a DocumentCollection using the from_document_list method.
        Args:
            dir          -- Path where document files are stored
            file_suffix  -- File-suffix (for example "txt") of the document files
        """
        files = [(dir + "/" + f) for f in os.listdir(dir) if f.endswith(file_suffix)]
        docs = [TextDocument.from_file(f) for f in files]
        return cls.from_document_list(docs)

    @classmethod
    def from_document_list(cls, docs):
        """Creates DocumentCollection Object from a list of documents.
        All documents from a list are used to create a DocumentCollection object. The method also parses the docs
        and calls the constructor with the correct values of term_to_df, term_to_docids and docid_to_doc.
        Args:
            docs -- list of documents to import
        """
        term_to_df = defaultdict(int)
        term_to_docids = defaultdict(set)
        docid_to_doc = dict()
        for doc in docs:
            docid_to_doc[doc.id] = doc
            for token in doc.token_counts.keys():
                term_to_df[token] += 1
                term_to_docids[token].add(doc.id)
        return cls(term_to_df, term_to_docids, docid_to_doc)

    def docs_with_all_tokens(self, tokens):
        """Searches a DocumentCollection for documents that contain a certain set of tokens from a query
        First it creates a (nested) list for each token from the query with the document ids for the documents
        they appear in, then uses intersection to find only the IDs for the documents that all tokens appear in.
        Returns Docids for the Documents that all tokens appear in.
        Args:
            tokens -- a list of tokens that
        """
        docids_for_each_token = [self.term_to_docids[token] for token in tokens]
        docids = set.intersection(*docids_for_each_token)  # union?
        if not docids:
            docids = set.union(*docids_for_each_token)
        return [self.docid_to_doc[id] for id in docids]

    def tfidf(self, counts):
        """Returns the "term frequency–inverse document frequency" vector for the DocumentCollection
        Creates a dictionary representing a Vector that maps Tokens to their TF-IDF value (a weighting factor used to
        reflect the importance of a term). The returned vector contains only those values that also appear in "counts"
        Args:
            counts -- token to term frequency dictionary used to reduce vector
        """
        N = len(self.docid_to_doc)
        return {tok: tf * math.log(N / self.term_to_df[tok]) for tok, tf in counts.items() if tok in self.term_to_df}

    def cosine_similarity(self, docA, docB):
        """Returns the cosine similarity of two documents
        Calculates the cosine similarity (a similarity measure) of two documents from a DocumentCollection representing
        the angle between the TF-IDF vectors of two Documents.
        Args:
            docA, docB -- Documents to Compare
        """
        weightedA = self.tfidf(docA.token_counts)
        weightedB = self.tfidf(docB.token_counts)
        dotAB = dot(weightedA, weightedB)
        normA = math.sqrt(dot(weightedA, weightedA))
        normB = math.sqrt(dot(weightedB, weightedB))
        if (normA == 0 or normB == 0):      # Check for division by zero (Exercise 4)
            return 0;    
        return dotAB / (normA * normB)

# TODO: Docstring documentation for all member functions (including constructors) Ex.3.2
class SearchEngine:
    def __init__(self, doc_collection):
        """Constructor for the SearchEngine, creates an instance of the SearchEngine for a DocumentCollection.
        Args:
            doc_collection -- the DocumentCollection the SearchEngine should operate on
        """
        self.doc_collection = doc_collection

    def ranked_documents(self, query):
        """Returns a list of documents ranked by cosine similarity to a search query in descending order.
        The search query is saved as a document and is then compared to all documents in the collection containing the
        same tokens using cosine similarity.
        Args:
            query -- a String with tokens for the search
        """
        query_doc = TextDocument(query)
        query_tokens = query_doc.token_counts.keys()
        docs = self.doc_collection.docs_with_all_tokens(query_tokens)
        docs_sims = [(doc, self.doc_collection.cosine_similarity(query_doc, doc)) for doc in docs]
        return sorted(docs_sims, key=lambda x: -x[1])

    def snippets(self, query, document, window=50):
        """ Searches a DocumentCollection for text-snippets containing tokens from a query
        Args:
            query -- a String with tokens for the search
            document -- the Document the text-snippets should be extracted from
            window -- the number of Characters before and after the tokens found in the doc for the text-snippet
        """
        tokens = normalized_tokens(query)
        text = document.text
        text = text.replace("\n", " ") # Macht newlines zu leerzeichen
        for token in tokens:
            start = text.lower().find(token.lower())
            if -1 == start:
                continue
            end = start + len(token)
            left = "..." + text[start - window:start]
            middle = "[" + text[start: end] + "]"
            right = text[end:end + window] + "..."
            yield left + middle + right
