#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     submit.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-28 18:50:21
# MODIFIED: 2016-07-28 18:50:22

import time
import datetime
from os import listdir
from os.path import isfile, join

def single_file(file_path, file):
    topid = file.strip().split("_")[0]
    write_file = "../data/data15/submit/" + file
    result = open(write_file, "w") 
    with open(file_path, "r") as fin:
        for i, line in enumerate(fin):
            info = line.strip().split("\t")
            try:
                delivery_time = datetime.datetime.strptime(info[0], "%a %b %d %H:%M:%S +0000 %Y")
                localtime = int(time.mktime(delivery_time.timetuple()))
                string = topid + "\t" + info[1] + "\t" + str(localtime) + "\t" + "runA" + "\n"
                result.write(string)
            except Exception, e:
                print topid
                print i
                print str(e)

            

if __name__ == "__main__":
    base_path = "../data/data15/res/N/"
    file_names = [f for f in listdir(base_path) if isfile(join(base_path, f))]
    file_names.sort()
    for file in file_names:
        print file
        full_path = base_path + file
        single_file(full_path, file)
        
        