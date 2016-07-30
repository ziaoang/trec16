import math

def jaccard(word_list_1, word_list_2):
    t1 = set(word_list_1)
    t2 = set(word_list_2)
    return len(t1 & t2) / float(len(t1 | t2))

def kl_jm(distribution_q, distribution_t, distribution_c, lamda):
    res = 0.0
    flag = False
    for key in distribution_q:
        smooth = 0
        if key in distribution_t: 
            smooth += (1 - lamda) * distribution_t[key]
        if key in distribution_c:
            smooth += lamda * distribution_c[key]
        if smooth != 0: 
            res += distribution_q[key] * math.log(smooth)
            flag = True
    if flag: return res
    return -999999.0

def kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t_len):
    res = 0.0
    flag = False
    for key in distribution_q:
        smooth = 0
        alpha = float(mu) / (t_len + mu);
        if key in distribution_t: 
            smooth += (1 - alpha) * distribution_t[key]
        if key in distribution_c: 
            smooth += alpha * distribution_c[key]
        if smooth != 0: 
            res += distribution_q[key] * math.log(smooth)
            flag = True
    if flag: return res
    return -999999.0

def kl_normalize(score):
    max_v = 0.0
    min_v = -20.0
    score = min(score, max_v)
    score = max(score, min_v)
    return (score - min_v) / (max_v - min_v)

def kl_jm_normalize(distribution_q, distribution_t, distribution_c, lamda):
    return kl_normalize(kl_jm(distribution_q, distribution_t, distribution_c, lamda))

def kl_dirichlet_normalize(distribution_q, distribution_t, distribution_c, mu, t_len):
    return kl_normalize(kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t_len))

def cos_normalize(vector_1, vector_2):
    a, b, c = 0.0, 0.0, 0.0
    for i in range(100):
        a += vector_1[i] * vector_2[i]
        b += vector_1[i] * vector_1[i]
        c += vector_2[i] * vector_2[i]
    if b == 0.0 or c == 0.0:
        return 0.0
    cos_score = a / math.sqrt(b * c)
    return ( cos_score + 1.0 ) / 2

def similarity_q_t(query, tweet, corpus_dict):
    s = kl_dirichlet(query.stem_distri, tweet.stem_distri, corpus_dict, 100, len(tweet.stem_list))
    return kl_normalize(s)

def similarity_t_t(tweet_1, tweet_2, corpus_dict):
    s1 = kl_dirichlet(tweet_1.stem_distri, tweet_2.stem_distri, corpus_dict, 100, len(tweet_2.stem_list))
    s2 = kl_dirichlet(tweet_2.stem_distri, tweet_1.stem_distri, corpus_dict, 100, len(tweet_1.stem_list))
    return (kl_normalize(s1) + kl_normalize(s2)) / 2.0



