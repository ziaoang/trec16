#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     topK.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-29 20:59:13
# MODIFIED: 2016-07-29 20:59:15

import sys
import os
import datetime
from os import listdir
from os.path import isfile, join, isdir

def single_file(file_path, nol, day, topid, k, write_dir):
    path = write_dir + nol + "/"
    if not isdir(path):
        cmd = "mkdir " + path
        os.system(cmd)
    path = path + "TOP" + k + "/"
    if not isdir(path):
        cmd = "mkdir " + path
        os.system(cmd)
    write_path = path + day
    # print write_path
    # exit()
    write_file = open(write_path, "a")
    
    fin = open(file_path, "r")
    content = fin.readlines()
    length = len(content)
    if length < int(k):
        line = content[length - 1]
    else: line = content[int(k) - 1]
    timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
    write_file.write(topid + "\t" + dirichlet + "\n") 
    write_file.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "sys.argv[1]: Input rankB output dir!"
        print "sys.argv[2]: Input K!"
        print "sys.argv[3]: Output threshold dir!"
        exit()
          
    nol_names = [dir for dir in listdir(sys.argv[1]) if isdir(join(sys.argv[1], dir))]  
    nol_names.sort()
    for nol in nol_names:
        cur_path = sys.argv[1] + nol + "/"
        day_names = [day for day in listdir(cur_path) if isdir(join(cur_path, day))]
        day_names.sort()
        # print day_names
        for day in day_names:
            second_path = cur_path + day + "/"
            # print second_path
            topid_names = [f for f in listdir(second_path) if isfile(join(second_path, f))]
            topid_names.sort()
            for topid in topid_names:
                print topid
                full_path = second_path + topid
                print full_path
                single_file(full_path, nol, day, topid, sys.argv[2], sys.argv[3])