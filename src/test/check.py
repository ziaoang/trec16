import numpy as np

score1_list = []
score2_list = []
score3_list = []

for line in open("score.dat"):
    t = line.strip().split('\t')
    qid, tid = t[0], t[1]
    score1, score2, score3 = float(t[2]), float(t[3]), float(t[4])
    score1_list.append(score1)
    score2_list.append(score2)
    score3_list.append(score3)
    

print "%.4f" % np.mean(score1_list) 
print "%.4f" % np.mean(score2_list) 
print "%.4f" % np.mean(score3_list) 



