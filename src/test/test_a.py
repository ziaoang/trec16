import sys
import json
import calendar
import datetime
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_corpus_dict
from package.relation import similarity_q_t, similarity_t_t

stopword_set = load_stopword_set()
vector_dict  = {}
corpus_dict  = load_corpus_dict()

print "load query list ..."
query_list = []
for line in open('../data/data15/origin.query'):
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

def time_format(create_at):
    delivery_time = datetime.datetime.strptime(create_at, "%a %b %d %H:%M:%S +0000 %Y")
    return calendar.timegm(delivery_time.timetuple())

def test(rel_thr, red_thr):
    #rel_thr = 0.75
    #red_thr = 0.67
    print "%.2f\t%.2f" % (rel_thr, red_thr)
    df = open("tmp/test_a_%.2f_%.2f.dat" % (rel_thr, red_thr), "w")
    submit_dict = {query.id:[] for query in query_list}
    for day in range(20, 30):
        for query in query_list:
            remain_count = 10
            for tweet in day_tweet[day]:
                if overlap(query.stem_distri, tweet.stem_list):
                    rel_score = similarity_q_t(query, tweet, corpus_dict)
                    if rel_score > rel_thr:
                        if remain_count > 0:
                            red_score = redundancy(tweet, submit_dict[query.id])
                            if red_score < red_thr:
                                remain_count -= 1
                                submit_dict[query.id].append(tweet)
                                df.write( "%s %s %s my\n" % (query.id, tweet.id, time_format(tweet.created_at) ) )
    df.close()


for rel_thr in [0.70, 0.72, 0.74, 0.76, 0.78, 0.80]:
    for red_thr in [0.60, 0.62, 0.64, 0.66, 0.68, 0.70]:
        test(rel_thr, red_thr)



