from collections import defaultdict

tf = defaultdict(int)
line_no = 0
for line in open("/index15/preprocess/raw_filtered.txt"):
    line_no += 1
    if line_no % 100000 == 0:
        print "%d lines" % line_no
    t = line.strip().split('\t')
    for w in t[3].split(' '):
        tf[w] += 1

total_count = 0
to_sort = []
for w in tf:
    total_count += tf[w]
    to_sort.append([w, tf[w]])
to_sort.sort(key=lambda x: x[1], reverse=True)

df = open("/index15/tf/tf_raw.dat", "w")
df.write("%d\n" % total_count)
for t in to_sort:
    df.write("%s\t%d\n" % (t[0], t[1]))
df.close()



