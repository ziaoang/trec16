import math


def jaccard(word_list_1, word_list_2):
    t1 = set(word_list_1)
    t2 = set(word_list_2)
    return len(t1 & t2) / float(len(t1 | t2))

def kl(distribution_1, distribution_2):
    res = 0.0
    overlap = set(distribution_1.keys()) & set(distribution_2.keys())
    for key in overlap:
        res += distribution_1[key] * math.log(distribution_1[key] / distribution_2[key])
    return res

def sym_kl(distribution_1, distribution_2):
    return (kl(distribution_1, distribution_2) + kl(distribution_2, distribution_1)) / 2

def cos(vector_1, vector_2):
    a, b, c = 0.0, 0.0, 0.0
    for i in range(len(vector_1)):
        a += vector_1[i] * vector_2[i]
        b += vector_1[i] * vector_1[i]
        c += vector_2[i] * vector_2[i]
    if b == 0.0 or c == 0.0:
        return 0.0
    return a / math.sqrt(b * c)

def dis(vector_1, vector_2):
    res = 0.0
    for i in range(len(vector_1)):
        res += (vector_1[i] - vector_2[i]) ** 2
    return math.sqrt(res)

def similarity_q_t(query, tweet):
    return 0.25 * jaccard(query.word_list, tweet.word_list) + \
           0.25 * kl(query.distribution, tweet.distribution) + \
           0.25 * cos(query.vector, tweet.vector) + \
           0.25 * dis(query.vector, tweet.vector)

def similarity_t_t(tweet_1, tweet_2):
    return 0.25 * jaccard(tweet_1.word_list, tweet_2.word_list) + \
           0.25 * kl(tweet_1.distribution, tweet_2.distribution) + \
           0.25 * cos(tweet_1.vector, tweet_2.vector) + \
           0.25 * dis(tweet_1.vector, tweet_2.vector)



