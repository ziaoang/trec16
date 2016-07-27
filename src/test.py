import sys
import json
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_vector_dict, load_corpus_dict
from package.relation import similarity_q_t

stopword_set = load_stopword_set()
vector_dict  = load_vector_dict()
corpus_dict  = load_corpus_dict()

query_list = []
for line in open('../data/data15/origin.query'):
    t = line.strip().split('\t')
    query_json                = {}
    query_json['topid']       = t[0]
    query_json['title']       = t[1]
    query_json['description'] = ""
    query_json['narrative']   = ""
    query_json_str = json.dumps(query_json)
    query = Query(query_json_str, stopword_set, vector_dict)
    if query.is_valid:
        query_list.append(query)
    else:
        print "ERROR: read query"
        exit()

def overlap(query_stem_dict, tweet_stem_list):
    for w in tweet_stem_list:
        if w in query_stem_dict:
            return True
    return False

df = open("../data/score.txt", "w")
line_no = 0
for line in open('/index15/preprocess/filter_raw.txt'):
    line_no += 1
    if line_no % 100000 == 0:
        print line_no
    t = line.strip().split('\t')
    tweet = AdvancedTweet(t[0], t[1], t[2], t[3], vector_dict)
    for query in query_list:
        if overlap(query.stem_distri, tweet.stem_list):
            score = similarity_q_t(query, tweet, corpus_dict)
            df.write("%s\t%s\t%.4f\n" % (query.topid, tweet.id_str, score))
df.close()



