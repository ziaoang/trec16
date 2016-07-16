#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     query.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-16 17:01:52
# MODIFIED: 2016-07-16 17:01:53

class Query:
    def __init__(self, id, query_text):
        self.__id = id
        self.__text = query_text
        self.__word_dict = {}
        tokens = self.__text.strip().split(' ')
        self.__word_num = len(tokens)
        for word in tokens:
            if word not in self.__word_dict:
                self.__word_dict[word] = 1
            else:
                self.__word_dict[word] += 1
                
    def get_query_id(self):
        return self.__id
    
    def get_content(self):
        return self.__text
        
    def get_word_num(self):
        return self.__word_num
        
    def get_unique_word_num(self):
        return len(self.__word_dict)
        
    def get_current_word_num(self, word):
        if word in self.__word_dict:
            return self.__word_dict[word]
        else:
            return 0
    
    def get_current_word_tf(self, word):
        if word in self.__word_dict:
            return float(self.__word_dict[word]) / self.__word_num
        else:
            return 0.0
            
        
                