import sys
import json
from package.query import Query
from package.tweet import Tweet
from package.utils import load_stopword_set, load_vector_dict

stopword_set = load_stopword_set()
vector_dict  = load_vector_dict()

#stopword_set = set()
#vector_dict  = {}

q_list = []
content = open('../data/data15/topic.txt').read()
query_json_list = json.loads(content)
for query_json in query_json_list:
    query_json_str = json.dumps(query_json)
    q = Query(query_json_str, stopword_set, vector_dict)
    if q.is_valid:
        q_list.append(q)
        print q.topid
        print q.vector
    else:
        print "ERROR: read query"
        exit()

for q in q_list:
    print '-' * 20
    print q.topid
    print q.title
    print q.plain_text

t_list = []
for line in open('../data/data15/example.txt'):
    t = Tweet(line.strip(), stopword_set, vector_dict)
    if t.is_valid:
        t_list.append(t)
    else:
        print "ERROR: read tweet"

for t in t_list:
    print '-' * 20
    print t.id_str
    print t.text
    print t.plain_text



