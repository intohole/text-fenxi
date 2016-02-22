#coding=utf-8



import os
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import collections
import json
import math
from b2 import file2
from optparse import OptionParser


def print_msg(msg):
    sys.stdout.write("%s\n" % msg)

def word_split(input_file_path  , save_path):
    word_freq = collections.defaultdict(int)
    lrc = file2.FilesRead(dirpath = input_file_path)
    for line in lrc:
        try:
            line = line.decode("gbk").encode("utf-8").split("]")
        except Exception ,e :
            continue
        if len(line) == 1:
            continue
        words = line[-1].replace("," ," ").replace("。" , " ").split()
        for word in words:
            word = word.decode("utf-8")
            # 使用2元文法
            if len(word) >1: 
                word_freq[word[-1]] += 1 
            for i in range(len(word)-1):
                cur_word = word[i : i + 2]
                word_freq[word[i]] += 1
                print_msg("%s\t%s\t%s" % ( cur_word , "word" , 1))
                if i != 0: 
                    # 左邻字
                    print_msg("%s\t%s\t%s" % (cur_word , "left" ,word[i-1]))
                if i < (len(word) -2):
                    # 右邻字
                    print_msg("%s\t%s\t%s" % (cur_word , "right" ,word[i + 2]))
    with open(save_path,"w") as f:
        f.write("sum\t%s\n"  % sum(word_freq.values()))
        for word,count in word_freq.items():
            f.write("%s\t%s\n" % (word , count)) 



def entropy( probs ):
    if isinstance(probs , (list , tuple)) is False or len(probs) == 0:
        return None
    return sum([ -prob * math.log(prob,2) for prob in probs])

def word_rec(dict_path , word_limit , left_entropy_limit , right_entropy_limit):
    word_freq = collections.defaultdict(int)
    with open(dict_path) as f:
        word_sum = float(f.readline().rstrip().split("\t")[1]) 
        for line in f.readlines():
            word , freq = line.rstrip().split("\t")
            word_freq[word.decode("utf-8")] = int(freq)

    last_word = ""
    word_count = 0
    word_left = collections.defaultdict(int) 
    word_right = collections.defaultdict(int)
    for line in sys.stdin:
        line = line.rstrip().split("\t")
        if len(line) != 3:
            continue
        word , sign , value = line 
        word = word.decode("utf-8")

        if last_word != word:
            if last_word != "":
                word_rate = word_count / word_sum 
                if word_rate / (word_freq[word[0]] /word_sum * word_freq[word[1]]/word_sum) > word_limit:
                    left_entropy = 1 
                    if len(word_left) >0:
                        left_sum = float(sum(word_left.values()))
                        left_entropy =  entropy([ l/left_sum  for l in word_left.values()])
                    right_entropy = 1 
                    if len(word_right) >0:
                        right_sum = float(sum(word_left.values()))
                        right_entropy =  entropy([ l/right_sum  for l in word_right.values()])
                    if left_entropy > left_entropy_limit and right_entropy > right_entropy_limit: 
                        print last_word,left_entropy,right_entropy 
            last_word = word 
            word_count = 0
            word_left.clear()
            word_right.clear()
        if sign == "word":
            word_count += 1
        elif sign == "left":
            value = value.decode("utf-8")
            word_left[value] += 1
        elif sign == "right":
            value = value.decode("utf-8")
            word_right[value] += 1

def main(input_file ,  dict_path = None , word_limit = 100 , left_entropy_limit = 1.0 , right_entropy_limit= 1.0):
    import subprocess
    import os 
    cwd = os.path.abspath(os.path.dirname(__file__))
    dict_path = os.path.join(cwd , "word.freq") if dict_path is None else dict_path 
    script_file = os.path.join(cwd , os.path.basename(__file__)) 
    commands = ["python" , script_file , "-m" , "pre" , "-i" ,input_file , "-d" , dict_path ]
    read_pipe = subprocess.Popen(commands ,stdout = subprocess.PIPE )
    sort_pipe = subprocess.Popen("sort" , stdin = read_pipe.stdout , stdout = subprocess.PIPE)
    sort_pipe.wait()
    sys.exit(0)
    commands1 = ["python" , script_file , "-m" , "rec" , "-d" , dict_path , "-w" , str(word_limit) , "-l" , str(left_entropy_limit) ,"-r", str(right_entropy_limit) ]
    rec_pipe = subprocess.Popen(commands1 , stdin = sort_pipe.stdout )
    rec_pipe.wait()

if __name__ == "__main__":
    opts = OptionParser()
    opts.add_option("-m" , "--method" , help = "选择文件方法选项" , dest = "method" , default = "main")
    opts.add_option("-i" , "--input" , help = "需要新词识别的文档路径" , dest = "input" , default = "" )
    opts.add_option("-d" , "--dict" , help = "词典文件（单字频率信息）保存路径" , dest = "dict"  , default = None )
    opts.add_option("-w" , "--word-limit" , help = "出现最小词频" , dest = "word_limit" , default = 100)
    opts.add_option("-l", "--left-entropy-limit" , help = "新词最小左熵限制" , dest = "left_entropy_limit" , default = 1.0 )
    opts.add_option("-r", "--right-entropy-limit" , help = "新词最小右熵限制" , dest = "right_entropy_limit" , default = 1.0) 
    (config , args) = opts.parse_args(sys.argv)
    print config
    if config.method == "main":
        main(config.input , config.dict , config.word_limit , config.left_entropy_limit , config.right_entropy_limit)
    elif config.method == "pre":
        word_split(config.input , config.dict)
    elif config.method == "rec":
        word_rec(config.dict , config.word_limit , config.left_entropy_limit , config.right_entropy_limit) 
