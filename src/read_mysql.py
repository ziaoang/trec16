#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     read_mysql.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-16 20:25:01
# MODIFIED: 2016-07-16 20:25:03

import MySQLdb
import time


if __name__ == "__main__":
        db = MySQLdb.connect(host="localhost",   
                             user="root",         
                             passwd="webkdd",  
                             db="trec16")        

        db.autocommit(True)
        try:
            cur = db.cursor()
            # sleep_time & flag are used to record continuous sleep time
            sleep_time = 0
            flag = False
            while True:
                cur.execute("SELECT * FROM raw WHERE is_process = 0")
                result = cur.fetchall()
                if len(result) == 0:
                    print 1
                    time.sleep(5)
                    if flag:
                        sleep_time += 5
                        # if continuous sleep time more than 2 hours, break
                        if sleep_time > 7200: break
                    else:
                        sleep_time = 5
                        flag = True
                    continue
                flag = False
                for row in result:
                    id = str(row[0])
                    json_data = row[1]
                    # deal with json_data, remain TO DO
                    print id
                    
                    # update database
                    cur.execute("UPDATE raw SET is_process = 1 WHERE id = %s", (id,))
        except MySQLdb.Error, e:
            print e
        db.close()
        