#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     novelty.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-28 16:46:13
# MODIFIED: 2016-07-28 16:46:14

import datetime
from os import listdir
from os.path import isfile, join
from package.advancedTweet import AdvancedTweet
from package.relation import similarity_t_t
from package.utils import load_vector_dict
from scenarioA import novel_strategy

vector_dict = load_vector_dict()


def single_file(file_path, file, method, nol):
    queue = []
    day_dict = {}
    write_file = "../data/data15/res/N/" + file + "_N" + str(nol)
    result = open(write_file, "w")
    with open(file_path, "r") as fin:
        for line in fin:
            timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
            tweet = AdvancedTweet(timestamp, id, plain_text, stem_text, vector_dict)
            
            cur_day = datetime.datetime.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y").day
            
            # Add current tweet to queue
            if len(queue) == 0 or cur_day not in day_dict: 
                queue.append(tweet)
                day_dict[cur_day] = 1
                string =  timestamp + "\t" + id      + "\t" + plain_text     + "\t" + \
                          stem_text + "\t" + str(jm) + "\t" + str(dirichlet) + "\n"
                result.write(string)
                continue
                
            # Continue when cur_day queue size more than 10
            if day_dict[cur_day] == 10: continue 
            
            # Whether current tweet can add to queue
            score = novel_strategy(1, tweet, queue, method)
            if score < nol:
                queue.append(tweet)
                day_dict[cur_day] += 1
                string =  timestamp + "\t" + id      + "\t" + plain_text     + "\t" + \
                          stem_text + "\t" + str(jm) + "\t" + str(dirichlet) + "\n"
                result.write(string)
    
            

if __name__ == "__main__":
    base_path = "../data/data15/res/R/"
    file_names = [f for f in listdir(base_path) if isfile(join(base_path, f))]
    file_names.sort()
    for file in file_names:
        # Use for test
        # if file.strip().split("_")[0] != "MB236": continue
        
        if "J" in file:
            method = "jm"
        else: method = "dirichlet"
        full_path = base_path + file
        for nol in [0.75, 0.8, 0.85, 0.9]:
            print "file: %s, nol: %f", (file, nol)
            single_file(full_path, file, method, nol)
            
            