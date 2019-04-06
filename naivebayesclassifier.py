import sys
import math
from classifier import Classifier


class NaiveBayesClassifier(Classifier):
    def __init__(self, fname, *args, **kargs):
        # type: (object, object, object) -> object
        Classifier.__init__(self, fname, *args, **kargs)
        self.thresholds = [1.0, 1.0]

    def setThresholds(self, neg=1.0, pos=1.0):
        self.thresholds = [neg, pos]

    def probTweetClass(self, text, c):
        features = self.getFeatures(text)
        p = 0
        for f in features:
            p += math.log(self.weightedProb(f, c))
        return p

    def probClassTweet(self, text, c):
        if self.probC(c) > 0:
            return self.probTweetClass(text, c) + math.log(self.probC(c))
        else:
            return self.probTweetClass(text, c) + math.log(sys.float_info.min)

    def classify(self, text):
        p0 = self.probClassTweet(text, 0)
        p1 = self.probClassTweet(text, 1)

        if p0 > p1 + math.log(self.thresholds[0]):
            return 0
        elif p1 > p0 + math.log(self.thresholds[1]):
            return 1
        else:
            return -1

    def __repr__(self):
        return "Classifier info: (weight=%s, grams=%s, thresholds=%s)" % (self.weight, self.numgrams, self.thresholds)


def main():
    fromf = 'trainingandtestdata/training.csv'
    naive = NaiveBayesClassifier(fromf)
    naive.trainClassifier()
    if len(sys.argv) == 2:
        print
        text = sys.argv[1]
        result = naive.classify(text)
        if result == 0:
            print "'%s' predicted to be Negative" % text
        elif result == 1:
            print "'%s' predicted to be Positive" % text
        else:
            print "'%s' predicted to be Neutral" % text


if __name__ == "__main__":
    main()
