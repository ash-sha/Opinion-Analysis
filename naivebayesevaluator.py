from evaluator import Evaluator
from naivebayesclassifier import NaiveBayesClassifier
import csv
import datetime
import sys
import argparse

class NaiveBayesEvaluator(Evaluator):
    def __init__(self, trainfile, testfile, *args, **kargs):
        Evaluator.__init__(self, trainfile, testfile, *args, **kargs)

        self.allthresholds = kargs.get("allthresholds")
        self.csvout = kargs.get("csvout", False)
        self.results = []



    def run(self):
        
        for grams in self.allgrams:
            c = NaiveBayesClassifier(self.rawfname,
                                     grams=grams)
            c.trainClassifier()
            self.stdout = False

            return self.evaluate(c)
        
            
        for grams in self.allgrams:
            c = NaiveBayesClassifier(self.rawfname,
                                     grams=grams)
            c.trainClassifier()
            
            for w in self.allweights:
                c.setWeight(w)                                
        
                for t1 in self.allthresholds:
                    for t2 in self.allthresholds:
                        c.setThresholds(neg=t1, pos=t2)
                        cinfo, accpos, accneg, accall, corrall = self.evaluate(c)
                        self.results.append([cinfo, accpos, accneg, accall, corrall])


def processGrams(glist):
    return [[int(eachr) for eachr in each.split(',')] for each in glist]

def floatrange(start, end, step):
    return [start + step*x for x in range(int((end-start)/step)+1)]

def processWT(wstr):
    start, end, step = [float(res) for res in wstr.split(',')]
    return floatrange(start, end, step)

def main(fromGUI=0):
    trainfile = "trainingandtestdata/training.csv"
    testfile = "trainingandtestdata/testing.csv"

    parser = argparse.ArgumentParser()
    parser.add_argument("--csvout", dest="csvout",
                        action="store_true", default=False)
    parser.add_argument("--stdout", dest="stdout", 
                        action="store_true", default=False)
    parser.add_argument("-g", dest="g", nargs="+",
                        metavar="x,y,z,..", required=False)
    parser.add_argument("-w", dest="w",
                        metavar="START, END, STEP", required=False)
    parser.add_argument("-t", dest="t",
                        metavar="START, END, STEP", required=False)

    args = parser.parse_args()
    if fromGUI==0:
        grams = processGrams(args.g)
    else:
        grams=[[1],[1,2]]
        weights = thresholds = []

    try:
        if fromGUI==0:
            if args.g and args.w and args.t:
                weights = processWT(args.w)
                thresholds = processWT(args.t)
            else:
                weights = thresholds = []
            
        nbEvaluator = NaiveBayesEvaluator(trainfile, testfile,
                                          allgrams=grams,
                                          allweights=weights,
                                          allthresholds=thresholds,
                                          csvout=args.csvout,
                                          stdout=args.stdout)        
        return nbEvaluator.run()
    
    except Exception as e: 
        print 'Exception: ', e
        parser.print_help()

if __name__ == "__main__":
    main()
