import nltk

def word_tokenize(text):
    return nltk.word_tokenize(text)


def normalized_tokens(text):
    """ This takes a string and returns lower-case tokens, using nltk for tokenization. """
    text = text.lower()
    return word_tokenize(text)

def countWords(text):
    txt = word_tokenize(text)
    d = {}
    for token in txt:
        if token in d:
            d[token] += 1
        else:
            d[token] = 1
    return d


class TextDocument:
    def __init__(self, text, id=None):
        """ This creates a TextDocument instance with a string, a dictionary and an identifier. """
        self.text = text
        self.word_to_count = countWords(text)
        self.id = id

    @classmethod
    def from_file(cls, filename):
        """ This creates a TextDocument instance by reading a file. """
        text = open(filename, "r")
        result = text.read()
        return cls(result, filename)

    def __str__(self):
        """ This returns a short string representation, which is at most 25 characters long.
        If the original text is longer than 25 characters, the last 3 characters of the short string should be '...'.
        """
        result = ''
        if (len(self.text) < 25):
            result = self.text
            return result
        else:
            count = 0
            for z in self.text:
                if (count < 23):
                    result += z
                    count += 1
                else:
                    continue;
        result += '...'
        return result


    def word_overlap(self, other_doc):
        """ This returns the number of words that occur in both documents (self and other_doc) at the same time.
        Every word should be considered only once, irrespective of how often it occurs in either document (i.e. we
        consider word *types*).
        """
        doc1 = countWords(self.text)
        doc2 = countWords(other_doc)
        res = []
        for word in doc1:
            if word in doc2:
                res.append(word)
        result = len(res)
        return result

