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

        default_t = defaultdict(lambda: None, t)
        self.topid        = default_t['topid']
        self.title        = default_t['title']
        self.description  = default_t['description']
        self.narrative    = default_t['narrative']
        
        if self.title != None:
            self.word_list    = self.extract_word_list(self.title)
            self.distribution = self.extract_distribution(self.word_list)
            self.vector       = self.extract_vector(self.word_list)
    
            self.nostop_list  = self.filter_stopword(self.word_list)
            self.stem_list    = self.stem(self.nostop_list)


