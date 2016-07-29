#!/usr/bin/sh
# AUTHOR:   yaolili
# FILE:     runTopK.sh
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-29 21:17:52
# MODIFIED: 2016-07-29 21:18:00

for ((k=4; k<=10; k++)); do
    python topK.py ../data/data15/rankScore3/ $k ../data/data15/threshold/
done;
