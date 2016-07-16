#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     tweet.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-16 17:01:45
# MODIFIED: 2016-07-16 17:01:47

class Tweet:
    def __init__(self, id, timestamp, tweet_text):
        self.__id = id                          # tweet id
        self.__timestamp = timestamp            # tweet timestamp
        self.__tweet_text = tweet_text          # tweet content
        self.__word_dict = {}                   # tweet word dictionary
        tokens = tweet_text.strip().split(" ")
        self.__word_num = len(tokens)           # word number 
        for word in tokens:
            if word not in self.__word_dict:
                self.__word_dict[word] = 1
            else:
                self.__word_dict[word] += 1
    
    def get_tweet_id(self):
        return self.__id
        
    def get_timestamp(self):
        return self.__timestamp
        
    def get_content(self):
        return self.__tweet_text

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
    
