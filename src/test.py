import json
from package.query import Query
from package.tweet import Tweet
from package.relation import similarity_q_t, similarity_t_t
from package.utils import load_stopword_set, load_vector_dict

stopword_set = load_stopword_set()
vector_dict = load_vector_dict()

q_list = []
content = open('../data/data15/topic.txt').read()
query_json_list = json.loads(content)
for query_json in query_json_list:
    query_json_string = json.dumps(query_json)
    q = Query(query_json_string, stopword_set, vector_dict)
    if q.topid != None:
        q_list.append(q)

#for q in q_list:
#    print(q.topid)

t_list = []
for line in open('../data/data15/example.txt'):
    t = Tweet(line.strip(), stopword_set, vector_dict)
    if t.created_at != None and t.lang == 'en':
        t_list.append(t)

#for t in t_list:
#    print(t.id_str)


if len(q_list) > 0 and len(t_list) > 1:
    print(similarity_q_t(q_list[0], t_list[0]))
    print(similarity_t_t(t_list[0], t_list[1]))


