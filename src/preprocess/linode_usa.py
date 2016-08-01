import MySQLdb

try:
    conn = MySQLdb.connect(host   = 'localhost',
                           user   = 'root',
                           passwd = 'webkdd',
                           db     = 'trec16',
                           port   = 3306)
    cur=conn.cursor()

    cur.execute('SELECT * FROM preprocess')
    rows = cur.fetchall()
    
    df = open('linode_usa.txt', 'w')
    for row in rows:
        id            = row[0]
        created_at    = row[1]
        id_str        = row[2] 
        word_list_str = row[3]
        stem_list_str = row[4]
        df.write("%s\t%s\t%s\t%s\n" % (created_at, id_str, word_list_str, stem_list_str))
    df.close

    cur.close()
    conn.close()
    
    print 'process %d rows' % len(rows)
except Exception, e:
    print e



