import os

def load_stopword_set():
    absolute_path = os.path.join(os.path.dirname(__file__) + "/../../data/stopword")
    stopword_set = set()
    for line in open(absolute_path):
        stopword_set.add(line.strip())
    return stopword_set

def load_vector_dict():
    print("load word2vec ...")
    absolute_path = "/index15/w2v/w2v.txt"
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
    absolute_path = os.path.join(os.path.dirname(__file__) + "/../../data/data15/1507ALL.txt")
    corpus_dict = {}
    with open(absolute_path, "r") as fin:
        for line in fin:
            word, prob = line.strip().split("\t")
            if word not in corpus_dict:
                corpus_dict[word] = 0
            corpus_dict[word] += float(prob)
    return corpus_dict
