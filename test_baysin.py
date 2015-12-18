#coding=utf-8




from moodstyle import cool
from b2 import file2

class ReadFile(file2.FilesRead):

    def __init__(self , **kw , *argv):
        super(ReadFile , self).__init__(**kw , *argv)
        self.content = []
   
    
    def change_file(self , file_path):
        pass


classifier = cool.testBayes.Bayes()
classifier.train()
classifier.predict()
