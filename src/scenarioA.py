#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     scenarioA.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-18 20:43:56
# MODIFIED: 2016-07-19 19:56:54

import json
import time
from datetime import datetime
from package.query import Query
from package.tweet import Tweet
from package.relation import similarity_q_t, similarity_t_t
from package.utils import load_stopword_set, load_vector_dict, load_corpus_dict
import logging

logging.basicConfig(filename='scenarioA.log', level=logging.INFO)

stopword_set = load_stopword_set()
vector_dict = load_vector_dict()
corpus_dict = load_corpus_dict()

def get_topics(file_path):
    query_list = []
    try:
        content = open(file_path).read()
        query_json_list = json.loads(content)
        for query_json in query_json_list:
            query_json_string = json.dumps(query_json)
            query = Query(query_json_string, stopword_set, vector_dict)
            if query.topid != None:
                query_list.append(query)
    except Exception, e:
        print "Error in get_topics(), " + str(e)
    return query_list
    

def get_threshold(file_path):
    result = {}
    try:
        with open(file_path, "r") as fin:
            for i, line in enumerate(fin):
                content = line.strip().split("\t")
                if len(content) >= 2:
                    query_id = content[0]
                    if query_id in result:
                        print "Duplicated query_id in threshold file!"
                        exit()
                    result[query_id] = content[1:]
                else:
                    print "Threshold file format wrong!"
                    exit()
    except Exception, e:
        print 'Error in get_threshold(): '+ str(e)
        exit()
    return result


def get_recommend_queue(file_path):
    queue = []
    tweet_dict = {}
    try:
        with open(file_path, "r") as fin:
            for i, line in enumerate(fin):
                timestamp, lang, id, text, recommend_time = line.strip().split("\t")
                tweet_dict['created_at'] = timestamp
                tweet_dict['lang'] = lang
                tweet_dict['id_str'] = id
                tweet_dict['text'] = text
                tweet_json = json.dumps(tweet_dict)
                queue.append(Tweet(tweet_json, stopword_set, vector_dict))
    except Exception, e:
        print 'Error in get_recommend_queue(): '+ str(e)
        exit()
    return queue    
        

def update_recommend_queue(file_path, tweet):
    try:
        result = open(file_path, "a")
        cur_time = datetime.utcnow()
        string =  tweet.created_at + "\t" + tweet.lang + "\t" \
                  + tweet.id_str + "\t" + tweet.text + "\t"   \
                  + str(cur_time) + "\n"
        result.write(string)
        result.close()
    except Exception, e:
        print 'Error in update_recommend_queue(): ' + str(e)
        exit()
       

def day_index(year, month, day):
    start_time = datetime(year, month, day, 0, 0)
    # start_time = start_time.replace(tzinfo=pytz.utc)
    cur_time = datetime.utcnow()
    return (cur_time - start_time).days
    


"""
Calculate the novelty score between current tweet and tweets in recommend queue  
:param strategy: only 1, 2, 3 are valid, 1:max, 2:min, 3:avg
:param cur_tweet: current tweet   
:param cur_queue: tweets in recommend queue 
:return: novelty score according to different strategy
"""
def novel_strategy(strategy, cur_tweet, cur_queue):
    if strategy not in [1, 2, 3]:
        print "Wrong strategy label!"
        exit()
    score_list = []
    min_score = 99999.0
    max_score = 0.0
    sum_score = 0.0
    for tweet in cur_queue:
        score = similarity_t_t(cur_tweet, tweet, corpus_dict)
        score_list.append(score)
        if score > max_score: max_score = score
        if score < min_score: min_score = score
        sum_score += score
    avg_score = float(sum_score) / len(score_list)    
    if strategy == 1: return max_score
    if strategy == 2: return min_score
    if strategy == 3: return avg_score
    
    
    
def pipeline(tweet_json):
    try:
        print "pipeline begin"
        tweet = Tweet(tweet_json, stopword_set, vector_dict)
        if tweet.created_at != None and tweet.lang == 'en':
            query_list = get_topics("../data/data15/topic.txt")
            threshold_dict = get_threshold("../data/data16/threshold.txt")
            for query in query_list:
                if query.topid not in threshold_dict:
                    print "Current query topid: " + query.topid + " not in threshold_dict!"
                    exit()
                rel_score = similarity_q_t(query, tweet, corpus_dict)
                
                # Get relevance and novelty threshold
                day_delta = day_index(2016, 8, 2)
                # if day_delta >= len(threshold_dict[query.topid]) or day_delta < 0:
                if day_delta >= len(threshold_dict[query.topid]):
                    print "day_delta invalid!"
                    exit()
                if day_delta < 0: day_delta = 0    
                
                rel_nol_pair = threshold_dict[query.topid][day_delta].strip().split("/")
                if len(rel_nol_pair) != 2:
                    print "Current query topid: " + query.topid + " rel_nol_pair split error!"
                    exit()
                rel_threshold = rel_nol_pair[0]
                nol_threshold = rel_nol_pair[1]

                # Compare with two thresholds
                if rel_score < rel_threshold:
                    continue
                # ScenarioB keep all relevant tweets
                file_path = "../data/data16/B/" + query.topid
                update_recommend_queue(file_path, tweet)
                
                # ScenarioA still need to compare with novelty threshold
                file_path = "../data/data16/A/" + query.topid
                cur_queue = get_recommend_queue(file_path)
                if len(cur_queue) == 0:
                    update_recommend_queue(file_path, tweet)
                    log_string = "[tweet text: " + tweet.text + ", query title: " + query.topid + ", rel_score: " + str(rel_score) + "]"
                    logging.info(log_string)
                else:
                    # remain TO TEST
                    nol_score = novel_strategy(1, tweet, cur_queue)
                    nol_score = novel_strategy(2, tweet, cur_queue)
                    nol_score = novel_strategy(3, tweet, cur_queue)
                    if nol_score < nol_threshold:
                        update_recommend_queue(file_path, tweet)
                        log_string = "[tweet text: " + tweet.text + ", query title: " + query.topid + ", rel_score: " + str(rel_score) + ", nol_score: " + str(nol_score) + "]"
                        logging.info(log_string)
        print "pipeline end"
    except ValueError, e:
        print 'Error in pipeline(): '+ str(e)
        exit()
        

    
