import json
from trecjson import TrecJson
from collections import defaultdict

class Query(TrecJson):
    def __init__(self, query_json, stopword_set, vector_dict):
        TrecJson.__init__(self, stopword_set, vector_dict)

        t = None
        try:
            t = json.loads(query_json)
        except:
            t = {}
        
        self.is_valid = True    

        default_t = defaultdict(lambda: None, t)
        self.topid        = default_t['topid']
        self.title        = default_t['title']
        self.description  = default_t['description']
        self.narrative    = default_t['narrative']
        
        if self.topid == None or self.title == None or self.description == None or self.narrative == None:
            self.is_valid = False
            return
 
        self.plain_text   = self.extract_plain_text(self.title)
            
        self.word_list    = self.extract_word_list(self.plain_text)
        self.word_distri  = self.extract_distribution(self.word_list)
            
        self.stem_list    = self.stem(self.filter_stopword(self.word_list))
        self.stem_distri  = self.extract_distribution(self.stem_list)

        self.vector       = self.extract_vector(self.word_list)



