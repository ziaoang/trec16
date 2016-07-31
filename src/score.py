#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     score.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-24 11:47:05
# MODIFIED: 2016-07-25 19:14:23

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import logging
import datetime
from package.advancedTweet import AdvancedTweet 
from package.query import Query
from package.relation import similarity_q_t
from package.utils import *
from os.path import isfile, isdir, join

print "---begin--"
stopword_set = load_stopword_set()
vector_dict = load_vector_dict()
corpus_dict = load_corpus_dict()
# ScenarioA
# query_list = load_query_list()
# ScenarioB
query_list = load_webexpansion_query()
selected_query_set = selected_queryid_set()
logging.basicConfig(filename='score.log', level=logging.INFO)
print "---end--"


def overlap(query_stem_list, tweet_stem_list):
    for w in tweet_stem_list:
        if w in set(query_stem_list):
            return True
    return False
    
def calculate_score(input_file):
    with open(input_file,'r') as fin:
        for i, line in enumerate(fin):
            if i % 1000 == 0: print i
            timestamp, id, plain_text, stem_list_str = line.strip().split("\t")
            tweet = AdvancedTweet(timestamp, id, plain_text, stem_list_str, vector_dict)
            cur_day = datetime.datetime.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y").day
            if cur_day < 20: continue
            write_dir = "../data/data15/score_expansion/"
            if not isdir(write_dir + str(cur_day)):
                cmd = "mkdir " + write_dir + str(cur_day)
                os.system(cmd)
            for query in query_list:
                if query.topid not in selected_query_set: continue
                if not overlap(query.stem_list, tweet.stem_list): continue
                write_file = write_dir + str(cur_day) + "/" + query.topid
                result = open(write_file, "a")
                jm = similarity_q_t(query, tweet, corpus_dict, "jm")
                dirichlet = similarity_q_t(query, tweet, corpus_dict, "dirichlet")
                if jm < -20 or dirichlet < -20:
                    log_string = "[" + tweet.id_str + "\t" + " ".join(tweet.stem_list) + "\t" + query.topid + "\t" + query.title + "\t" + str(jm) + "\t" + str(dirichlet) + "]"
                    logging.info(log_string)
                    continue
                string =  tweet.created_at + "\t" + tweet.id_str + "\t"  \
                          + " ".join(tweet.word_list) + "\t"             \
                          + " ".join(tweet.stem_list) + "\t"             \
                          + str(jm) + "\t" + str(dirichlet) + "\n"
                result.write(string)
                # result.close()                          


if __name__ == "__main__":
    input_file = "/index15/preprocess/filter_raw_expansion.txt"
    calculate_score(input_file)
