import abc
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

class TextClassifier(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._corpus = None
        self._vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english', analyzer="word") #todo config

    def set_corpus(self, corpus):
        """
        Sets the classifiers corpus
            Must be a list of iterables
        """
        self._corpus = []
        for element in corpus:
            self._corpus.append(element)

    def append_to_corpus(self, to_append):
        if self._corpus is None:
            self._corpus = []
        self._corpus.append(to_append)

    @abc.abstractmethod
    def train(self, train_data, train_labels):
        raise Exception("Abstract Class : Not Implemented")

    @abc.abstractmethod
    def predict(self, data):
        raise Exception("Abstract Class : Not Implemented")


class BayesClassifier(TextClassifier):

    def __init__(self):
        super(BayesClassifier, self).__init__()
        self._classifier = MultinomialNB()

    def train(self, train_data, train_labels):
        if self._corpus is None:
            raise Exception("Corpus is not set")
        self._vectorizer.fit(self._corpus)
        train_vectors = self._vectorizer.transform(train_data)
        self._classifier.fit(train_vectors, train_labels)

    def predict(self, data):
        vector = self._vectorizer.transform([data])
        return self._classifier.predict(vector)
