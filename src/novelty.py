#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     novelty.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-28 16:46:13
# MODIFIED: 2016-07-28 16:46:14

import os
import sys
import datetime
from os import listdir
from os.path import isfile, isdir, join
from package.advancedTweet import AdvancedTweet
from package.relation import similarity_t_t
from package.utils import load_vector_dict, selected_queryid_set
from scenarioA import novel_strategy

vector_dict = load_vector_dict()
topid_set = selected_queryid_set()
queue = {}
for topid in topid_set:
    queue[topid] = {}

def single_file(file_path, topk, day, topid, nol, write_dir):
    topk_path = write_dir + topk + "_" + str(nol)
    if not isdir(topk_path):
        cmd = "mkdir " + topk_path
        os.system(cmd)
    if not isdir(topk_path + "/" + day):
        cmd = "mkdir " + topk_path + "/" + day
        os.system(cmd)
        
    write_path = topk_path + "/" + day + "/" + topid
    write_file = open(write_path, "w")

    cur_queue = []
    with open(file_path, "r") as fin:
        for line in fin:
            timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
            tweet = AdvancedTweet(timestamp, id, plain_text, stem_text, vector_dict)
            
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
            if score < float(nol.split("N")[1]):
                string = timestamp + "\t" + id + "\t" + \
                         plain_text + "\t" + stem_text + "\t" + \
                         jm + "\t" + dirichlet + "\n"
                write_file.write(string)    
                cur_queue.append(tweet)
                
    queue[topid][day] = cur_queue

            

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input one stage candidate dir"
        print "sys.argv[2]: Output two stage candidate dir!"
        exit()
    
    nol_names = [nol for nol in listdir(sys.argv[1]) if isdir(join(sys.argv[1], nol))]
    nol_names.sort()
    for nol in nol_names:
        path = sys.argv[1] + nol + "/"
        topk_names = [topk for topk in listdir(path) if isdir(join(path, topk))] 
        topk_names.sort()
        for topk in topk_names:
            cur_path = path + topk + "/"
            day_names = [day for day in listdir(cur_path) if isdir(join(cur_path, day))]
            day_names.sort()
            for day in day_names:
                second_path = cur_path + day + "/"           
                topid_names = [topid for topid in listdir(second_path) if isfile(join(second_path, topid))]
                topid_names.sort()
                for topid in topid_names:
                    full_path = second_path + topid
                    print full_path
                    single_file(full_path, topk, day, topid, nol, sys.argv[2])



            