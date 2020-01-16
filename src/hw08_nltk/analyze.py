import nltk
from nltk import FreqDist
from nltk import word_tokenize


class Analyzer(object):
    def __init__(self, path):
        """reads the file text, creates the list of words (use nltk.word_tokenize to tokenize the text),
            and calculates frequency distribution """
        f = open(path)
        raw = f.read()
        f.close()
        self.text = nltk.word_tokenize(raw)
        self.token_counts = nltk.FreqDist(self.text)

    def numberOfTokens(self):
        """returns number of tokens in the text """
        return len(self.text)

    def vocabularySize(self):
        """returns a list of the vocabulary of the text """
        return len(self.token_counts)

    def lexicalDiversity(self):
        """returns the lexical diversity of the text """
        return self.numberOfTokens() / self.vocabularySize()

    def getKeywords(self):
        """return words as possible key words, that are longer than seven characters, that occur more than seven
        times (sorted alphabetically) """
        return sorted([key for (key, value) in self.token_counts.items() if len(key) > 7 and value > 7])

    def numberOfHapaxes(self):
        """returns the number of hapaxes in the text"""
        return len(self.token_counts.hapaxes())

    def avWordLength(self):
        """returns the average word length of the text"""
        all_Characters = 0
        for word in self.token_counts:
            all_Characters += len(word)
        return all_Characters / self.vocabularySize()

    def topSuffixes(self):
        """returns the 10 most frequent 2-letter suffixes in words
            (restrict to words of length 5 or more)"""
        wordlist = [words[-2:] for words in self.token_counts if len(words) >= 5]
        count_Suffixes = nltk.FreqDist(wordlist)
        suffixes_List = [suffix for suffix, count in sorted(count_Suffixes.items(), key=lambda v: v[1], reverse=True)]
        return suffixes_List[:10]

    def topPrefixes(self):
        """returns the 10 most frequent 2-letter prefixes in words
            (restrict to words of length 5 or more)"""
        wordlist = [word[:2] for word in self.token_counts if len(word) >= 5]
        countsuf = nltk.FreqDist(wordlist)
        suflist = [suffix for suffix, count in sorted(countsuf.items(), key=lambda v: v[1], reverse=True)]
        return suflist[:10]

    def tokensTypical(self):
        """returns first 5 tokens of the (alphabetically sorted) vocabulary
        that contain both often seen prefixes and suffixes in the text. As in topPrefixes()
        and topSuffixes(), Prefixes and Suffixes are 2 characters long."""
        toppre = self.topPrefixes()
        topsuf = self.topSuffixes()
        tokenstypical = [tt for tt in self.token_counts if tt[:2] in toppre and tt[-2:] in topsuf]
        return sorted(tokenstypical)[:5]
