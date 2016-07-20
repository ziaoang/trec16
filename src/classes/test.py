import json

import relation
from trecjson import Query, Tweet


content = open('../../data/data15/topic.txt').read()

q_list = []
query_json_list = json.loads(content)
for query_json in query_json_list:
    query_json_string = json.dumps(query_json)
    q = Query(query_json_string)
    if q.topid != None:
        q_list.append(q)

for q in q_list:
    print(q.topid)

t_list = []
for line in open('../../data/data15/example.txt'):
    t = Tweet(line.strip())
    if t.created_at != None and t.lang == 'en':
        t_list.append(t)

for t in t_list:
    print(t.plain_text)


if len(q_list) > 0 and len(t_list) > 1:
    print(relation.similarity_q_t(q_list[0], t_list[0]))
    print(relation.similarity_t_t(t_list[0], t_list[1]))



