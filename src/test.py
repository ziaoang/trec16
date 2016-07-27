import sys
import json
from package.query import Query
from package.tweet import Tweet
from package.utils import load_stopword_set, load_vector_dict

stopword_set = load_stopword_set()
vector_dict  = load_vector_dict()


q_word_set = set()
q_list = []
for line in open('../data/data15/origin.query'):
    t = line.strip().split('\t')
    q_json                = {}
    q_json['topid']       = t[0]
    q_json['title']       = t[1]
    q_json['description'] = ""
    q_json['narrative']   = ""
    q_json_str = json.dumps(q_json)
    q = Query(q_json_str, stopword_set, vector_dict)
    if q.is_valid:
        q_list.append(q)
        for w in q.stem_list:
            q_word_set.add(w)
    else:
        print "ERROR: read query"
        exit()

for q in q_list:
    print '-' * 20
    print q.topid
    print q.title
    print " ".join(q.word_list)
    print " ".join(q.stem_list)

print len(q_word_set)


