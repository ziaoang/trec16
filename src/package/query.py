import json
from trecjson import TrecJson

class Query(TrecJson):
    def __init__(self, query_json, stopword_set, vector_dict):
        TrecJson.__init__(self, stopword_set, vector_dict)

        try:
            t = json.loads(query_json)
            self.topid        = t['topid']
            self.title        = t['title']
            self.description  = t['description']
            self.narrative    = t['narrative']
            
            self.plain_text   = self.extract_plain_text(self.title)
            self.word_list    = self.extract_word_list(self.plain_text)
            self.word_distri  = self.extract_distribution(self.word_list)
            self.stem_list    = self.stem(self.filter_stopword(self.word_list))
            self.stem_distri  = self.extract_distribution(self.stem_list)
            self.vector       = self.extract_vector(self.word_list)

            self.is_valid = True
        except:
            self.is_valid = False
 


