import nltk
import collections
from nltk.corpus import udhr


class LangModeler(object):
    def __init__(self, languages, words):
        self.languages = languages
        self.words = words

    def build_language_models(self):
        # hint: use nltk.ConditionalFreqDist
        return nltk.ConditionalFreqDist((language, word.lower())
                                        for language in self.languages
                                        for word in udhr.words(language + '-Latin1'))

    def guess_language(self, language_model_cfd, text):
        """Returns the guessed language for the given text"""

        # based on the frequency of words accessible by language_model_cfd[language].freq(word) and then
        # identify most likely language for a given text according to this score
        results = {lang: 0 for lang in self.languages}
        token = nltk.word_tokenize(text)
        for word in token:
            for language in self.languages:
                results[language] += language_model_cfd[language][word]

        results = [lang for lang, _ in sorted(results.items(), key=lambda s: s[1], reverse=True)]

        return results[0]
