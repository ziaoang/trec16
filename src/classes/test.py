from query import Query
from tweet import Tweet
import relation

q = Query("MB001", "A A B C", "", "")
t1 = Tweet("A A B B C D D D")
t2 = Tweet("A A B C C D")

print(relation.similarity_q_t(q, t1))

print(relation.similarity_t_t(t1, t2))

print(relation.similarity_t_t(t1, t1))


