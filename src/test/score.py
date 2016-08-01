import sys
import json
import calendar
import datetime
sys.path.append("../")
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_vector_dict, load_corpus_dict
from package.relation import jm_score, dir_score, cos_score

stopword_set = load_stopword_set()
vector_dict  = load_vector_dict()
corpus_dict  = load_corpus_dict()

print "load query list ..."
query_list = []
for line in open('../../data/data15/origin.query'):
    t = line.strip().split('\t')
    query_json = {"topid":t[0], "title":t[1], "description":"", "narrative":""}
    query_json_str = json.dumps(query_json)
    query = Query(query_json_str, stopword_set, vector_dict)
    if query.is_valid and len(query.vector) == 100:
        query_list.append(query)
    else:
        print "ERROR: read query"
        exit()
print "load query list over"

print "load tweet list ..."
tweet_list = []
for line in open('/index15/preprocess/filter_raw_19_29.txt'):
    t = line.strip().split('\t')
    tweet = AdvancedTweet(t[0], t[1], t[2], t[3], vector_dict)
    if len(tweet.vector) == 100:
        tweet_list.append(tweet)
print "load tweet list over"

def overlap(query_stem_distri, tweet_stem_list):
    for w in tweet_stem_list:
        if w in query_stem_distri:
            return True
    return False

df = open("score.dat", "w")
for query in query_list:
    for tweet in tweet_list:
        if overlap(query.stem_distri, tweet.stem_list):
            score1 = jm_score(query, tweet, corpus_dict)
            score2 = dir_score(query, tweet, corpus_dict)
            score3 = cos_score(query, tweet)
            df.write("%s\t%s\t%.4f\t%.4f\t%.4f\n"%(query.id, tweet.id, score1, score2, score3))
df.close()



