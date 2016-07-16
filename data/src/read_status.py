#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     readStatus.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-07-15 21:01:07
# MODIFIED: 2016-07-16 15:14:02

import sys
import json
import gzip
from utils import preprocess
reload(sys)
sys.setdefaultencoding('utf-8')

def extract_status(status_json):
    text = ''
    try:
        status = json.loads(status_json) 
        if status.has_key('created_at') and status['lang'] == 'en':
            origin_text = status['text'].replace('\n','').replace('\t','')
            processed_text = preprocess(status['text'])
            if processed_text != '':
                text = '%s\t%s\t%s\t%s' % (status['id_str'], status['created_at'], processed_text, origin_text)
    except Exception, e:
        print 'Error: ' + str(e)
        exit()
    return text
    
def read_data(input_file, output_file):
    result = open(output_file, "w")
    try: 
        with gzip.open(input_file,'rt') as fin:
            for i, line in enumerate(fin):
                text = extract_status(line.strip())
                #skip empty tweet after stemmered, stopword removal
                if text == '': continue 
                result.write(text + "\n")
    except Exception as e:
        print "Error: " + str(e)
    result.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'argv[1]: input origin status.gzip file!'
        print 'argv[2]: output result file!'
        exit()
        
    read_data(sys.argv[1], sys.argv[2])
