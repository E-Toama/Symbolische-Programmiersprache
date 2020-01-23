from nltk.corpus import wordnet
from itertools import combinations
from collections import Counter


def leave_odd_man_out(words):
    pairs = [(x, y) for x in words for y in words if x != y]
    simsilarities = get_similarity_scores(pairs)
    res = min(simsilarities, key=lambda x: x[1])[0].split("-")[1]
    return res


def get_similarity_scores(pairs):
    results = []

    for pair in pairs:

        max_score = 0.0
        max_line = ()  # should look like "('food-fruit', 0.1)"

        # TODO 1. iterate over all combinations of synsets formed by the synsets of the words in the word pair
        # TODO 2. determine the maximum similarity score
        # TODO 3. save max_line in results in form ("pair1-pair2", similarity_value) e.g.('car-automobile', 1.0)
        word1 = wordnet.synsets(pair[0])
        word2 = wordnet.synsets(pair[1])
        for w1 in word1:
            for w2 in word2:
                similarity = w1.path_similarity(w2)
                if similarity != None and similarity > max_score:
                    max_score = similarity
                    max_line = (pair[0] + '-' + pair[1], max_score)
        results.append(max_line)

    return sorted(results, key=lambda x: x[1], reverse=True)
