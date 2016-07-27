#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     corpus.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-22 19:37:10
# MODIFIED: 2016-07-23 11:18:11

import json
import os.path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import bz2
from bz2 import decompress
from package.tweet import Tweet
from package.utils import load_stopword_set, load_vector_dict

stopword_set = load_stopword_set()
vector_dict = load_vector_dict()


def conver(num):
    string = ""
    if num < 10:
        string += "0"
    string += str(num)
    return string

if __name__ == "__main__":
    try:
        base_path = "/index15/1507/"
        for day in range(1, 32):
            day = conver(day)
            count = 0
            dict = {}
            write_file = "../data/data15/1507" + day + ".txt"
            result = open(write_file, "w")
            
            print "Current day is: ", day
            for hour in range(0, 24):
                hour = conver(hour)
                print "Current hour is: ", hour
                for minute in range(0, 60):
                    minute = conver(minute)
                    print "Current minute is: ", minute
                    full_path = base_path + day + "/" + hour + "/" + minute + ".json.bz2"
                    if not os.path.isfile(full_path): continue
                    content = open(full_path).read()
                    content = bz2.decompress(content)
                    json_list = content.strip().split("\n")
                    for tweet_json in json_list:
                        tweet = Tweet(tweet_json, stopword_set, vector_dict)
                        if tweet.is_valid:
                            for key in tweet.stem_distri:
                                if key == "":
                                    print "Empty!"
                                    print tweet.stem_distri
                                    print tweet.nostop_list
                                    print tweet.text
                                    print "-" * 20
                                    print tweet.plain_text
                                    print tweet.id_str
                                    print full_path
                                    exit()
                                if key not in dict:
                                    dict[key] = 0
                                dict[key] += tweet.stem_distri[key]
                            count += 1
                    print len(dict)
            for key in dict:
                dict[key] = dict[key] / count
                result.write(key + "\t" + str(dict[key]) + "\n")
            result.close()
    except Exception as e:
        print str(e)
        exit()


    

    
