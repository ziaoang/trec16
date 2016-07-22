import gzip
from gensim.models.word2vec import Word2Vec
from package.tweet import Tweet

def load_sentences(file_path):
    sentences = []
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            tweet = Tweet(line.strip(), set(), {})
            if tweet.created_at != None and tweet.lang == 'en':
                if tweet.word_list != None and len(tweet.word_list) > 0:
                    sentences.append(tweet.word_list)
    return sentences

def train_w2v():
    sentences = []
    for day in range(13, 30):
        for hour in range(24):
            try:
                file_path = "/index15/raw/statuses.log.2015-07-%02d-%02d.gz"%(day, hour)
                current_sentences = load_sentences(file_path)
                print("%02d\t%02d\t%d"%(day, hour, len(current_sentences)))
                sentences += current_sentences
            except Exception, e:
                print("%02d\t%02d"%(day, hour))
                print e
    
    print("total sentences count: %d"%len(sentences))
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save_word2vec_format("/index15/w2v/w2v.txt")

train_w2v()


