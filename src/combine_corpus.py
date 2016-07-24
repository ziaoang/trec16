#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     combine_corpus.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-23 20:44:43
# MODIFIED: 2016-07-23 20:44:44

from corpus import conver


base_path = "../data/data15/1507"
dict = {}
write_file = "../data/data15/1507ALL.txt"
result = open(write_file, "w")

for day in range(1, 32):
    day = conver(day)
    print "Current day: ", day
    full_path = base_path + day + ".txt"
    with open(full_path, "r") as fin:
        for i, line in enumerate(fin):
            # Remain to figure out
            if i == 0: continue
            word, prob = line.strip().split("\t")
            if word not in dict:
                dict[word] = 0
            dict[word] += float(prob)
for key in dict:
    result.write(key + "\t" + str(dict[key] / 31) + "\n")
result.close()    
            
# Check the sum is equal to 1 or not.
# sum = 0
# with open("../data/data15/1507ALL.txt", "r") as fin:
    # for line in fin:
        # word, prob = line.strip().split("\t")
        # sum += float(prob)
        
# print sum