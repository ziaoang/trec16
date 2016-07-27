import bz2
import os.path
from package.tweet import Tweet
from package.utils import load_stopword_set

stopword_set = load_stopword_set()

df = open("/index15/preprocess/1507_filtered.txt", "w")

def single_file(file_path):
    with bz2.BZ2File(file_path) as f:
        for line in f:
            t = Tweet(line.strip(), stopword_set)
            if t.is_valid:
                df.write( "%s\t%s\t%s\t%s\n" % (t.created_at, t.id_str, " ".join(t.word_list), " ".join(t.stem_list)) )

def multi_files():
    for day in range(1, 32):
        for hour in range(24):
            print "%02d\t%02d" % (day, hour)
            for minute in range(60):
                file_path = "/index15/1507/%02d/%02d/%02d.json.bz2"%(day, hour, minute)
                if os.path.isfile(file_path):
                    single_file(file_path)
    
multi_files()

df.close()



