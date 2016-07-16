#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     readStatus.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-15 21:01:07
# MODIFIED: 2016-07-16 10:57:41

import sys
import json
import gzip
from utils import preprocess
reload(sys)
sys.setdefaultencoding('utf-8')

def extractStatus(statusJson):
    text = ''
    try:
        status = json.loads(statusJson) 
        if status.has_key('created_at') and status['lang'] == 'en':
            originText = status['text'].replace('\n','').replace('\t','')
            processedText = preprocess(status['text'])
            if processedText != '':
                text = '%s\t%s\t%s\t%s' % (status['id_str'], status['created_at'], processedText, originText)
    except:
        print statusJson
        print 'json format error'
        exit()
    return text
    
def readData(inputFile, outputFile):
    result = open(outputFile, "w")
    try: 
        count = 0
        with gzip.open(inputFile,'rt') as fin:
            for i, line in enumerate(fin):
                text = extractStatus(line.strip())
                #skip empty tweet after stemmered, stopword removal
                if text == '': continue 
                result.write(text + "\n")
    except Exception as e:
        print e 
    result.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'argv[1]: input origin status.gzip file!'
        print 'argv[2]: output result file!'
        exit()
        
    readData(sys.argv[1], sys.argv[2])
