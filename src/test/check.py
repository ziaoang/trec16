import numpy as np

score1_list = []
score2_list = []

for line in open("score.dat"):
    t = line.strip().split('\t')
    qid, tid = t[0], t[1]
    score1, score2 = float(t[2]), float(t[3])
    score1_list.append(score1)
    score2_list.append(score2)

print "%.4f" % np.mean(score1_list) 
print "%.4f" % np.mean(score2_list) 



