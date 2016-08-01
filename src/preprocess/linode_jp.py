import sys
import gzip
sys.path.append('../')
from package.tweet import Tweet
from package.utils import load_stopword_set

stopword_set = load_stopword_set()

df = open("/index15/preprocess/linode_jp.txt", "w")

def single_file(file_path):
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            t = Tweet(line.strip(), stopword_set)
            if t.is_valid:
                df.write( "%s\t%s\t%s\t%s\n" % (t.created_at, t.id_str, " ".join(t.word_list), " ".join(t.stem_list)) )

def multi_files():
    for day in range(25, 29):
        for hour in range(24):
            print "%02d\t%02d" % (day, hour)
            try:
                file_path = "/home/ziaoang/linode_jp/statuses.log.2016-07-%02d-%02d.gz"%(day, hour)
                single_file(file_path)
                print "OK"
            except Exception, e:
                print e
    
multi_files()

df.close()



