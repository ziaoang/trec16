class AdvancedQuery:
    def __init__(self, topid, title):
        self.topid        = topid
        self.title        = title
 
        self.plain_text   = self.extract_plain_text(self.title)
            
        self.word_list    = self.extract_word_list(self.plain_text)
        #self.word_distri  = self.extract_distribution(self.word_list)
            
        self.stem_list    = self.stem(self.filter_stopword(self.word_list))
        #self.stem_distri  = self.extract_distribution(self.stem_list)

        #self.vector       = self.extract_vector(self.word_list)



