import json
from trecjson import TrecJson
from collections import defaultdict

class Tweet(TrecJson):
    def __init__(self, tweet_json, stopword_set, vector_dict):
        TrecJson.__init__(self, stopword_set, vector_dict)
        
        t = None
        try:
            t = json.loads(tweet_json)
        except:
            t = {}
        
        self.is_valid = True    
        
        default_t = defaultdict(lambda: None, t)
        self.created_at   = default_t['created_at']
        self.lang         = default_t['lang']
        self.id_str       = default_t['id_str']
        self.text         = default_t['text']

        if self.created_at == None or self.lang == None or self.id_str == None or self.text == None:
            self.is_valid = False
            return
        
        if self.lang != 'en':
            self.is_valid = False
            return

        self.plain_text   = self.extract_plain_text(self.text)
            
        self.word_list    = self.extract_word_list(self.plain_text)
        self.word_distri  = self.extract_distribution(self.word_list)
    
        self.stem_list    = self.stem(self.filter_stopword(self.word_list))
        self.stem_distri  = self.extract_distribution(self.stem_list)

        self.vector       = self.extract_vector(self.word_list)

        if len(self.word_list) < 5 or len(self.stem_list) < 3:
            self.is_valid = False
            return



