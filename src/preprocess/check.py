a = set()
for line in open("/index15/preprocess/filter_raw_19_29.txt"):
    t = line.strip().split('\t')
    a.add(t[1])

b = set()
for line in open("/index15/preprocess/filter_1507_19_29.txt"):
    t = line.strip().split('\t')
    b.add(t[1])

print(len(a))
print(len(b))
print(len(a-b))
print(len(b-a))
print(len(a&b))
print(len(a|b))



