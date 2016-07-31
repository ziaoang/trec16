import time
import MySQLdb
import datetime

def row_handle(created_at, id_str, word_list_str, stem_list_str):
    dt = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
    if dt.month == 8 and dt.day >= 2 and dt.day <= 11:
        print 'target tweet'
    else:
        print 'not target tweet'

if __name__ == '__main__':
    while True:
        try:
            conn = MySQLdb.connect(host   = 'localhost',
                                   user   = 'root',
                                   passwd = 'webkdd',
                                   db     = 'trec16',
                                   port   = 3306)
            cur=conn.cursor()

            cur.execute('SELECT * FROM preprocess WHERE is_process = 0 limit 10')
            rows = cur.fetchall()
            for row in rows:
                id            = row[0]
                created_at    = row[1]
                id_str        = row[2] 
                word_list_str = row[3]
                stem_list_str = row[4]
                row_handle(created_at, id_str, word_list_str, stem_list_str)
                #cur.execute('UPDATE raw SET is_process = 1 WHERE id = %d' % id)
            conn.commit()
            
            cur.close()
            conn.close()
            
            print 'process %d rows' % len(rows)
        except Exception, e:
            print e            

        time.sleep(10)



