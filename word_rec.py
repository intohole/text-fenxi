#coding=utf-8



import os
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import collections
import json

def word_split(save_path):
    word_freq = collections.defaultdict(int)
    for dirpath , dirnames , filenames in os.walk('texts/lrc'):
        for filename in filenames:
            with open(os.path.join(dirpath , filename)) as f:
                for line in f.readlines():
                    try:
                        line = line.decode("gbk").encode("utf-8").rstrip().split("]")
                    except:
                        continue 
                    if len(line ) == 1:
                        continue
                    words = line[-1].replace("," ," ").replace("。", " ").split()
                    for word in words:
                        word = word.decode("utf-8")
                        # 使用2元文法
                        if len(word) >1: 
                            word_freq[word[-1]] += 1 
                        for i in range(0 ,len(word)-1):
                            cur_word = word[i : i + 2]
                            word_freq[word[i]] += 1
                            print "%s\t%s\t%s" % ( cur_word , "word" , 1)
                            if i != 0: 
                                # 左邻字
                                print "%s\t%s\t%s" % (cur_word , "left" ,word[i-1])
                            if i < (len(word) -2):
                                # 右邻字
                                print "%s\t%s\t%s" % (cur_word , "right" ,word[i + 2])
    with open(save_path,"w") as f:
        f.write("sum\t%s\n"  % sum(word_freq.values()))
        for word,count in word_freq.items():
            f.write("%s\t%s\n" % (word , count)) 

def word_rec(dict_path , word_limit):
    word_freq = collections.defaultdict(int)
    with open(dict_path) as f:
        word_sum = float(f.readline().rstrip().split("\t")[1]) 
        for line in f.readlines()[1:]:
            word , freq = line.rstrip().split("\t")
            word_freq[word.decode("utf-8")] = int(freq)

    last_word = ""
    word_count = 0
    word_left = collections.defaultdict(int) 
    word_right = collections.defaultdict(int)
    for line in sys.stdin:
        word , sign , freq = line.rstrip().split("\t") 
        word = word.decode("utf-8")

        if last_word != word:
            if last_word != "":
                word_rate = word_count / word_sum 
                if word_rate / (word_freq[word[0]] /word_sum * word_freq[word[1]]/word_sum) > word_limit:
                    print last_word 
            last_word = word 
            word_count = 0
        if sign == "word":
            word_count += 1


if __name__ == "__main__":
    if sys.argv[1] == "wordsplit":
        word_split(sys.argv[2])
    elif sys.argv[1] == "wordrec":
       word_rec(sys.argv[2] , float(sys.argv[3])) 
