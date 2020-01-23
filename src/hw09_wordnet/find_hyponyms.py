import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet


class HyponymSearcher(object):
    def __init__(self, text_path):

        self.noun_lemmas = []

        with open(text_path, mode='r') as file:
            text = file.read()
            sentences = nltk.sent_tokenize(text)
            tokens = nltk.word_tokenize(text)
            tags = nltk.pos_tag(tokens)
            lemmatizer = WordNetLemmatizer()
            nouns = [tag[0] for tag in tags if tag[1].startswith("N")]
            self.noun_lemmas = [lemmatizer.lemmatize(lemma, wordnet.NOUN) for lemma in nouns][:1262]

    def hypernymOf(self, synset1, synset2):
        res = False
        if synset1 == synset2 or synset2 in synset1.hypernyms():
            return True
        for hypernym in synset1.hypernyms():
            if synset2 == hypernym:
                return True
            if self.hypernymOf(hypernym, synset2):
                return True
        return False

    def get_hyponyms(self, hypernym):
        hyponyms = []
        for lemma in self.noun_lemmas:
            for synset in wordnet.synsets(lemma):
                if self.hypernymOf(synset, hypernym):
                    hyponyms.append(lemma)
        return set(hyponyms)
