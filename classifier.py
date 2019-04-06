import csv
import re
import nltk
import os
import cPickle as pickle
import random

class Classifier:

    def __init__(self, rawfname, *args, **kargs):
        self.rawfname = rawfname

        self.force = kargs.get("force", False)
        self.numgrams = kargs.get("grams", [1])

        self.modelfname = "model%s.dat" % \
                          (reduce(lambda x, y: str(x)+'-'+str(y),
                                  self.numgrams))
        self.weight = kargs.get("weight", 0.00005)
        self.filesubset = kargs.get("filesubset", "all")
        self.tweetcounts = [0, 0]
        self.ftweetcounts = {}

    def incFC(self, f, c):
        self.ftweetcounts.setdefault(f, [0, 0])
        self.ftweetcounts[f][c] += 1

    def incC(self, c):
        self.tweetcounts[c] += 1

    def getFC(self, f, c):
        if f in self.ftweetcounts:
            return float(self.ftweetcounts[f][c])
        return 0.0

    def getC(self, c):
        return float(self.tweetcounts[c])
    
    def getTotal(self):
        return sum(self.tweetcounts)

    def getFeatures(self, item):
        flist = []
        for gram in self.numgrams:
            tokenized = nltk.word_tokenize(item)
            for i in range(len(tokenized)-gram+1):
                flist.append(" ".join(tokenized[i:i+gram]))
        return set(flist)

    def train(self, c, item):
        features = self.getFeatures(item)
        for f in features:
            self.incFC(f, c)
        self.incC(c)

    def trainClassifier(self):

        if self.force:
            os.remove(self.modelfname)        
        elif os.path.exists(self.modelfname):
            grams, self.tweetcounts, self.ftweetcounts = pickle.load(open(self.modelfname, "rb"))
            if grams == self.numgrams:
                print "Model retrieved from '%s'" % self.modelfname
                return

        f = open(self.rawfname)
        r = csv.reader(f, delimiter=',', quotechar='"')


        stripped = [(0 if line[0] == '0' else 1, 
                     re.sub(r'[,.]', r'',
                            line[-1].lower().strip())) for line in r]

        last_line = len(stripped) if self.filesubset == "all" else self.filesubset

        for each in stripped[:last_line]:
            self.train(each[0], each[1])


        pickle.dump([self.numgrams, self.tweetcounts, self.ftweetcounts],
                    open(self.modelfname, "wb")
        )


        f.close()

    def getSampleTweets(self, n, pct_pos = .5):

        random.seed(10)
        numpos, numneg = 0, 0
        targetpos, targetneg = int(n * pct_pos), int(n * (1 - pct_pos))


        sample = []

        f = open(self.rawfname)
        r = csv.reader(f, delimiter=',', quotechar='"')


        stripped = [(0 if line[0] == '0' else 1, 
                     re.sub(r'[,.]', r'',
                            line[-1].lower().strip())) for line in r]

        random.shuffle(stripped)
        
        i = 0


        while numpos < targetpos or numneg < targetneg:
            curtweet = stripped[i]

            if curtweet[0] == 0 and numneg < targetneg:
                numneg += 1
                sample.append(curtweet)
            elif curtweet[0] == 1 and numpos < targetpos:
                numpos += 1
                sample.append(curtweet)
            i += 1

        return sample

    def probFC(self, f, c):

        if self.getC(c) == 0: 
            return 0
        return self.getFC(f, c)/self.getC(c)

    def probC(self, c):

        return self.getC(c)/self.getTotal()

    def setWeight(self, w):

        self.weight = w

    def weightedProb(self, f, c, ap=0.5):

        real = self.probFC(f, c)
        

        totals = sum([self.getFC(f,c) for c in [0, 1]])
        

        return ((self.weight * ap) + (totals * real))/(self.weight + totals)


    def __repr__(self):
        return "Classifier info: (weight=%s, grams=%s)" % (self.weight, self.numgrams)
