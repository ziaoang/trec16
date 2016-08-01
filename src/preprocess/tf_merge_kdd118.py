tid_set = set()
tf = {}

def add(file_path):
    for line in open(file_path):
        t = line.strip().split('\t')
        tid, stem_list_str = t[1], t[3]
        if tid not in tid_set:
            tid_set.add(tid)
            for w in stem_list_str.split(' '):
                if w not in tf:
                    tf[w] = 0
                tf[w] += 1

add("/index15/preprocess/preprocess_raw.txt")
add("/index15/preprocess/preprocess_1507.txt")

total_count = 0 
to_sort = []
for w in tf: 
    total_count += tf[w]
    to_sort.append([w, tf[w]])
to_sort.sort(key=lambda x: x[1], reverse=True)

df = open("/index15/tf/tf_merge_kdd118.txt", "w")
df.write("%d\n" % total_count)
for t in to_sort:
    df.write("%s\t%d\n" % (t[0], t[1]))
df.close()



