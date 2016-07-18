import math

def jaccard(s1, s2):
    t1 = set(s1.split(' '))
    t2 = set(s2.split(' '))
    return len(t1 & t2) / float(len(t1 | t2))

def kl(distri1, distri2):
    res = 0.0
    overlap = set(distri1.keys()) & set(distri2.keys())
    for key in overlap:
        res += distri1[key] * math.log(distri1[key] / distri2[key])
    return res

def sym_kl(distri1, distri2):
    return (kl(distri1, distri2) + kl(distri2, distri1)) / 2

def cos(vec1, vec2):
    a, b, c = 0.0, 0.0, 0.0
    for i in range(len(vec1)):
        a += vec1[i] * vec2[i]
        b += vec1[i] * vec1[i]
        c += vec2[i] * vec2[i]
    if b == 0.0 or c == 0.0:
        return 0.0
    return a / math.sqrt(b * c)

def dis(vec1, vec2):
    res = 0.0
    for i in range(len(vec1)):
        res += (vec1[i] - vec2[i]) ** 2
    return math.sqrt(res)

def similarity_q_t(query, tweet):
    return 0.25 * jaccard(query._title, tweet._text) + \
           0.25 * kl(query._distri, tweet._distri) + \
           0.25 * cos(query._vec, tweet._vec) + \
           0.25 * dis(query._vec, tweet._vec)

def similarity_t_t(tweet1, tweet2):
    return 0.25 * jaccard(tweet1._text, tweet2._text) + \
           0.25 * sym_kl(tweet1._distri, tweet2._distri) + \
           0.25 * cos(tweet1._vec, tweet2._vec) + \
           0.25 * dis(tweet1._vec, tweet2._vec)


