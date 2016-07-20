import re
import json
from collections import defaultdict

class TrecJson:
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

    def extract_distribution(self, word_list):
        res = {}
        for w in word_list:
            if w not in res:
                res[w] = 0 
            res[w] += 1
        length = float(len(word_list))
        for w in res:
            res[w] /= length
        return res

    def extract_vector(self, word_list):
        res = [0.0] * 100
        return res


class Query(TrecJson):
    def __init__(self, query_json):
        try:
            t = json.loads(query_json)
            default_t = defaultdict(lambda: None, t)
            self.topid        = default_t['topid']
            self.title        = default_t['title']
            self.description  = default_t['description']
            self.narrative    = default_t['narrative']
            
            self.word_list    = self.extract_word_list(self.title) if self.title != None else None
            self.distribution = self.extract_distribution(self.word_list) if self.word_list != None else None
            self.vector       = self.extract_vector(self.word_list) if self.word_list != None else None
        except:
            self.topid        = None
            self.title        = None
            self.description  = None
            self.narrative    = None

            self.word_list    = None
            self.distribution = None
            self.vector       = None


class Tweet(TrecJson):
    def __init__(self, tweet_json):
        try:
            t = json.loads(tweet_json)
            default_t = defaultdict(lambda: None, t)
            self.created_at   = default_t['created_at']
            self.lang         = default_t['lang']
            self.id_str       = default_t['id_str']
            self.text         = default_t['text']

            self.plain_text   = self.extract_plain_text(self.text) if self.text != None else None
            self.word_list    = self.extract_word_list(self.plain_text) if self.plain_text != None else None
            self.distribution = self.extract_distribution(self.word_list) if self.word_list != None else None
            self.vector       = self.extract_vector(self.word_list) if self.word_list != None else None
        except:
            self.created_at   = None
            self.lang         = None
            self.id_str       = None
            self.text         = None

            self.plain_text   = None
            self.word_list    = None
            self.distribution = None
            self.vector       = None



