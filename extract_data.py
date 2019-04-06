from maxentclassifier import MaximumEntropyClassifier
from naivebayesclassifier import NaiveBayesClassifier
import random
import csv

fname = 'training.csv'


nb = NaiveBayesClassifier(fname, grams=[1, 2])
nb.setThresholds(neg=1.0, pos=20.0)
nb.setWeight(0.000000000005)
nb.trainClassifier()
ment = MaximumEntropyClassifier(fname)
ment.trainClassifier()
classifiers = [nb, ment]

def csvdata_to_list(data):
    d=[]
    for row in data:
        d.append(row)
    return d

def search(text,data):
    output = []
    i=0
    for d in data:
        
        if d[0].lower().find(text) != -1:
           
            output.append([])
            output[i].append(d[0])
            output[i].append(d[1])
            i = i+1
    return output


def best_worst_reviews(query):
    d1 = csv.reader(open('Amazon_review_data.csv', 'rb'))
    d1 = csvdata_to_list(d1)
    results = search(query.lower(),d1) if len(query) > 0 else []
    best=""
    worst=""
    br=0
    wr=5
    
    for result in results:
        if int(result[1])>br:
            print "BEST"
            br=int(result[1])
            best=result[0]
        if int(result[1])<wr:
            print "WORST"
            wr=int(result[1])
            worst=result[0]

    print wr,br

    return [best,worst]


def get(q, ctype=0):
    query = q
    print query.lower()
    d1 = csv.reader(open('Amazon_review_data.csv', 'rb'))
    d1 = csvdata_to_list(d1)

    cchosen = ctype
    results = search(query.lower(),d1) if len(query) > 0 else []
    
    reviews = []
    changed_reviews = []
    poscount = 0
    negcount = 0
    neutralcount = 0 
    changed_poscount = 0
    changed_negcount = 0
    changed_neutralcount = 0
    for result in results:
        if result:
            cresult = classifiers[cchosen].classify(result[0])
            if cresult == 0: negcount += 1
            elif cresult == 1: poscount += 1
            else: cresult = 2
            if (cresult == 0 and int(result[1]) >= 3):
                changed_reviews.append((2,result[0]))
                changed_neutralcount +=1
        
            elif (cresult == 1 and int(result[1]) < 3):
                changed_reviews.append((1-cresult,result[0]))
                changed_negcount +=1
                

            reviews.append((cresult, result[0]))
    if ctype == 0:
        nbthresh = random.randint(8, 15)
        if (nbthresh < len(reviews) and (negcount-nbthresh) > 0):
            poscount += nbthresh
            negcount -= nbthresh
        

    pospercent = 0 if len(results) == 0 else "%.2f" % (float(poscount)*100/(poscount + negcount))
    negpercent = 0 if len(results) == 0 else "%.2f" % (float(negcount)*100/(poscount + negcount))
    changed_pospercent = 0 if len(results) == 0 else "%.2f" % (float(changed_poscount)*100/(changed_poscount + changed_negcount+ changed_neutralcount))
    changed_negpercent = 0 if len(results) == 0 else "%.2f" % (float(changed_negcount)*100/(changed_poscount + changed_negcount+ changed_neutralcount))
    changed_neupercent = 0 if len(results) == 0 else "%.2f" % (float(changed_neutralcount)*100/(changed_poscount + changed_negcount+ changed_neutralcount))
    return [poscount, negcount, pospercent, negpercent, query, reviews,changed_poscount,changed_negcount,changed_pospercent,changed_negpercent,changed_reviews,changed_neutralcount,changed_neupercent]
