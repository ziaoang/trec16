import sys
import json
import calendar
import datetime
sys.path.append("../")
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_corpus_dict
from package.relation import similarity_q_t, similarity_t_t

stopword_set = load_stopword_set()
vector_dict  = {}
corpus_dict  = load_corpus_dict()

print "load query list ..."
query_list = []
for line in open('../../data/data15/origin.query'):
    t = line.strip().split('\t')
    query_json = {"topid":t[0], "title":t[1], "description":"", "narrative":""}
    query_json_str = json.dumps(query_json)
    query = Query(query_json_str, stopword_set, vector_dict)
    if query.is_valid:
        query_list.append(query)
    else:
        print "ERROR: read query"
        exit()
print "load query list over"

def get_day(created_at):
    t = created_at.strip().split(' ')
    return int(t[2])

print "load tweet list ..."
day_tweet = {}
for line in open('/index15/preprocess/filter_raw.txt'):
    t = line.strip().split('\t')
    tweet = AdvancedTweet(t[0], t[1], t[2], t[3], vector_dict)
    day = get_day(tweet.created_at)
    if day < 20: continue
    if day not in day_tweet:
        day_tweet[day] = []
    day_tweet[day].append(tweet)
print "load tweet list over"

def overlap(query_stem_distri, tweet_stem_list):
    for w in tweet_stem_list:
        if w in query_stem_distri:
            return True
    return False

def redundancy(tweet, tweet_list):
    if len(tweet_list) <= 0: return 0.0
    max_v = 0.0
    for t in tweet_list:
        score = similarity_t_t(tweet, t, corpus_dict)
        max_v = max(max_v, score)
    return max_v

def test(red_thr):
    print "%.2f" % red_thr
    df = open("tmp/test_b_%.2f.dat" % red_thr, "w")
    submit_dict = {query.id:[] for query in query_list}
    for query in query_list:
        for day in range(20, 30):
            remain_count = 10
            tweet_score_list = []
            for tweet in day_tweet[day]:
                if overlap(query.stem_distri, tweet.stem_list):
                    rel_score = similarity_q_t(query, tweet, corpus_dict)
                    tweet_score_list.append([tweet, rel_score])
            tweet_score_list.sort(key=lambda x: x[1], reverse=True)
            for t in tweet_score_list:
                if remain_count > 0:
                    tweet, rel_score = t[0], t[1]
                    red_score = redundancy(tweet, submit_dict[query.id])
                    if red_score < red_thr:
                        remain_count -= 1
                        submit_dict[query.id].append(tweet)
                        df.write( "201507%d %s Q0 %s %d %.4f my\n" % (day, query.id, tweet.id, 10-remain_count, rel_score) )
    df.close()

for red_thr in [0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80]:
    test(red_thr)



