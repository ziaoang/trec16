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
            while True:
                cur.execute("SELECT * FROM raw WHERE is_process = 1")
                if len(cur.fetchall()) == 0:
                    time.sleep(5)
                    continue
                for row in cur.fetchall():
                    id = str(row[0])
                    json_data = row[1]
                    # deal with json_data, remain TO DO
                    
                    
                    # update database
                    cur.execute("UPDATE raw SET is_process = 0 WHERE id = %s", (id,))
                # exit()
        except MySQLdb.Error, e:
            print e
        db.close()
        