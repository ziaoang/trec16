#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     relevance.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-28 13:27:24
# MODIFIED: 2016-07-29 20:58:02

import os
import sys
from os import listdir
from os.path import isfile, join, isdir
from package.utils import selected_queryid_set
from package.relation import similarity_t_t

# Version 2.0
def single_file(score_file, day, topid, threshold_dir, nol, write_dir):
    # Get threshold dict, Key: topk, Value: current topid's threshold
    threshold = {} 
    topk_names = [k for k in listdir(threshold_dir) if isdir(join(threshold_dir, k))] 
    topk_names.sort()
    for topk in topk_names:
        file_path = threshold_dir + topk + "/" + str(int(day) - 1)
        with open(file_path) as fin:
            for line in fin:
                if not line.startswith(topid): continue
                threshold[topk] = line.strip().split("\t")[1]
                break

    for topk in topk_names:
        path = write_dir + nol + "/"
        if not isdir(path):
            cmd = "mkdir " + path
            os.system(cmd)
        path += topk + "/"
        if not isdir(path):
            cmd = "mkdir " + path
            os.system(cmd)
        path += day + "/"
        if not isdir(path):
            cmd = "mkdir " + path
            os.system(cmd)
        write_path = path + topid
        write_file = open(write_path, "w")
    
        with open(score_file, "r") as fin:
            for line in fin:
                timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
                if float(dirichlet) > float(threshold[topk]):
                    write_file.write(line)
            

            
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "sys.argv[1]: Input score.py result dir"
        print "sys.argv[2]: Input topK.py threshold dir!"
        print "sys.argv[3]: Output one stage candidate dir!"
        exit()
          
    day_names = [day for day in listdir(sys.argv[1]) if isdir(join(sys.argv[1], day))] 
    day_names.sort()
    for day in day_names:
        if int(day) <= 19: continue
        cur_path = sys.argv[1] + day + "/"
        topid_names = [f for f in listdir(cur_path) if isfile(join(cur_path, f))]
        topid_names.sort()
        for topid in topid_names:
            full_path = cur_path + topid
            print full_path
            nol_names = [nol for nol in listdir(sys.argv[2]) if isdir(join(sys.argv[2], nol))]
            nol_names.sort()
            for nol in nol_names:
                threshold_dir = sys.argv[2] + nol + "/"
                print threshold_dir
                single_file(full_path, day, topid, threshold_dir, nol, sys.argv[3])
            
            
# Version 1.0   
# selected_query_set = selected_queryid_set()
# logging.basicConfig(filename='train.log', level=logging.INFO)         
# def single_query(file_path, topid):
    # jm_min = 9999999
    # jm_max = 0
    # dirichlet_min = 9999999
    # dirichlet_max = 0
    # fin = open(file_path, "r")
    # content = fin.readlines()
    # for line in content:
        # timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
        # if jm_min > float(jm): jm_min = float(jm)
        # if jm_max < float(jm): jm_max = float(jm)
        # if dirichlet_min > float(dirichlet): dirichlet_min = float(dirichlet)
        # if dirichlet_max < float(dirichlet): dirichlet_max = float(dirichlet)
    # # logging.info(file_path + "\t" + str(jm_min) + "\t" + str(jm_max) + "\t" + str(dirichlet_min) + "\t" + str(dirichlet_max))
    
    # jm_begin = float("{0:.2f}".format(jm_min))
    # jm_step = float("{0:.2f}".format((jm_max - jm_begin) / 10))
    # dirichlet_begin = float("{0:.2f}".format(dirichlet_min))
    # dirichlet_step = float("{0:.2f}".format((dirichlet_max - dirichlet_min) / 10))
    
    # count = 0
    # while jm_begin < jm_max: 
        # jm_begin += jm_step
        # dirichlet_begin += dirichlet_step
        # count += 1
        # if count < 4: continue
        # # print "jm_begin: ", jm_begin
        # # print "dirichlet_begin: ", dirichlet_begin
        # wf1 = "../data/data15/res/R/" + topid + "_JR" + str(jm_begin)
        # wf2 = "../data/data15/res/R/" + topid + "_DR" + str(dirichlet_begin)
        # r1 = open(wf1, "w")
        # r2 = open(wf2, "w")
        # for line in content:
            # timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
            # if float(jm) > jm_begin:
                # string =  timestamp  + "\t" + id + "\t"         \
                          # plain_text + "\t" + stem_text + "\t" + \
                          # str(jm)    + "\t" + str(dirichlet) + "\n"
                # r1.write(string)
            # if float(dirichlet) > dirichlet_begin:
                # string =  timestamp  + "\t" + id + "\t"         \
                          # plain_text + "\t" + stem_text + "\t" + \
                          # str(jm)    + "\t" + str(dirichlet) + "\n"
                # r2.write(string)          

                
# if __name__ == "__main__":
    # base_path = "../data/data15/score2/"
    # for topid in selected_query_set:
        # print topid
        # full_path = base_path + topid
        # if os.path.isfile(full_path):
            # single_query(full_path, topid)
