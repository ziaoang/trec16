def load_stopword_set():
    stopword_set = set()
    for line in open("../data/stopword"):
        stopword_set.add(line.strip())
    return stopword_set

def load_vector_dict():
    return {}
