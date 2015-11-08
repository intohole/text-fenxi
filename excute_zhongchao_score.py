#coding=utf-8





#从sklearn引入线性模型，用于回灌数据
from sklearn import linear_model


# 为了防止过拟合，使用l1正则化 ；
with open("data1/zhongchao_2014.txt") as f:
    x = []
    y = []
    for line in f.readlines():
        line = line.rstrip()
        features = line.split()[1:]
        features = map(  lambda x : float(x) , features )
        x.append(features[:-1])
        y.append(features[-1])
    """
       刚才没有进行这个步骤的时候，数据在这个点并没有表现好，回归模型主要是通过不断迭代参数，所以需要数据
       复制一批低分链接，将整体阈值拉低 ；
    """
    x.append(x[-2])
    y.append(y[-2])
    x.append(x[-2])
    y.append(y[-2])
    x.append(x[-1])
    y.append(y[-1])
    x.append(x[-1])
    y.append(y[-1])
lg = linear_model.LogisticRegression(C = 2.0 , penalty = "l1")
lg.fit(x[:-1] , y[:-1])
print lg.coef_
print lg.predict(x[-1]),y[-1]
