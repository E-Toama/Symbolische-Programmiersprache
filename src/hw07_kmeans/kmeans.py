import string
import numpy as np
import random, math

class Reader:

    def __init__(self, path):
        self.path = path
        self.punctuation = set(string.punctuation)
        self.courses = self.get_lines()
        self.vocabulary = self.get_vocabulary()
        self.vector_spaced_data = self.data_to_vectorspace()

    def get_lines(self):
        #TODO 1 return list of courses from file
        result = []
        with open(self.path, "r") as file:
            line = file.readline()
            while line != "":
                result.append(line.strip())
                line = file.readline()
        return result

    def normalize_word(self,word):
        #TODO 2 normalize word by lower casing and deleting punctuation from word
        #TODO use set of punctuation symbols self.punctuation
        for symbol in string.punctuation:
            if symbol in word:
                word = word.replace(symbol, '')
        return word.lower()

    def get_vocabulary(self):
        #TODO 3 return list of unique words from file and sort them alphabetically
        normalized_courses = [self.normalize_word(x) for x in self.get_lines()]
        vocabulary = set()
        for elem in normalized_courses:
            vocabulary = vocabulary.union(elem.split(' '))
        return sorted(vocabulary)

    def vectorspaced(self,course):
        #TODO 4 represent course by one-hot vector: vector filled with 0s, except for a 1 at the position associated with word in vocabulary
        #TODO length of vector should be equal vocabulary size
        temp = [(x in self.normalize_word(course).split(' ')) for x in self.vocabulary]
        return list(map(int, temp))


    def data_to_vectorspace(self):
        return [self.vectorspaced(course) for course in self.courses if course]

class Kmeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k
        self.means = None

    def distance(self, x,y):
        #TODO 5 calculate Euclidean distance between two vectors x and y
        result = 0
        for i in range(len(x)):
            result += (x[i] - y[i])**2
        return math.sqrt(result)

    def classify(self,input):
        #TODO 6 calculate Euclidean distances between input and the means and return the mean index with min distance
        return min(range(self.k), key=lambda i: self.distance(input, self.means[i]))

    def vector_mean(self,vectors):
        #TODO calculate mean of the list of vectors
        zipped = zip(*vectors)
        result = []
        for tuple in zipped:
            result.append(sum([x for x in tuple])/len(tuple))
        return result

    def train(self, inputs):
        # choose k random points as the initial means
        self.means = random.sample(inputs, self.k)#step 1

        #uncomment the following line and use the given means for the unittest
        self.means = [inputs[32], inputs[67], inputs[46]]

        assignments = None
        iter = 0
        while iter != 100:
            # find new assignments
            assignments = list(map(self.classify, inputs))

            # compute new means based on the new assignments
            for i in range(self.k):
                # find all the points assigned to cluster i
                i_points = [p for p, a in zip(inputs,assignments) if a == i]
                if i_points:
                    # make sure i_points is not empty so don't divide by 0
                    self.means[i] = self.vector_mean(i_points)
            iter += 1
