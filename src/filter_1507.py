import sys
import json
from package.query import Query
from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_vector_dict

stopword_set = load_stopword_set()
vector_dict  = load_vector_dict()

query_word_set = set()
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
        for w in query.stem_list:
            query_word_set.add(w)
    else:
        print "ERROR: read query"
        exit()

def match(tweet):
    for w in tweet.split(' '):
        if w in query_word_set:
            return True
    return False

df = open("/index15/preprocess/filter_1507.txt", "w")
for line in open("/index15/preprocess/preprocess_1507.txt"):
    t = line.strip().split('\t')
    if match(t[3]):
        df.write(line)
df.close()



