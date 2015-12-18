#coding=utf-8




from b2 import file2
import os

class FilesRead1(file2.FilesRead):



    def change_file(self , filepath ):
        print os.path.split(filepath )

filesread = FilesRead1(dirpath = "texts/Reduced")

while filesread.get_line()  != None:
    continue
