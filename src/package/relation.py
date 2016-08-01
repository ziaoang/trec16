import math

##################################################
def kl_normalize(score):
    max_v = 0.0
    min_v = -20.0
    if score > max_v: score = max_v
    if score < min_v: score = min_v
    return (score - min_v) / (max_v - min_v)

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
    alpha = float(mu) / (t_len + mu)
    return kl_jm(distribution_q, distribution_t, distribution_c, alpha)


##################################################
def jm2_score(query, tweet, corpus_dict):
    lamda = 0.2
    return kl_normalize(kl_jm(query.stem_distri, tweet.stem_distri, corpus_dict, lamda))

def sym_jm2_score(tweet_1, tweet_2, corpus_dict):
    score_1 = jm2_score(tweet_1, tweet_2, corpus_dict)
    score_2 = jm2_score(tweet_2, tweet_1, corpus_dict)
    return (score_1 + score_2) / 2.0

def jm5_score(query, tweet, corpus_dict):
    lamda = 0.5
    return kl_normalize(kl_jm(query.stem_distri, tweet.stem_distri, corpus_dict, lamda))

def sym_jm5_score(tweet_1, tweet_2, corpus_dict):
    score_1 = jm5_score(tweet_1, tweet_2, corpus_dict)
    score_2 = jm5_score(tweet_2, tweet_1, corpus_dict)
    return (score_1 + score_2) / 2.0

def dir_score(query, tweet, corpus_dict):
    mu = 100
    return kl_normalize(kl_dirichlet(query.stem_distri, tweet.stem_distri, corpus_dict, mu, len(tweet.stem_list)))

def sym_dir_score(tweet_1, tweet_2, corpus_dict):
    score_1 = dir_score(tweet_1, tweet_2, corpus_dict)
    score_2 = dir_score(tweet_2, tweet_1, corpus_dict)
    return (score_1 + score_2) / 2.0



