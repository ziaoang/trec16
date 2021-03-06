from trecjson import TrecJson

class AdvancedTweet(TrecJson):
    def __init__(self, created_at, id_str, word_list_str, stem_list_str):
        TrecJson.__init__(self, set())

        self.created_at   = created_at
        self.id_str       = id_str

        self.id           = self.id_str
        
        self.word_list    = word_list_str.split(' ')
        self.word_distri  = self.extract_distribution(self.word_list)
        self.stem_list    = stem_list_str.split(' ')
        self.stem_distri  = self.extract_distribution(self.stem_list)



