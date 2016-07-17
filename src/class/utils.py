def distribution(s):
    res = {}
    t = s.split(' ')
    for w in t:
        if w not in res:
            res[w] = 0
        res[w] += 1
    length = float(len(t))
    for w in res:
        res[w] /= length
    return res

def vector(s):
    res = [0.0] * 100
    return res


