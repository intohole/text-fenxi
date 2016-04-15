from b2 import system2
import xlrd
from collections import defaultdict

system2.reload_utf8()
user_goods_dict = defaultdict(list) 
xls = xlrd.open_workbook("./texts/association.xls")

for booksheet in xls.sheets():
    for row in xrange(booksheet.nrows):
        user_goods_dict[booksheet.cell(row , 0).value].append((booksheet.cell(row , 2).value))


sentences = []
for user,goods in user_goods_dict.items():
    sentences.append(goods)
import gensim
model = gensim.models.Word2Vec(sentences , window = 5 , size = 200 , min_count = 5 )
