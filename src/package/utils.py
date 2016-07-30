import os

def load_stopword_set():
    print("load stopword ...")
    absolute_path = os.path.join(os.path.dirname(__file__) + "/../../data/stopword")
    stopword_set = set()
    for line in open(absolute_path):
        stopword_set.add(line.strip())
    print("load stopword over")
    return stopword_set

def load_vector_dict():
    print("load word2vec ...")
    absolute_path = "/index15/w2v/w2v_raw.txt"
    vector_dict = {}
    line_no = 0
    for line in open(absolute_path):
        line_no += 1
        if line_no == 1:
            continue
        t = line.strip().split()
        word = t[0]
        vector = []
        for i in range(1, len(t)):
            vector.append(float(t[i]))
        vector_dict[word] = vector
    print("load word2vec over")
    return vector_dict

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


