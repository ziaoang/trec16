import sys
from gensim.models.word2vec import Word2Vec

sentences = []
line_no = 0
for line in open("/index15/preprocess/preprocess_1507.txt"):
    line_no += 1
    if line_no % 100000 == 0:
        print "%d lines" % line_no
    t = line.strip().split('\t')
    sentences.append(t[2].split(' '))

print "total sentences count: %d" % len(sentences)
model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
model.save_word2vec_format("/index15/w2v/w2v_1507.txt")



