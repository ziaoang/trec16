import os
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
    base_path = "../data/data15/submit/"
    file_names = [f for f in listdir(base_path) if isfile(join(base_path, f))]
    file_names.sort()
    for file in file_names:
        print file
        full_path = base_path + file
        if os.stat(full_path).st_size == 0: continue
        eval_file = open('evalA.res','a')
        cmd = 'python ../data/data15/real-time-filtering-modelA-eval.py -q ../data/data15/qrels.txt -c ../data/data15/clusters-2015.json.txt -r ' + full_path + ' > tmp.res'
        os.system(cmd)
        tmpFile = open('tmp.res','r')
        line = tmpFile.readline()
        info = line.strip().split()
        out_line = '%s\t%s\t%s\n' % (full_path, info[1],info[2])
        eval_file.write(out_line)


