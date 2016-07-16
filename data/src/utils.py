#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     utils.py
# ROLE:     This module contains various general utility functions
# CREATED:  2016-07-15 21:00:56
# MODIFIED: 2016-07-15 21:00:58

import json
import nltk
import string
import urllib2
import re
from bs4 import BeautifulSoup
from ssl import SSLError
import socket
import httplib
import urlparse

socket.setdefaulttimeout(0.5)

def loadStopWord(filePath):
    stopwordFile = open(filePath,'r')
    stopwordDict = {}
    for line in stopwordFile:
        stopwordDict[line.strip()] = True
    return stopwordDict
    
def non_ascii_term(term):
    ascii_reg = re.compile(r'^[\x00-\x7F]+$')
    if ascii_reg.match(term):
        return True
    else:
        return False

def link_term(term):
    url_reg = re.compile(r'(https?://)+(\w+\.)+\w+(/\w+)*/*')
    if url_reg.search(term):
        return True
    else:
        return False

def non_ascii_url_term(term):
    ascii_reg = re.compile(r'^[\x00-\x7F]+$')
    url_reg = re.compile(r'(https?://)+(\w+\.)+\w+(/\w+)*/*')
    if ascii_reg.match(term) and not url_reg.search(term):
        return True
    else:
        return False

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url
        
def crawlTitleFromUrl(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    long_url = unshorten_url(url)
    try:
        request = urllib2.Request(long_url, headers=hdr)
        connection = urllib2.urlopen(request,timeout=0.5)
        soup = BeautifulSoup(connection.read(10240),'html.parser')
        connection.close()
        title = soup.title.string
        title = title.replace('&quot','')
        space_reg = re.compile('\s+')
        term_list = space_reg.split(title)
        title = filter(non_ascii_url_term,term_list)
        return ' '.join(title)    
    except urllib2.HTTPError, e:
        print 'Miss1',str(e)
    except urllib2.URLError, e1:
        print 'MIss2',str(e1)
    except SSLError, e2:
        print 'Miss3',str(e2)
    except Exception, e3:
        print 'Miss4',str(e3)
    return ''
    

def preprocess(tweetText):
    stopwordDict = loadStopWord('stopword')
    text = tweetText.replace('\n','').replace('\t','')
    if text.find('RT @') >= 0:  
        rt_token = text.split('RT ')
        text = ' '.join(rt_token[1:])
    space_reg = re.compile('\s+')
    term_list = space_reg.split(text.lower())
    # remove stopword,  @username, rt
    filtered_term_list = [term for term in term_list if not term == '' and not term == 'rt' and not stopwordDict.has_key(term) and not term[0]=='@']
    filtered_term_list2 = filter(non_ascii_term, filtered_term_list)
    text = ' '.join(filtered_term_list2)
    url_reg = re.compile(r'(https?://+\w+\.+\w+/\w+)')
    url_list = url_reg.findall(text)
    url_text = ''
    for url in url_list:
        text = text.replace(url,'')
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    tokens = nltk.word_tokenize(text.lower())
    filtered_tokens = tokens
    porter = nltk.PorterStemmer()
    stem_tokens = [porter.stem(token.encode('utf-8')) for token in filtered_tokens if not token=='' and not token =='rt' and not stopwordDict.has_key(token) and not token.isdigit()]
    return ' '.join(stem_tokens)


