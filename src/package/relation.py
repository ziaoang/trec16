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
            # print key, "in t!"
            # print "distribution: ", distribution_t[key]
            smooth += (1 - lamda) * distribution_t[key]
        if key in distribution_c:
            '''
            print key, "in c!"
            print "distribution: ", distribution_c[key]
            if key == "hershey": distribution_c[key] = 4.98517e-06
            if key == "pa":     distribution_c[key] = 0.000114567
            if key == "quilt":  distribution_c[key] = 1.37092e-05
            if key == "show":   distribution_c[key] = 0.00195049
            print "distribution: ", distribution_c[key]
            '''
            smooth += lamda * distribution_c[key]
        if smooth != 0: 
            flag = True
            # print "smooth: ", smooth
            res += distribution_q[key] * math.log(smooth)
    if flag: return res
    else: return -999999.0

# Notice, t_len is len(tweet.stem_list), different from len(distribution_t)
def kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t_len):
    res = 0.0
    flag = False
    for key in distribution_q:
        smooth = 0
        alpha = float(mu) / (t_len + mu);
        if key in distribution_t: 
            # print key, "in t"
            # print "distribution: ", distribution_t[key]
            smooth += (1 - alpha) * distribution_t[key]
        if key in distribution_c: 
            '''
            print key, "---------->in c!"
            if key == "hershey": distribution_c[key] = 4.98517e-06
            if key == "pa":     distribution_c[key] = 0.000114567
            if key == "quilt":  distribution_c[key] = 1.37092e-05
            if key == "show":   distribution_c[key] = 0.00195049
            print "distribution: ", distribution_c[key]
            '''
            smooth += alpha * distribution_c[key]
        if smooth != 0: 
            flag = True
            # print "smooth: ", smooth
            res += distribution_q[key] * math.log(smooth)
    if flag: return res
    else: return -999999.0
        

        
def cos(vector_1, vector_2):
    a, b, c = 0.0, 0.0, 0.0
    for i in range(len(vector_1)):
        a += vector_1[i] * vector_2[i]
        b += vector_1[i] * vector_1[i]
        c += vector_2[i] * vector_2[i]
    if b == 0.0 or c == 0.0:
        return 0.0
    return a / math.sqrt(b * c)

def similarity_q_t(query, tweet, corpus_dict):
    distribution_q = query.stem_distri
    distribution_t = tweet.stem_distri
    distribution_c = corpus_dict
    mu = 100
    t_len = len(tweet.stem_list)
    return kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t_len)
    # jaccard_score = jaccard(query.word_list, tweet.word_list)
    # kl_score = kl(query.distribution, tweet.distribution)
    # cos_score = cos(query.vector, tweet.vector)
    # return 0.33 * jaccard_score + 0.33 * kl_score + 0.33 * cos_score
    

def similarity_t_t(tweet_1, tweet_2, corpus_dict):
    distribution_q = tweet_1.stem_distri
    distribution_t = tweet_2.stem_distri
    distribution_c = corpus_dict
    mu = 100
    t_len = len(tweet_2.stem_list)
    s1 = kl_dirichlet(distribution_q, distribution_t, distribution_c, mu, t_len)
    t_len = len(tweet_1.stem_list)
    s1 = kl_dirichlet(distribution_t, distribution_q, distribution_c, mu, t_len)
    return float(s1 + s2) / 2
    # jaccard_score = jaccard(tweet_1.word_list, tweet_2.word_list)
    # sym_kl_score = sym_kl(tweet_1.distribution, tweet_2.distribution)
    # cos_score = cos(tweet_1.vector, tweet_2.vector)
    # return 0.33 * jaccard_score + 0.33 * sym_kl_score + 0.33 * cos_score


