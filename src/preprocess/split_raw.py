df = open("/index15/preprocess/filter_raw_19_29.txt", "w")
for line in open("/index15/preprocess/filter_raw.txt"):
    t = line.strip().split('\t')
    tt = t[0].split(' ')
    day = int(tt[2])
    if day >= 19 and day <= 29:
        df.write(line)
df.close()
    


