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

def single_file(file_path, dir, file, k, write_dir):
    if not isdir(write_dir + "TOP" + k):
        cmd = "mkdir " + write_dir + "TOP" + k
        os.system(cmd)
    write_path = write_dir + "TOP" + k + "/" + dir
    write_file = open(write_path, "a")
    
    with open(file_path, "r") as fin:
        for i, line in enumerate(fin):
            if i == int(k) - 1:
                timestamp, id, plain_text, stem_text, jm, dirichlet = line.strip().split("\t")
                write_file.write(file + "\t" + dirichlet + "\n")
                break
            
    write_file.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "sys.argv[1]: Input rankB output dir!"
        print "sys.argv[2]: Input K!"
        print "sys.argv[3]: Output threshold dir!"
        exit()
          
    dir_names = [dir for dir in listdir(sys.argv[1]) if isdir(join(sys.argv[1], dir))]  
    dir_names.sort()
    # dir means day, file means topid
    for dir in dir_names:
        cur_path = sys.argv[1] + dir + "/"
        file_names = [f for f in listdir(cur_path) if isfile(join(cur_path, f))]
        file_names.sort()
        for file in file_names:
            full_path = cur_path + file
            print full_path
            single_file(full_path, dir, file, sys.argv[2], sys.argv[3])