from collections import defaultdict
from nltk import word_tokenize
import sys
import math

def normalized_tokens(text):
    return [token.lower() for token in word_tokenize(text)]

class DataInstance:
    def __init__(self, feature_counts, label):
        """ A data instance consists of a dictionary with feature counts (string -> int) and a label (True or False)."""
        self.feature_counts = feature_counts
        self.label = label

    @classmethod
    def from_list_of_feature_occurrences(cls, feature_list, label):
        """ Creates feature counts for all features in the list."""
        feature_counts = dict()
        for feature in feature_list:
            count = feature_counts.get(feature, 0)
            feature_counts[feature] = count + 1
        return cls(feature_counts, label)

    @classmethod
    def from_text_file(cls, filename, label):
        with open(filename, 'r') as myfile:
            token_list = normalized_tokens(myfile.read().strip())
        return cls.from_list_of_feature_occurrences(token_list, label)

class Dataset:
    def __init__(self, instance_list):
        """ A data set is defined by a list of instances """
        self.instance_list = instance_list
        self.feature_set = set.union(*[set(inst.feature_counts.keys()) for inst in instance_list])


class NaiveBayesClassifier:
    def __init__(self, word_and_category_to_count, category_to_num_instances, vocabsize, smoothing):
        """ Creates a Naive Bayes-Classifier. The following parameters are used:
        word_and_category_to_count: how often did a word occur in instances of a category?
        category_to_num_instances: proportion of instances per category.
        vocabsize: overall size of feature set (= vocabulary)
        smoothing: laplace parameter, added to counts for each word when calculating probabilities
        """
        self.word_and_cat_to_count = word_and_category_to_count
        self.cat_to_num_words = defaultdict(int)
        for (word, cat), count in word_and_category_to_count.items():
            self.cat_to_num_words[cat] += count
        self.vocabsize = vocabsize
        total_instances = sum(category_to_num_instances.values())
        self.category_to_prior = {c: n/total_instances for c, n in category_to_num_instances.items()}
        self.smoothing = smoothing

    @classmethod
    def for_dataset(cls, dataset, smoothing = 1.0):
        """ Creates a NB-Classifier for a dataset."""
        # (str,str) -> int | (word,label) -> count
        word_and_category_to_count = defaultdict(int) # maps tuples (word, category) to the number of occurences (of a word in a that category)
        # str -> int | label -> number of instances of this label
        category_to_num_instances = defaultdict(int) # maps a category name to the number of instances in that category
        vocabsize = len(dataset.feature_set)
        for inst in dataset.instance_list:
            # da defaultdicts, braucht man nicht ueberpruefen ob die Keys schon existieren
            for word in inst.feature_counts:
                word_and_category_to_count[(word, inst.label)] += inst.feature_counts[word]
            category_to_num_instances[inst.label] += 1
        return cls(word_and_category_to_count, category_to_num_instances, vocabsize, smoothing)

    def log_probability(self, word, category):
        """ This computes the probability log(P(instance|category)).
        The probability of the instance is the product of the probability of all words (w1, w2, ... wn) in that instance.
        Laplace smoothing is applied when the word probabilities are computed.

        log[P(instance|category)] = log[P(w1|category) * P(w1|category) * ... * P(wn|category)]
            = log[P(w1|category)] +  log[P(w1|category)] + ... + log[P(wn|category)]
        """
        wordcount = self.word_and_cat_to_count.get((word, category), 0)
        total = self.cat_to_num_words.get(category, 0)
        # Parametrize by overall count added rather than per type.
        return math.log(wordcount + self.smoothing) - math.log(total + self.smoothing * self.vocabsize)

    def score_for_category(self, feature_counts, category):
        """ This computes the unnormalized log-probability of a category for one instance.

        score_for_category(instance, category) = log( P(instance|category) * p(category) )
            = log[P(instance|category)] + log[P(category)]
        """
        # language model probability
        score = sum([count * self.log_probability(word, category) for word, count in feature_counts.items()])
        # prior probability
        score += math.log(self.category_to_prior[category])
        return score

    def prediction(self, feature_counts):
        """ Predicts a category according of the log-odds of the feature counts of this label.
        feature_counts is a dict (str -> int)."""
        category_score_dict = {}
        for category in self.cat_to_num_words:
            category_score_dict[category] = self.score_for_category(feature_counts, category)
        best_category = None

        for category in category_score_dict:
            if best_category == None or category_score_dict[category] > category_score_dict[best_category]:
                best_category = category
        return best_category

    def prediction_accuracy(self, dataset):
        """ Returns the accuracy of this classifier on a test set."""
        predicted_list = []
        if len(dataset.instance_list) == 0:
            return 0
        for instance in dataset.instance_list:
            if self.prediction(instance.feature_counts) == instance.label:
                predicted_list.append(instance)
        return len(predicted_list) / len(dataset.instance_list)

    def log_odds_for_word(self, word, category):
        """ This computes the log-odds for one word only.
        log_odds(word, category) = log( P(category|word) / (1 - P(category|word)) )
            = log[P(word|category)*P(category)]
                - log[P(word|other_category1)*P(other_category1)
                      + P(word|other_category2)*P(other_category2) + ...]
        """
        category_log_prob = self.log_probability(word, category) + math.log(self.category_to_prior[category])
        score_others = 0

        for cat in self.category_to_prior:
            if cat != category:
                numerator = (self.word_and_cat_to_count.get((word, cat), 0) + self.smoothing) * self.category_to_prior[cat]
                denominator = self.cat_to_num_words[cat] + self.smoothing * self.vocabsize
                score_others +=  numerator / denominator
        score_others = math.log(score_others)
        return category_log_prob - score_others

    def features_for_category(self, category, topn=10):
        """ Returns the topn features, that have the highest log-odds ratio for a category."""
        words = [word for word, cat in self.word_and_cat_to_count if cat == category]
        return sorted(words, key=lambda word: self.log_odds_for_word(word, category), reverse=True)[:topn]
