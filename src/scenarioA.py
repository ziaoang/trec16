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
    text = ''
    try:
        status = json.loads(status_json) 
        if status.has_key('created_at') and status['lang'] == 'en':
            origin_text = status['text'].replace('\n','').replace('\t','')
            processed_tokens = preprocess(status['text'])
            if len(processed_tokens) >= 5:
                text = ' '.join(processed_tokens)
    except Exception, e:
        print 'Error: ' + str(e)
        exit()
    return text
    

def pipeline(tweet_json):
    try:
        print "pipeline begin"
        text = extract_status(tweet_json)
        if text != '':
            tweet = Tweet(text)
            query_list = get_topics("data/data15/topic.txt")
            for query in query_list:
                rel_score = similarity_q_t(query, tweet)
                #nol_score = similarity_t_t()
        print "pipeline end"
        
    except ValueError, e:
        print str(e)
        

    