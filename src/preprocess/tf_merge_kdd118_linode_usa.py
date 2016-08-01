tf = {}

def add(file_path):
    line_no = 0
    for line in open(file_path):
        line_no += 1
        if line_no == 1:
            continue
        t = line.strip().split('\t')
        w, cnt = t[0], int(t[1])
        if w not in tf:
            tf[w] = 0
        tf[w] += cnt

add("/index15/tf/tf_merge_kdd118.txt")
add("/index15/tf/tf_merge_linode_usa.txt")

total_count = 0
to_sort = []
for w in tf:
    total_count += tf[w]
    to_sort.append([w, tf[w]])
to_sort.sort(key=lambda x: x[1], reverse=True)

df = open("/index15/tf/tf_merge_kdd118_linode_usa.txt", "w")
df.write("%d\n" % total_count)
for t in to_sort:
    df.write("%s\t%d\n" % (t[0], t[1]))
df.close()



