#coding=utf-8




from moodstyle import cool
from moodstyle.cool import testFeatureExtract
from moodstyle.cool import testDict
from moodstyle.cool import testBayes
from b2 import file2
import sys
import re
xx = []
doc = testFeatureExtract.CreateDocument()
chinese =  re.compile(ur"[\u4e00-\u9fa5]+")
for i in range(1 , 45000):
    with open("data/%s.txt" % i ) as f:
        title = ""
        cls = ""
        for line in f.readlines():
            if line.startswith("# title"):
                title = line.rstrip().replace("# title #", "" ).replace("# / title #" , "")
            elif line.startswith("# emotion #"):
                cls = line.rstrip().replace("# emotion #" ,"").replace("# / emotion #" , "")
        if title  and cls:
            labels = map( lambda x : int(x) ,cls.strip().replace("%" ,"").split())
            label = None 
            for index , value in enumerate(labels):
                if value >= 75:
                    label = index 
            if label is None  or label == 0:
                continue
            title = [ t for t in title.split() if chinese.match(t.decode("utf-8")) ] 
            if len(title):
                xx.append((" ".join(title) , label ))
                doc.insert_document_list(str(label) , title)

extracts = cool.testFeatureExtract.IM()
word_set = set()
for doc_type , words in extracts.extract_feature(doc.doc , 2500):
    word_set.update(words)
dic = testDict.Dictionary(words = word_set)
vectors = []
lables = []
for x in xx:
    vectors.append(dic.to_vector(x[0]))
    labels.append(x[1])
classifier = testBayes.Bayes()
classifier.train(vectors[:18000] , len(dic) , labels[:18000])
from collections import Counter
c = Counter(labels)
right = 0  
from collections import defaultdict
a = defaultdict(int) 
for vector,label in  zip( vectors[-1000:] , labels[-1000:]):
    predict = classifier.predict(vector)[1]
    a[predict] += 1 if predict == label else 0 
print a 

