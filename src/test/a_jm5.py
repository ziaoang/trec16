import sys
import json
import calendar
import datetime
sys.path.append("../")
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_corpus_dict
from package.relation import sym_jm5_score

stopword_set = load_stopword_set()
corpus_dict  = load_corpus_dict()

score_dict = {}
for line in open("score.dat"):
    t = line.strip().split('\t')
    qid, tid = t[0], t[1]
    score1, score2 = float(t[2]), float(t[3])
    if qid not in score_dict:
        score_dict[qid] = {}
    score_dict[qid][tid] = score1

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

def get_day(created_at):
    t = created_at.strip().split(' ')
    return int(t[2])

print "load tweet list ..."
day_tweet = {}
for line in open('/index15/preprocess/filter_raw_19_29.txt'):
    t = line.strip().split('\t')
    tweet = AdvancedTweet(t[0], t[1], t[2], t[3])
    day = get_day(tweet.created_at)
    if day not in day_tweet:
        day_tweet[day] = []
    day_tweet[day].append(tweet)
print "load tweet list over"

def overlap(query, tweet):
    for w in query.stem_distri:
        if w in tweet.stem_distri:
            return True
    return False

def time_format(create_at):
    delivery_time = datetime.datetime.strptime(create_at, "%a %b %d %H:%M:%S +0000 %Y")
    return calendar.timegm(delivery_time.timetuple())

def main(rel_thr, red_thr):
    print "%.2f\t%.2f" % (rel_thr, red_thr)
    df = open("tmp/jm5_%.2f_%.2f.dat" % (rel_thr, red_thr), "w")
    submit_dict = {query.id:[] for query in query_list}
    for day in range(20, 30):
        for query in query_list:
            remain_count = 10
            for tweet in day_tweet[day]:
                if overlap(query, tweet):
                    rel_score = score_dict[query.id][tweet.id]
                    if rel_score > rel_thr:
                        if remain_count > 0:
                            red_score = 0
                            for submited_tweet in submit_dict[query.id]:
                                score = sym_jm5_score(tweet, submited_tweet, corpus_dict)
                                red_score = max(red_score, score)
                            if red_score < red_thr:
                                remain_count -= 1
                                submit_dict[query.id].append(tweet)
                                df.write( "%s %s %s my\n" % (query.id, tweet.id, time_format(tweet.created_at) ) )
    df.close()


for rel_thr in [0.75, 0.76, 0.77, 0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85]:
    for red_thr in [0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80]:
        main(rel_thr, red_thr)
    


