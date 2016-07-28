#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     train.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-28 13:27:24
# MODIFIED: 2016-07-28 13:27:25

import os
import logging
from package.utils import selected_queryid_set
from package.relation import similarity_t_t

selected_query_set = selected_queryid_set()
# logging.basicConfig(filename='train.log', level=logging.INFO)


def single_query(file_path, topid):
    jm_min = 9999999
    jm_max = 0
    dirichlet_min = 9999999
    dirichlet_max = 0
    fin = open(file_path, "r")
    content = fin.readlines()
    for line in content:
        timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
        if jm_min > float(jm): jm_min = float(jm)
        if jm_max < float(jm): jm_max = float(jm)
        if dirichlet_min > float(dirichlet): dirichlet_min = float(dirichlet)
        if dirichlet_max < float(dirichlet): dirichlet_max = float(dirichlet)
    # logging.info(file_path + "\t" + str(jm_min) + "\t" + str(jm_max) + "\t" + str(dirichlet_min) + "\t" + str(dirichlet_max))
    
    jm_begin = float("{0:.2f}".format(jm_min + (jm_max - jm_min) * 0))
    jm_step = float("{0:.2f}".format((jm_max - jm_begin) / 10))
    dirichlet_begin = float("{0:.2f}".format(dirichlet_min + (dirichlet_max - dirichlet_min) * 0))
    dirichlet_step = float("{0:.2f}".format((dirichlet_max - dirichlet_min) / 10))
    
    
    while jm_begin < jm_max:
        # print "jm_begin: ", jm_begin
        # print "dirichlet_begin: ", dirichlet_begin
        wf1 = "../data/data15/res/R" + topid + "_JR" + str(jm_begin)
        wf2 = "../data/data15/res/R" + topid + "_DR" + str(dirichlet_begin)
        r1 = open(wf1, "w")
        r2 = open(wf2, "w")
        for line in content:
            timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
            if float(jm) > jm_begin:
                string =  timestamp + "\t" + id      + "\t" + plain_text     + "\t" + \
                          stem_text + "\t" + str(jm) + "\t" + str(dirichlet) + "\n"
                r1.write(string)
            if float(dirichlet) > dirichlet_begin:
                string =  timestamp + "\t" + id      + "\t" + plain_text     + "\t" + \
                          stem_text + "\t" + str(jm) + "\t" + str(dirichlet) + "\n"
                r2.write(string)          
        jm_begin += jm_step
        dirichlet_begin += dirichlet_step
        
    

if __name__ == "__main__":
    base_path = "../data/data15/score2/"
    topid = "MB226"
    full_path = base_path + topid
    single_query(full_path, topid)
    # for topid in selected_query_set:
        # print topid
        # full_path = base_path + topid
        # if os.path.isfile(full_path):
            # single_query(full_path, topid)