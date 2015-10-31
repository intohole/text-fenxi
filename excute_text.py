#coding=utf-8

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import lda


c =  CountVectorizer()
t = TfidfTransformer()
tfidf = TfidfVectorizer()
vector = []
for i in range(1, 10):
    with open('data/%s.txt' % i) as f:
        content = []
        is_content = False
        for line in f.readlines():
            line = line.rstrip()
            if line.startswith("# title #") and line.endswith('# / title #'):
                line = line.replace("# title #" , "" ).replace("# / title #","")
                content.append(line)
            elif line.startswith("# content #") and is_content is False:
                content.append(line.replace("# content #",""))
                is_content = True
            elif line.startswith("# / content #"):
                is_content = False
            elif is_content is True:
                content.append(line)
        vector.append(' '.join(content))
tfidf_vector = tfidf.fit_transform(vector)
cluster = KMeans(init = 'k-means++' , n_clusters =  3  )
cluster_result = cluster.fit(tfidf_vector)
print cluster_result.labels_

