#coding=utf-8





from sklearn import linear_model



liner = linear_model.Ridge(alpha = 0.5 )

liner.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
print liner.predict([1,0])

