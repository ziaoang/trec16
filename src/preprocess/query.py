import sys
sys.path.append("../")
from package.query import Query
from package.utils import load_stopword_set, load_vector_dict, load_corpus_dict, load_query_list


# Global Variates
stopword_set = load_stopword_set()
print 'stopword_set size: %d' % len(stopword_set)

vector_dict = load_vector_dict()
print 'vector_dict size: %d'  % len(vector_dict)

corpus_dict = load_corpus_dict()
print 'corpus_dict size: %d'  % len(corpus_dict)

query_list = load_query_list(stopword_set, vector_dict)
print 'query_list size: %d'   % len(query_list)

for query in query_list:
    print "%s\t%s\t%s" % (query.id, ' '.join(query.word_list), ' '.join(query.stem_list))

