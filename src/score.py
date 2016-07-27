#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     score.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-24 11:47:05
# MODIFIED: 2016-07-25 19:14:23

import gzip
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
from datetime import datetime
from package.tweet import Tweet
from package.query import Query
from package.relation import kl_jm, kl_dirichlet
from package.utils import load_stopword_set, load_vector_dict, load_corpus_dict
from scenarioA import get_topics
from corpus import conver
import logging

logging.basicConfig(filename='score.log', level=logging.INFO)

# remain to figure out
print "---begin--"
stopword_set = load_stopword_set()
vector_dict = load_vector_dict()
corpus_dict = load_corpus_dict()
query_list = get_topics("../data/data15/topic.txt")
selected_query = [339,243,242,331,392,391,389,278,253,236,254,255,379,344,405,354,326,324,400,366,348,284,287,448,401,305,262,260,267,265,228,227,226,409,249,248,383,362,357,416,246,353,377,298,439,371,384,434,432,419,359]
full_seleted = []
for id in selected_query:
    full_seleted.append("MB" + str(id))
selected_query_set = set(full_seleted)
print "---end--"

def normalize(score):
    max = 0.0
    min = -20.0
    return float(score - min) / (max - min)

def list_to_string(stem_list):
    res = ""
    for word in stem_list:
        res += word + " "
    return res
    
def calculate_score(input_file):
    try: 
        with gzip.open(input_file,'r') as fin:
            for i, line in enumerate(fin):
                if i % 100 == 0: print i
                tweet = Tweet(line, stopword_set, vector_dict)
                if tweet.is_valid:
                    for query in query_list:
                        if query.topid not in selected_query_set: continue
                        write_file = "../data/data15/score/" + query.topid
                        result = open(write_file, "a")
                        jm = kl_jm(query.stem_distri, tweet.stem_distri, corpus_dict, 0.2)
                        dirichlet = kl_dirichlet(query.stem_distri, tweet.stem_distri, corpus_dict, 100, len(tweet.stem_list))
                        if jm < -20 or dirichlet < -20:
                            log_string = "[tweet text: " + tweet.plain_text + ", query title: " + query.title + ", jm_score: " + str(jm) + ", dirichlet: " + str(dirichlet) + "]"
                            logging.info(log_string)
                            continue
                        #normalize
                        jm_normal = normalize(jm)
                        dirichlet_normal = normalize(dirichlet)
                        avg = (jm_normal + dirichlet_normal) / 2
                        string =  tweet.created_at + "\t" + tweet.lang            + "\t" \
                                  + tweet.id_str   + "\t" + tweet.plain_text      + "\t" \
                                  + list_to_string(tweet.stem_list)               + "\t" \
                                  + str(jm_normal) + "\t" + str(dirichlet_normal) + "\n"
                        result.write(string)
                        # result.close()                          
    except Exception as e:
        print str(e) 


if __name__ == "__main__":
    for day in range(20, 30):
        print "Current day: ", day
        for hour in range(0, 24):
            hour = conver(hour)
            print "Current hour: ", hour
            input_file = "/index15/raw/statuses.log.2015-07-" + str(day) + "-" + str(hour) + ".gz"
            calculate_score(input_file)
