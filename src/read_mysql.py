#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     read_mysql.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-16 20:25:01
# MODIFIED: 2016-07-16 20:25:03

import MySQLdb
import time
from src.scenarioA import pipeline


if __name__ == "__main__":
    while True:
        # iterator every 10 seconds
        time.sleep(10)
        
        try:
            # connect db
            conn=MySQLdb.connect(host='localhost',user='root',passwd='webkdd',db='trec16',port=3306)
            cur=conn.cursor()

            # select rows
            cur.execute("SELECT * FROM raw WHERE is_process = 0")
            rows = cur.fetchall()
            ids = []
            for row in rows:
                id = str(row[0])
                json_data = row[1]
                # deal with json_data, remain TO DO
                pipeline(json_data)
                print id
                ids.append(id)
            
            print ids
            # update rows
            if len(ids) > 0:
                cur.executemany("UPDATE raw SET is_process = 1 WHERE id = %s", ids)
                conn.commit()

            # close db
            cur.close()
            conn.close()

            # print state
            print "OK"

        except Exception, e:
            # print state
            print e


        