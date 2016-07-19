#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     read_topic.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-18 20:00:39
# MODIFIED: 2016-07-18 20:00:40

import json
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from src.classes.query import Query

# topic file is json format
def get_topics(input_file):
    while(True):
        try:
            with open(input_file, "r") as fin:
                data = json.load(fin)
                query_list = []
                for index in data:
                    for key in index:
                        index[key] = index[key].encode("utf-8")
                        key = key.encode("utf-8")
                    topid = index["topid"]
                    title = index["title"]
                    description = index["description"]
                    narrative = index["narrative"]
                    query_list.append(Query(topid, title, description, narrative))
                return query_list
        except ValueError, e:
            print str(e)
            time.sleep(5)
            continue