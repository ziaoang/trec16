import math

def normalize(score):
    max = 0.0
    min = -20.0
    return float(score - min) / (max - min)

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
    if score > max_v: score = max_v
    if score < min_v: score = min_v
    return (score - min_v) / (max_v - min_v)

def jm_score(query, tweet, corpus_dict):
    lamda = 0.2
    return kl_normalize(kl_jm(query.stem_distri, tweet.stem_distri, corpus_dict, lamda))

def dir_score(query, tweet, corpus_dict):
    mu = 100
    return kl_normalize(kl_dirichlet(query.stem_distri, tweet.stem_distri, corpus_dict, mu, len(tweet.stem_list)))

def sym_dir_score(tweet_1, tweet_2, corpus_dict):
    score_1 = dir_score(tweet_1, tweet_2, corpus_dict)
    score_2 = dir_score(tweet_2, tweet_1, corpus_dict)
    return (score_1 + score_2) / 2.0

def cos(vector_1, vector_2):
    a, b, c = 0.0, 0.0, 0.0
    for i in range(100):
        a += vector_1[i] * vector_2[i]
        b += vector_1[i] * vector_1[i]
        c += vector_2[i] * vector_2[i]
    if b == 0.0 or c == 0.0:
        return 0.0
    cos_score = a / math.sqrt(b * c)
    return ( cos_score + 1.0 ) / 2

def cos_score(query, tweet):
    return cos(query.vector, tweet.vector)

def similarity_q_t(query, tweet, corpus_dict):
    return dir_score(query, tweet, corpus_dict)

def similarity_t_t(tweet_1, tweet_2, corpus_dict):
    return sym_dir_score(tweet_1, tweet_2, corpus_dict)

def similarity_q_t2(query, tweet, corpus_dict, method):
    distribution_q = query.stem_distri
    distribution_t = tweet.stem_distri
    distribution_c = corpus_dict
    if method == "jm":
        lamda = 0.2
        score = kl_jm(distribution_q, distribution_t, distribution_c, lamda)
        return normalize(score)
    if method == "dirichlet":
        mu = 100
        t_len = len(tweet.stem_list)
        score = kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t_len)
        return normalize(score)
    print "Wrong method in similarity_q_t(), expected 'jm' or 'dirichlet'!"
    exit()
    

def similarity_t_t2(tweet_1, tweet_2, corpus_dict, method):
    distribution_q = tweet_1.stem_distri
    distribution_t = tweet_2.stem_distri
    distribution_c = corpus_dict
    t1 = len(tweet_1.stem_list)
    t2 = len(tweet_2.stem_list)
    if method == "jm":
        lamda = 0.2
        s1 = kl_jm(distribution_q, distribution_t, distribution_c, lamda)
        s2 = kl_jm(distribution_t, distribution_q, distribution_c, lamda)
        return normalize(float(s1 + s2) / 2)
    if method == "dirichlet":
        mu = 100
        s1 = kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t2)
        s2 = kl_dirichlet(distribution_t, distribution_q, distribution_c, mu, t1)
        return normalize(float(s1 + s2) / 2)
    print "Wrong method in similarity_t_t(), expected 'jm' or 'dirichlet'!"
    exit()
    


