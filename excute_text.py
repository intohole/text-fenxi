#coding=utf-8

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import lda
from gensim.models.ldamodel import LdaModel
from gensim.corpora import Dictionary

c =  CountVectorizer()
t = TfidfTransformer()
tfidf = TfidfVectorizer()
vector = []
vectors = []
for i in range(1, 100):
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
        vectors.append(line.split())
        vector.append(' '.join(content))
tfidf_vector = tfidf.fit_transform(vector[:-3])
cluster = KMeans(init = 'k-means++' , n_clusters =  3  )
cluster_result = cluster.fit(tfidf_vector)
tfidf_vector_test = tfidf.fit_transform(vector[-3:])
dc = Dictionary(vectors)
corpus = [dc.doc2bow(vec) for vec in vectors]
lda = LdaModel(corpus = corpus , id2word=dc , num_topics = 3)
print lda.show_topics()
print lda.print_topics(3)[0]
