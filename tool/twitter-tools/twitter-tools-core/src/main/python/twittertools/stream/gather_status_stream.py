# Twitter Tools
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import logging
import logging.handlers
import MySQLdb
import sys
sys.path.append('../../../../../../../../src')
from package.tweet import Tweet
from package.utils import load_stopword_set

consumer_key="cYB00c5FkSbCY2oMyAqQ"
consumer_secret="eSg9pvRc1Q57yzH8W0cj2feziw7dUfvKyW3QzKPsBN4"

access_token="1661733726-nkRPTWH4UFi2rYfhr7qKM1P3Mo8OaMyVYdyjGcB"
access_token_secret="lt5GOQsOOBdJVRsCyOCdQdYnDkpJcsK1YMq93E8Y0"

stopword_set = load_stopword_set()

class TweetListener(StreamListener):

    def __init__(self,api=None):
        super(TweetListener,self).__init__(api)
        self.logger = logging.getLogger('tweetlogger')

        
        statusHandler = logging.handlers.TimedRotatingFileHandler('status.log',when='H',encoding='bz2',utc=True)
        statusHandler.setLevel(logging.INFO)
        self.logger.addHandler(statusHandler)
        

        warningHandler = logging.handlers.TimedRotatingFileHandler('warning.log',when='H',encoding='bz2',utc=True)
        warningHandler.setLevel(logging.WARN)
        self.logger.addHandler(warningHandler)
        logging.captureWarnings(True)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.WARN)
        self.logger.addHandler(consoleHandler)


        self.logger.setLevel(logging.INFO)
        self.count = 0
        self.cache = []

    def on_data(self,data):
        self.count+=1
        self.logger.info(data)
        self.cache.append(data)
        if self.count % 1000 == 0:
            print "%d statuses processed" % self.count
            try:
                insert_data = []
                for raw_json in self.cache:
                    t = Tweet(raw_json, stopword_set)
                    if t.is_valid:
                        insert_data.append([t.created_at, t.id_str, " ".join(t.word_list), " ".join(t.stem_list)])
                if len(insert_data) > 0:
                    conn=MySQLdb.connect(host='localhost',user='root',passwd='webkdd',db='trec16',port=3306)
                    cur=conn.cursor()
                    cur.executemany('INSERT INTO raw (created_at, id_str, word_list_str, stem_list_str) VALUES (%s, %s, %s, %s)', insert_data)
                    conn.commit()
                    cur.close()
                    conn.close()
                self.cache = []
                print "%d tweets are inserted" % len(insert_data)
            except Exception, e:
                print e
        return True

    def on_error(self,exception):
        self.logger.warn(str(exception))

if __name__ == '__main__':
    listener = TweetListener()
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    stream = Stream(auth,listener)
    while True:
        try:
            stream.sample()
        except Exception as ex:
            print str(ex)
            pass



