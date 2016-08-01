import os
import sys
import json

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
    for line in open("/index15/tf/tf_merge_kdd118_linode_usa.txt"):
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



