from unittest import TestCase
from hw04_text_search.text_vectors import TextDocument, DocumentCollection, SearchEngine

test_doc_list = [TextDocument(text_and_id[0], text_and_id[1]) for text_and_id in
                 [("the cat sat on a mat", "doc1"),
                  ("a rose is a rose", "doc2"),
                  ("Well, good night.\nIf you do meet Horatio and Marcellus,\nThe rivals of my watch", "doc3"), #Test for linebreaks
                  ("Horatio says 'tis but our fantasy, And will not let belief take hold of him","doc4")]]
small_collection = DocumentCollection.from_document_list(test_doc_list)

class DocumentCollectionTest(TestCase):

    def setUp(self):
        test_doc_list = [TextDocument(text_and_id[0], text_and_id[1]) for text_and_id in
                         [("the cat sat on a mat", "doc1"),
                          ("a rose is a rose", "doc2")]]
        self.small_collection = DocumentCollection.from_document_list(test_doc_list)

        # TODO: uncomment in case tests need access to whole document collection.
        # this_dir = os.path.dirname(os.path.abspath(__file__))
        # document_dir = os.path.join(this_dir, os.pardir, 'data/enron/enron1/ham/')
        # self.large_collection = DocumentCollection.from_dir(document_dir, ".txt")

    def test_unknown_word_cosine(self):
        """ Return 0 if cosine similarity is called for documents with only out-of-vocabulary words. """
        # Document that only contains words that never occurred in the document collection.
        query_doc = TextDocument(text="unknownwords", id=None)
        # Some document from collection.
        collection_doc = self.small_collection.docid_to_doc["doc1"]
        # Similarity should be zero (instead of undefined).
        self.assertEqual(self.small_collection.cosine_similarity(query_doc, collection_doc), 0.)

    def test_less_tokens_if_needed(self):
        """If no result is found with all the tokens, show results that at least include one token"""
        self.assertEqual(self.small_collection.docs_with_all_tokens({"cat", "dog"}), self.small_collection.docs_with_all_tokens({"cat"}))

class TextDocumentTest(TestCase):
    # TODO: Unittests for TextDocument go here.
    pass


class SearchEngineTest(TestCase):

    def setUp(self):
        self.search_engine = SearchEngine(small_collection)

    # TODO: Unittests for SearchEngine go here.
    def test_snippets_linebreak(self):
        """Tests if line break markers are removed from the textsnippets"""
        for snippet in self.search_engine.snippets("Horatio", small_collection.docid_to_doc["doc3"]):
            self.assertTrue("\n" not in snippet)

    def test_token_multiple(self):
        """Tests that a query only shows one text snippet, if a query contains the same token multiple times"""
        for snippet in self.search_engine.snippets("Horatio", small_collection.docid_to_doc["doc3"]):
            self.string1 = [snippet]
        for snippet in self.search_engine.snippets("Horatio Horatio", small_collection.docid_to_doc["doc3"]):
            self.string2 = [snippet]
        self.assertEqual(self.string1, self.string2)