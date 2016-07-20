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
        try:
            # connect db
            conn=MySQLdb.connect(host='localhost',user='root',passwd='webkdd',db='trec16',port=3306)
            cur=conn.cursor()

            # select rows
            cur.execute("SELECT * FROM raw WHERE is_process = 0")
            rows = cur.fetchall()
            for row in rows:
                id, json_data = str(row[0]), row[1]
                print id
                # deal with json_data
                pipeline(json_data)
                cur.execute("UPDATE raw SET is_process = 1 WHERE id = %s", (id,))
            conn.commit()

            # close db
            cur.close()
            conn.close()

            # print state
            print "OK"

        except Exception, e:
            print str(e)
            
        # iterator every 10 seconds
        time.sleep(10)

        
