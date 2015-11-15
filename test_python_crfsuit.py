#coding=utf-8





import pycrfsuite


"""
    阅读http://nbviewer.ipython.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb
"""


#建立训练器
trainer = pycrfsuite.Trainer(verbose = False)
trainer.append(['我' , '爱' , '中' ,'国','共','产','党','！'] , ['s' , 's' ,'b' ,'m'  ,'m' ,'m' ,'e' , 's'])
trainer.set_params({
    'c1': 1.0,   # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 50,  # stop earlier

    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
    })
trainer.train('model.bin')
tagger = pycrfsuite.Tagger('model.bin')
print tagger.tag(['我' ,'爱' ,'中'])
