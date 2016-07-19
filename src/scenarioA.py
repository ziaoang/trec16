#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     scenarioA.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-18 20:43:56
# MODIFIED: 2016-07-18 20:43:58

import json
from src.read_topic import get_topics
from src.utils import preprocess
from src.classes.tweet import Tweet
from src.classes.relation import *


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
        print 'Error: ' + str(e)
        exit()
    return tweet_info
    
def get_recommend_queue(query_id):
    queue = []
    file_path = "src/result/" + query_id
    try:
        with open(file_path, "r") as fin:
            for i, line in enumerate(fin):
                tweet_id, timestamp, text = line.strip().split("\t")
                if tweet_id in queue:
                    print "Duplicated tweet_id in queue!"
                    exit()
                queue.append(Tweet(tweet_id, timestamp, text))
    except Exception, e:
        print str(e)
        exit()
    return queue    
        
def update_recommend_queue(query_id, tweet):
    file_path = "src/result/" + query_id
    try:
        result = open(file_path, "a")
        result.write(tweet.id + "\t" + tweet.timestamp + "\t" + tweet.text + "\n")
        result.close()
    except Exception, e:
        print str(e)
        exit()
    
def pipeline(tweet_json):
    try:
        print "pipeline begin"
        tweet_info = extract_status(tweet_json)
        if len(tweet_info) == 3:
            tweet = Tweet(tweet_info[0], tweet_info[1], tweet_info[2])
            query_list = get_topics("data/data15/topic.txt")
            for query in query_list:
                rel_score = similarity_q_t(query, tweet)
                cur_queue = get_recommend_queue(query.id)
                #remain TO DO
                #nol_score = similarity_t_t()
        
        
    except ValueError, e:
        print str(e)
        

    