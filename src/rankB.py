#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     rankB.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-29 17:30:26
# MODIFIED: 2016-07-29 17:30:27

import sys
import os
import datetime
from os import listdir
from os.path import isfile, join, isdir
from package.candidate import Candidate
from package.advancedTweet import AdvancedTweet
from package.utils import load_vector_dict

vector_dict = load_vector_dict()

def single_file(file_path, dir, file, write_dir):
    fin = open(file_path, "r")
    if not isdir(write_dir + dir):
        cmd = "mkdir " + write_dir + dir
        os.system(cmd)
    write_path = write_dir + dir + "/" + file
    write_file = open(write_path, "w")
    res_list = []
    
    # Read and sorted by dirichlet 
    for line in fin:
        timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
        tweet = AdvancedTweet(timestamp, id, plain_text, stem_text, vector_dict)
        candidate = Candidate(tweet, jm, dirichlet)
        res_list.append(candidate)
    res_list.sort(key = lambda x: x.dirichlet, reverse = True)
    
    # Write top10 to another file
    for i in range(0, len(res_list)):
        if i >= 10: break
        timestamp = res_list[i].tweet.created_at
        id = res_list[i].tweet.id_str
        plain_text = " ". join(res_list[i].tweet.word_list)
        stem_text = " ". join(res_list[i].tweet.stem_list)
        jm = res_list[i].jm
        dirichlet = res_list[i].dirichlet
        string =  timestamp + "\t" + id + "\t" + plain_text + "\t" + \
                  stem_text + "\t" + jm + "\t" + dirichlet  + "\n"
        write_file.write(string)
    
    fin.close()   
    write_file.close()
        
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input candidate dir!"
        print "sys.argv[2]: Output result dir"
        exit()
          
    dir_names = [dir for dir in listdir(sys.argv[1]) if isdir(join(sys.argv[1], dir))]    
    for dir in dir_names:
        cur_path = sys.argv[1] + dir + "/"
        file_names = [f for f in listdir(cur_path) if isfile(join(cur_path, f))]  
        for file in file_names:
            full_path = cur_path + file
            print full_path
            single_file(full_path, dir, file, sys.argv[2])
    