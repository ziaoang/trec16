import os
import sys
import json
from query import Query

def load_stopword_set():
    print("load stopword ...")
    absolute_path = os.path.join(os.path.dirname(__file__) + "/../../data/stopword")
    stopword_set = set()
    for line in open(absolute_path):
        stopword_set.add(line.strip())
    print("load stopword over")
    return stopword_set

def load_corpus_dict():
    print("load corpus ...")
    corpus_dict = {}
    total_count = 0
    line_no = 0
    for line in open("/index15/tf/tf_raw.txt"):
        line_no += 1
        if line_no == 1:
            total_count = float(line.strip())
        else:
            t = line.strip().split('\t')
            corpus_dict[t[0]] = float(t[1]) / total_count
    print("load corpus over")
    return corpus_dict
    
def load_df_dict():
    corpus_dict = {}
    word_count = 0
    document_count = 0
    with open("/index15/tf/tfidf_1319.txt", "r") as fin:
        for i, line in enumerate(fin):
            if i == 0:
                word_count, document_count = line.strip().split("\t")
            else: 
                word, tf, df = line.strip().split("\t")
                corpus_dict[word] = float(df) / float(document_count)
    return corpus_dict, float(document_count)

def load_query_list():
    absolute_path = os.path.join(os.path.dirname(__file__) + "/../../data/data15/topic.txt")
    query_list = []
    try:
        content = open(absolute_path).read()
        query_json_list = json.loads(content)
        stopword_set = load_stopword_set()
        vector_dict = load_vector_dict()
        for query_json in query_json_list:
            query_json_string = json.dumps(query_json)
            query = Query(query_json_string, stopword_set, vector_dict)
            if not query.is_valid:  
                print "Error in get_topics(), invalid query!"
                exit()
            query_list.append(query)
    except Exception, e:
        print "Error in load_query_list(), " + str(e)
    return query_list
    
def load_webexpansion_query():
    query_list = []
    stopword_set = load_stopword_set()
    vector_dict = load_vector_dict()
    for line in open('../data/data15/web.top5.query'):
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
            print 'ERROR: query is not valid'
            exit()
    print 'load query over'
    return query_list

def selected_queryid_set():
    query_list = load_query_list()
    selected_query = [339,243,242,331,392,391,389,278,253,236,254,255,379,344,405,354,326,324,400,366,348,284,287,448,401,305,262,260,267,265,228,227,226,409,249,248,383,362,357,416,246,353,377,298,439,371,384,434,432,419,359]
    full_seleted = []
    for id in selected_query:
        full_seleted.append("MB" + str(id))
    selected_query_map = {}
    for query in query_list:
        if query.topid in set(full_seleted):
            selected_query_map[query.topid] = query.stem_list
    return selected_query_map


