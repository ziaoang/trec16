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
from package.utils import load_vector_dict
from scenarioA import novel_strategy

vector_dict = load_vector_dict()


def single_file(file_path, topk, day, topid, nol, write_dir):
    topk_path = write_dir + topk + "_N" + str(nol)
    if not isdir(topk_path):
        cmd = "mkdir " + topk_path
        os.system(cmd)
    if not isdir(topk_path + "/" + day):
        cmd = "mkdir " + topk_path + "/" + day
        os.system(cmd)
        
    write_path = topk_path + "/" + day + "/" + topid
    write_file = open(write_path, "w")

    queue = []
    with open(file_path, "r") as fin:
        for line in fin:
            timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
            tweet = AdvancedTweet(timestamp, id, plain_text, stem_text, vector_dict)
            
            # Add current tweet to queue
            if len(queue) == 0: 
                queue.append(tweet)
                string = timestamp + "\t" + id + "\t" + plain_text + "\t" + \
                         stem_text + "\t" + jm + "\t" + dirichlet  + "\n"
                write_file.write(string)
                continue
                
            # Break when queue size more than 10
            if len(queue) == 10: break 
            
            # Whether current tweet can add to queue
            score = novel_strategy(1, tweet, queue, "dirichlet")
            if score < nol:
                queue.append(tweet)
                string = timestamp + "\t" + id + "\t" + plain_text + "\t" + \
                         stem_text + "\t" + jm + "\t" + dirichlet  + "\n"
                write_file.write(string)
    
            

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input one stage candidate dir"
        print "sys.argv[2]: Output two stage candidate dir!"
        exit()
              
    topk_names = [topk for topk in listdir(sys.argv[1]) if isdir(join(sys.argv[1], topk))] 
    topk_names.sort()
    for topk in topk_names:
        cur_path = sys.argv[1] + topk + "/"
        day_names = [day for day in listdir(cur_path) if isdir(join(cur_path, day))]
        day_names.sort()
        for day in day_names:
            second_path = cur_path + day + "/"           
            topid_names = [topid for topid in listdir(second_path) if isfile(join(second_path, topid))]
            topid_names.sort()
            for topid in topid_names:
                full_path = second_path + topid
                print full_path
                for nol in [0.55, 0.6, 0.65, 0.7, 0.75]:
                    single_file(full_path, topk, day, topid, nol, sys.argv[2])



            