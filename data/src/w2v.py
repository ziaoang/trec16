import re
import json
import gzip
from collections import defaultdict
from gensim.models.word2vec import Word2Vec

class Status():
    def __init__(self, status_json):
        t = json.loads(status_json)
        default_t = defaultdict(lambda: None, t)
        self.created_at = default_t['created_at']
        self.lang       = default_t['lang']
        self.id_str     = default_t['id_str']
        self.text       = default_t['text']

        self.plain_text = self.extract_plain_text(self.text) if self.text != None else None
        self.word_list = self.extract_word_list(self.plain_text) if self.plain_text != None else None

    def filter_non_ascii(self, text):
        return re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    def merge_space(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def is_rt(self, term):
        return term == 'RT'

    def is_url(self, term):
        return r'http://' in term or r'https://' in term

    def is_at_user(self, term):
        return len(term) > 1 and term[0] == '@'

    def is_hashtag(self, term):
        return len(term) > 1 and term[0] == '#'
    
    def filter_twitter_label(self, text):
        if text == '': return text
        out = []
        for term in text.split(' ') :
            if self.is_rt(term) or self.is_url(term) or self.is_at_user(term):
                continue
            if self.is_hashtag(term):
                out.append(term[1:])
            else:
                out.append(term)
        return ' '.join(out)

    def extract_plain_text(self, text):
        text_1 = self.filter_non_ascii(text)
        text_2 = self.merge_space(text_1)
        text_3 = self.filter_twitter_label(text_2)
        return text_3
    
    def extract_word_list(self, text):
        return re.sub(r'[^a-zA-Z]+', ' ', text).lower().strip().split(' ')

def load_sentences(file_path):
    sentences = []
    with gzip.open(file_path, 'rt') as f:
        for line in f:
            status = Status(line.strip())
            if status.created_at != None and status.lang == 'en':
                sentences.append(status.word_list)
    return sentences

def train_w2v():
    sentences = []
    for day in range(13, 30):
        for hour in range(24):
            print("%d\t%d"%(day, hour))
            file_path = "/index15/raw/statuses.log.2015-07-%02d-%02d.gz"%(day, hour)
            current_sentences = load_sentences(file_path)
            sentences += current_sentences
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save_word2vec_format("w2v.txt")

train_w2v()



