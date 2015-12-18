#coding=utf-8





from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet 
from pybrain.supervised.trainers import BackpropTrainer
import random
# create nerual net work  , with one input layer , one hidden layer , one outputlayer 
net = buildNetwork( 2 , 2 ,1,bias= True)
ds = SupervisedDataSet(2 , 1)
data = []
data.append([(0 ,0) ,(0,)])
data.append([(0 ,1) ,(1,)])
data.append([(1 ,1) ,(0,)])
data.append([(1 ,0) ,(1,)])
data.append([(0 ,0) ,(0,)])
for i in xrange(10000):
    index = random.randint(0,4)    
    ds.addSample(data[index][0] ,data[index][1] )
trainer = BackpropTrainer(net , ds)
trainer.trainEpochs()
print net.activate((0,0))
print net.activate((1 ,0))
