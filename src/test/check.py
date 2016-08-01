from collections import defaultdict
import numpy as np

a = defaultdict(set)
for line in open("../../data/data15/qrels.txt"):
    t = line.strip().split(' ')
    qid = "MB" + t[0]
    tid = t[2]
    if t[3] == '1' or t[3] == '2':
        a[qid].add(tid)

total_count = 0
for qid in a:
    total_count += len(a[qid])
print total_count

score1_list = []
score2_list = []
score3_list = []
for line in open("score.dat"):
    t = line.strip().split('\t')
    qid, tid = t[0], t[1]
    score1, score2, score3 = float(t[2]), float(t[3]), float(t[4])
    #if tid in a[qid]:
    score1_list.append(score1)
    score2_list.append(score2)
    score3_list.append(score3)

print len(score1_list)
       
print np.mean(score1_list) 
print np.mean(score2_list) 
print np.mean(score3_list) 



