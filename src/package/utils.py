import os

def load_stopword_set():
    absolute_path = os.path.join(os.path.dirname(__file__) + "/../../data/stopword")
    stopword_set = set()
    for line in open(absolute_path):
        stopword_set.add(line.strip())
    return stopword_set

def load_vector_dict():
    return {}
