#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     submit.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-28 18:50:21
# MODIFIED: 2016-07-28 18:50:22

import sys
import time
import datetime
import calendar
import os
from os import listdir
from os.path import isfile, isdir, join
from package.utils import selected_queryid_set


def single_file(file_path, topkn, write_dir):
    write_file = write_dir + topkn
    result = open(write_file, "a") 
    with open(file_path, "r") as fin:
        for i, line in enumerate(fin):
            info = line.strip().split("\t")
            try:
                delivery_time = datetime.datetime.strptime(info[0], "%a %b %d %H:%M:%S +0000 %Y")
                localtime = calendar.timegm(delivery_time.timetuple())
                string = topid + "\t" + info[1] + "\t" + str(localtime) + "\t" + "runA" + "\n"
                result.write(string)
            except Exception, e:
                print topid
                print i
                print str(e)

            

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input two stage candidate dir"
        print "sys.argv[2]: Output submit dir!"
        exit()
    
    topid_set = selected_queryid_set() 
    topid_list = sorted(topid_set)

    topkn_names = [topKN for topKN in listdir(sys.argv[1]) if isdir(join(sys.argv[1], topKN))]
    topkn_names.sort()
    for topkn in topkn_names:
        # nol = float(topkn.strip.split("N")[1])
        cur_path = sys.argv[1] + topkn + "/"
        for topid in topid_list:
            day_names = [day for day in listdir(cur_path) if isdir(join(cur_path, day))]
            day_names.sort()
            for day in day_names:
                full_path = cur_path + day + "/" + topid
                print full_path
                single_file(full_path, topkn, sys.argv[2])
        
        