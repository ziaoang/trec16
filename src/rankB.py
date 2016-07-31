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
from package.utils import load_vector_dict, selected_queryid_set
from scenarioA import novel_strategy


vector_dict = load_vector_dict()
topid_set = selected_queryid_set()
queue = {}
for topid in topid_set:
    queue[topid] = {}


def single_file(file_path, day, topid, nol, write_dir):
    path = write_dir + "N" + str(nol) + "/"
    if not isdir(path):
        cmd = "mkdir " + path
        os.system(cmd)
    if not isdir(path + day):
        cmd = "mkdir " + path + day
        os.system(cmd)
    write_path = path + day + "/" + topid
    write_file = open(write_path, "w")
    res_list = []
    
    # Read and sorted by dirichlet 
    fin = open(file_path, "r")
    for line in fin:
        timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
        tweet = AdvancedTweet(timestamp, id, plain_text, stem_text, vector_dict)
        candidate = Candidate(tweet, jm, dirichlet)
        res_list.append(candidate)
    res_list.sort(key = lambda x: x.dirichlet, reverse = True)
    
    cur_queue = []

    # Write top10 to another file
    for i in range(0, len(res_list)):
        
        tweet = res_list[i].tweet
        timestamp = tweet.created_at
        id = tweet.id_str
        plain_text = " ". join(tweet.word_list)
        stem_text = " ". join(tweet.stem_list)
        jm = res_list[i].jm
        dirichlet = res_list[i].dirichlet
        
        recommend_histroy = []
        for key in queue[topid]:
            if int(key) < int(day) and int(key) > 19:
                recommend_histroy += queue[topid][key]
        
        # Add current tweet to cur_queue
        if len(recommend_histroy) == 0 and len(cur_queue) == 0: 
            cur_queue.append(tweet)
            string = timestamp + "\t" + id + "\t" + \
                     plain_text + "\t" + stem_text + "\t" + \
                     jm + "\t" + dirichlet + "\n"
            write_file.write(string)
            continue
            
        # Break when cur_queue size more than 10
        if len(cur_queue) >= 10: break

        # Whether current tweet can add to cur_queue
        recommend_histroy += cur_queue
        score = novel_strategy(1, tweet, recommend_histroy, "dirichlet")
        if score < nol:
            string = timestamp + "\t" + id + "\t" + \
                     plain_text + "\t" + stem_text + "\t" + \
                     jm + "\t" + dirichlet + "\n"
            write_file.write(string)    
            cur_queue.append(tweet)
            
    queue[topid][day] = cur_queue
    fin.close()   
    write_file.close()
    
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input scenarioB candidate dir!"
        print "sys.argv[2]: Output result dir"
        exit()
          
    day_names = [day for day in listdir(sys.argv[1]) if isdir(join(sys.argv[1], day))]  
    day_names.sort()
    for day in day_names:
        if int(day) < 20: continue
        cur_path = sys.argv[1] + day + "/"
        topid_names = [topid for topid in listdir(cur_path) if isfile(join(cur_path, topid))]  
        for topid in topid_names:
            full_path = cur_path + topid
            print full_path
            for nol in [0.71, 0.73, 0.75]:
                single_file(full_path, day, topid, nol, sys.argv[2])
    