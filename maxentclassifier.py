
import sys
import csv
import re
import os
import cPickle as pickle
from classifier import Classifier
from evaluator import Evaluator
from nltk.classify.maxent import MaxentClassifier

class MaximumEntropyClassifier(Classifier):
    def __init__(self, rawfname, min_occurences=5, **kargs):
        Classifier.__init__(self, rawfname, **kargs)

        self.min_occurences = min_occurences

        self.all_training_examples = []

        self.all_features = {}
        self.model = None

        self.filesubset = kargs.get('filesubset', 3000)

        self.max_iter = kargs.get('max_iter', 4)

    
    def setModel(self, model):
        self.model = model

    def initFeatures(self):
        training_sample = self.getSampleTweets(self.filesubset)

        for each in training_sample:
            classification = each[0]
            text = each[1]
            feature_set = self.getFeatures(text)

            feature_vector = self.getFeatureDict(feature_set)
            self.all_training_examples.append((feature_vector, classification))       


    def getFeatureDict(self, featureset):

        feature_dict = {}

        for feat in featureset:
            feature_dict[feat] = 1
            self.all_features.setdefault(feat, 0)
            self.all_features[feat] += 1
        
        return feature_dict


    def trainClassifier(self):

        pickled_model = self.checkForPickle()
        if pickled_model:
            self.model = pickled_model
        else:

            self.initFeatures()
            kargs = {'algorithm' : 'gis', }
            if self.max_iter != None:
                kargs['max_iter'] = self.max_iter
            self.pickleModel()
        print 'Max ent model built'


    def classify(self, text):
        feature_set = self.getFeatures(text)
        feature_vector = self.getFeatureDict(feature_set)

        return self.model.classify(feature_vector)

    def checkForPickle(self):
        pickle_name = self.getPickleFileName()

        if os.path.exists(pickle_name):
            f = file(pickle_name, 'rb')
            model = pickle.load(f)
            f.close()

            return model
        else:
            return False

    def pickleModel(self, model_name=None):

        if model_name == None:
            model_name = 'maxentpickles/maxent_%i_%i_%i.dat' % \
                         (self.filesubset, self.min_occurences, len(self.numgrams))

        outfile = open(model_name, "wb")
        pickle.dump(self.model, outfile)

        outfile.close()

    def getPickleFileName(self):
        return 'maxentpickles/maxent_%i_%i_%i.dat' % \
               (self.filesubset, self.min_occurences, len(self.numgrams))


def main():    
    trainfile = "trainingandtestdata/training.csv"
    testfile = "trainingandtestdata/testing.csv"
    maxent_args = {
      'filesubset' : 3500,
      'min_occurences' : 5,
      'max_iter' : 4,
      'grams' : [1]
    }
    ent = MaximumEntropyClassifier(trainfile, **maxent_args)
    ent.trainClassifier()

    if len(sys.argv) == 2:
        print ent.classify(sys.argv[1])
    

if __name__ == "__main__":
    main()
