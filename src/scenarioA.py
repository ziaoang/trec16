#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     scenarioA.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-18 20:43:56
# MODIFIED: 2016-07-19 19:56:54

import json
import time
from datetime import datetime
import pytz
from src.read_topic import get_topics
from src.utils import preprocess
from src.classes.tweet import Tweet
from src.classes.query import Query
from src.classes.relation import *

log = open("log.txt", "a+")
log.write("----------------------\n")

def extract_status(status_json):
    tweet_info = []
    try:
        status = json.loads(status_json) 
        if status.has_key('created_at') and status['lang'] == 'en':
            origin_text = status['text'].replace('\n','').replace('\t','')
            processed_tokens = preprocess(status['text'])
            if len(processed_tokens) >= 5:
                text = ' '.join(processed_tokens)
                id = status['id_str']
                timestamp = status['created_at']
                tweet_info = [id, timestamp, text]
    except Exception, e:
        print 'Error in extract_status(): ' + str(e)
        exit()
    return tweet_info
    

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


def get_recommend_queue(query_id):
    queue = []
    file_path = "src/result/" + query_id
    try:
        with open(file_path, "r") as fin:
            for i, line in enumerate(fin):
                tweet_id, timestamp, text, recommend_time = line.strip().split("\t")
                if tweet_id in queue:
                    print "Duplicated tweet_id in queue!"
                    exit()
                queue.append(Tweet(tweet_id, timestamp, text))
    except Exception, e:
        print 'Error in get_recommend_queue(): '+ str(e)
        exit()
    return queue    
        

def update_recommend_queue(query_id, tweet):
    file_path = "src/result/" + query_id
    try:
        result = open(file_path, "a")
        cur_time = datetime.datetime.utcnow()
        string = tweet.id + "\t" + tweet.timestamp + "\t" \
                 + tweet.text + "\t" + str(cur_time) + "\n"
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
        s1 = similarity_t_t(cur_tweet, tweet)
        s2 = similarity_t_t(tweet, cur_tweet)
        score = float(s1 + s2) / 2
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
        tweet_info = extract_status(tweet_json)
        if len(tweet_info) == 3:
            tweet = Tweet(tweet_info[0], tweet_info[1], tweet_info[2])
            query_list = get_topics("data/data15/topic.txt")
            threshold_dict = get_threshold("src/data/threshold.txt")
            for query in query_list:
                rel_score = similarity_q_t(query, tweet)
                day_delta = day_index(2016, 8, 2)
                # use for test
                # if day_delta >= len(threshold_dict[query._topid]) or day_delta < 0:
                if query._topid not in threshold_dict:
                    print "Current query topid: " + query._topid + " not in threshold_dict!"
                    exit()
                if day_delta >= len(threshold_dict[query._topid]):
                    print "day_delta invalid!"
                    exit()
                # use for test
                if day_delta < 0: day_delta = 0
                rel_nol_pair = threshold_dict[query._topid][day_delta].strip().split("/")
                if len(rel_nol_pair) != 2:
                    print "Current query topid: " + query._topid + " rel_nol_pair split error!"
                    exit()
                rel_threshold = rel_nol_pair[0]
                nol_threshold = rel_nol_pair[1]

                if rel_score < rel_threshold:
                    continue
                cur_queue = get_recommend_queue(query._topid)
                if len(cur_queue) == 0:
                    update_recommend_queue(query._topid, tweet)
                    log_string = "tweet text: " + tweet._text + ", query title: " + query._topid + ", rel_score: " + str(rel_score) + "\n"
                    log.write(log_string)
                else:
                    # remain TO TEST
                    nol_score = novel_strategy(1, tweet, cur_queue)
                    nol_score = novel_strategy(2, tweet, cur_queue)
                    nol_score = novel_strategy(3, tweet, cur_queue)
                    if nol_score < nol_threshold:
                        update_recommend_queue(query._topid, tweet)
                        log_string = "tweet text: " + tweet._text + ", query title: " + query._topid + ", rel_score: " + str(rel_score) + ", nol_score: " + str(nol_score) + "\n"
                        log.write(log_string)
        print "pipeline end"
    except ValueError, e:
        print 'Error in pipeline(): '+ str(e)
        

    
