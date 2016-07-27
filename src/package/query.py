import json
from trecjson import TrecJson

class Query(TrecJson):
    def __init__(self, query_json, stopword_set):
        TrecJson.__init__(self, stopword_set, {})

        try:
            t = json.loads(query_json)
            self.topid        = t['topid']
            self.title        = t['title']
            self.description  = t['description']
            self.narrative    = t['narrative']
            
            self.plain_text   = self.extract_plain_text(self.title)
            self.word_list    = self.extract_word_list(self.plain_text)
            self.stem_list    = self.stem(self.filter_stopword(self.word_list))

            self.is_valid = True
        except:
            self.is_valid = False
 


