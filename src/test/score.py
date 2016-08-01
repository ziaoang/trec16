import sys
import json
import calendar
import datetime
sys.path.append("../")
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_corpus_dict
from package.relation import jm2_score, jm5_score, dir_score

stopword_set = load_stopword_set()
corpus_dict  = load_corpus_dict()

print "load query list ..."
query_list = []
for line in open('../../data/data15/origin.query'):
    t = line.strip().split('\t')
    query_json = {"topid":t[0], "title":t[1], "description":"", "narrative":""}
    query_json_str = json.dumps(query_json)
    query = Query(query_json_str, stopword_set)
    if query.is_valid:
        query_list.append(query)
    else:
        print "ERROR: read query"
        exit()
print "load query list over"

print "load tweet list ..."
tweet_list = []
for line in open('/index15/preprocess/filter_raw_19_29.txt'):
    t = line.strip().split('\t')
    tweet = AdvancedTweet(t[0], t[1], t[2], t[3])
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
            score1 = jm2_score(query, tweet, corpus_dict)
            score2 = jm5_score(query, tweet, corpus_dict)
            score3 = dir_score(query, tweet, corpus_dict)
            df.write("%s\t%s\t%.4f\t%.4f\t%.4f\n"%(query.id, tweet.id, score1, score2, score3))
df.close()



