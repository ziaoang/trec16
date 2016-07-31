import os
import sys
import time
import json
import MySQLdb
import datetime

from package.advancedTweet import AdvancedTweet
from package.utils import load_stopword_set, load_corpus_dict, load_corpus_dict, load_query_list
from package.relation import similarity_q_t, similarity_t_t

# Global Variates
stopword_set = load_stopword_set()
print 'stopword_set size: %d' % len(stopword_set)

vector_dict  = {}
print 'vector_dict size: %d'  % len(vector_dict)

corpus_dict = corpus_dict()
print 'corpus_dict size: %d'  % len(corpus_dict)

query_list   = load_query_list(stopword_set, vector_dict)
print 'query_list size: %d'   % len(query_list)

all_stem_set = set()
for query in query_list:
    for stem in query.stem_distri:
        all_stem_set.add(stem)
print 'all_stem_set size: %d' % len(all_stem_set)

# Submit Functions
def load_submit(file_path):
    submit = {}
    for query in query_list:
        submit[query.id] = {}
        for day in range(2, 11 + 1):
            submit[query.id][day] = []
    for line in open(file_path):
        t = line.strip().split('\t')
        qid, day = t[0], int(t[1])
        tweet = AdvancedTweet(t[2], t[3], t[4], t[5], vector_dict)
        submit[qid][day].append(tweet)
    return submit

def save_submit(file_path, qid, day, tweet):
    df = open(file_path, 'a')
    created_at    = tweet.created_at
    id_str        = tweet.id_str
    word_list_str = ' '.join(tweet.word_list)
    stem_list_str = ' '.join(tweet.stem_list)
    df.write('%s\t%d\t%s\t%s\t%s\t%s\n' % (qid, day, created_at, id_str, word_list_str, stem_list_str))
    df.close()

def post_submit(qid, tid, client_id):
    os.system("Post: curl -X POST -H 'Content-Type: application/json'  54.164.151.19:80/tweet/%s/%s/%s" % (qid, tid, client_id))

#=================================================================# RUN A 1
run_a_1_client_id = 'kcm9Tu9dUIjP'
run_a_1_rel_thr = 0.67
run_a_1_red_thr = 0.67
run_a_1_submit_file_path = 'RUN/A1_SUBMIT.txt'
run_a_1_submit  = load_submit(run_a_1_submit_file_path)

def run_a_1(query, tweet):
    dt = datetime.datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")
    if len(run_a_1_submit[query.id][dt.day]) >= 10: return
    rel_score = similarity_q_t(query, tweet, corpus_dict)
    if rel_score > run_a_1_rel_thr:
        max_red_score = 0
        for day in range(2, dt.day + 1):
            for other_tweet in run_a_1_submit[query.id][day]:
                red_score = similarity_q_t(tweet, other_tweet, corpus_dict)
                max_red_score = max(max_red_score, red_score)
        if max_red_score < run_a_1_red_thr:
            run_a_1_submit[query.id][dt.day].append(tweet)
            save_submit(run_a_1_submit_file_path, query.id, dt.day, tweet)
            post_submit(query.id, tweet.id, run_a_1_client_id)
    
#=================================================================# RUN A 2
run_a_2_client_id = 'TyeaK74Lafp2'

def run_a_2(query, tweet):
    pass

#=================================================================# RUN A 3
run_a_3_client_id = '5YUZahsxivLv'

def run_a_3(query, tweet):
    pass

def is_overlap(query, tweet):
    for stem in tweet.stem_distri:
        if stem in query.stem_distri:
            return True
    return False

def tweet_handle(tweet):
    for query in query_list:
        if is_overlap(query, tweet):
            run_a_1(query, tweet)
            #run_a_2(query, tweet)
            #run_a_3(query, tweet)

def is_quick_filtered(tweet):
    for stem in tweet.stem_distri:
        if stem in all_stem_set:
            return False
    return True

def row_handle(created_at, id_str, word_list_str, stem_list_str):
    dt = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
    if dt.month == 8 and dt.day >= 2 and dt.day <= 11:
        print 'target tweet'
        tweet = AdvancedTweet(created_at, id_str, word_list_str, stem_list_str, vector_dict)
        if not is_quick_filtered(tweet):
            tweet_handle(tweet)
    else:
        print 'not target tweet'

def main():
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

def is_system_break():
    if os.path.exists('RUN/system_break.dat'):
        return True
    return False

if __name__ == "__main__":
    while True:
        if is_system_break():
            print 'system break'
            exit()
        
        print 'main'
        #main()
        
        print 'sleep 10 seconds'
        time.sleep(10)



