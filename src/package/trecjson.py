import re
import nltk

class TrecJson:
    def __init__(self, stopword_set, vector_dict):
        self.stopword_set = stopword_set
        self.vector_dict = vector_dict

    # term level
    def is_rt(self, term):
        return term == 'RT'

    def is_url(self, term):
        return r'http://' in term or r'https://' in term

    def is_at_user(self, term):
        return len(term) > 1 and term[0] == '@'

    def is_hashtag(self, term):
        return len(term) > 1 and term[0] == '#'

    # text level
    def filter_non_ascii(self, text):
        return re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    def merge_space(self, text):
        return re.sub(r'\s+', ' ', text).strip()
    
    def filter_twitter_label(self, text):
        if text == '': return text
        out = []
        for term in text.split(' ') :
            if self.is_rt(term) or self.is_url(term) or self.is_at_user(term):
                continue
            if self.is_hashtag(term):
                out.append(term[1:])
            else:
                out.append(term)
        return ' '.join(out)

    def extract_plain_text(self, text):
        text_1 = self.filter_non_ascii(text)
        text_2 = self.merge_space(text_1)
        text_3 = self.filter_twitter_label(text_2)
        return text_3
    
    def extract_word_list(self, text):
        return re.sub(r'[^a-zA-Z]+', ' ', text).strip().lower().split(' ')

    # word list level
    def filter_stopword(self, word_list):
        res = []
        for w in word_list:
            if w not in self.stopword_set:
                res.append(w)
        return res
    
    def stem(self, word_list):
        porter = nltk.PorterStemmer()
        return [porter.stem(w) for w in word_list]

    def extract_distribution(self, word_list):
        res = {}
        for w in word_list:
            if w not in res:
                res[w] = 0 
            res[w] += 1
        length = float(len(word_list))
        for w in res:
            res[w] /= length
        return res

    def extract_vector(self, word_list):
        res = []
        count = 0
        for w in word_list:
            if w in self.vector_dict:
                vector = self.vector_dict[w]
                if len(res) == 0:
                    for i in range(len(vector)):
                        res.append(vector[i])
                else:
                    for i in range(len(vector)):
                        res[i] += vector[i]
                count += 1
        for i in range(len(res)):
            res[i] = res[i] / count
        return res


