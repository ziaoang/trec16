import json
from trecjson import TrecJson

class Tweet(TrecJson):
    def __init__(self, tweet_json, stopword_set):
        TrecJson.__init__(self, stopword_set, {})
        
        try:
            t = json.loads(tweet_json)
            self.created_at   = t['created_at']
            self.lang         = t['lang']
            self.id_str       = t['id_str']
            self.text         = t['text']
            
            if self.lang == 'en'            
                self.plain_text   = self.extract_plain_text(self.text)
                self.word_list    = self.extract_word_list(self.plain_text)
                self.stem_list    = self.stem(self.filter_stopword(self.word_list))
                
                if len(self.word_list) >= 5 and len(self.stem_list) >= 3:
                    self.is_valid = True
                else:
                    self.is_valid = False
            else:
                self.is_valid = False
        except:
            self.is_valid = False
        


