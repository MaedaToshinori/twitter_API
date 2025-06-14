
import json
import csv
import config
from natural_word6 import Word_data
from requests_oauthlib import OAuth1Session
import time
import MeCab
import pandas as pd

class Twitter_API:
    def __init__(self):
        # OAuth認証部分
        self.CK      = config.CONSUMER_KEY
        self.CS      = config.CONSUMER_SECRET
        self.AT      = config.ACCESS_TOKEN
        self.ATS     = config.ACCESS_TOKEN_SECRET
        self.twitter = OAuth1Session(self.CK, self.CS, self.AT, self.ATS)


    def api_word(self,url,keyword):
        # Twitter Endpoint(検索結果を取得する)
        self.pos_pd = pd.DataFrame(columns=["user_id",
                                             "tw_text",
                                             "comp_text",
                                             "pos", "neg",
                                             "RT",
                                             "good"])
        self.pos_pd.head(5)
        self.neg_pd = pd.DataFrame(columns=["user_id",
                                             "tw_text",
                                             "comp_text",
                                             "pos", "neg",
                                             "RT",
                                             "good"])
        self.neg_pd.head(5)

        tweet_id = 'max_id'
        all_count=0
        getdata_count=0
        while getdata_count<=5000:
            data_count=0
            certification=0
            while certification <= 180:
                params ={
                            'count' : 100,      # 取得するtweet数
                            'exclude': 'retweets',   #RTを除外
                            'result_type': 'recent',    #時系列で取得
                            'max_id': tweet_id,
                            'q'     : keyword
                            }
                req = self.twitter.get(url, params = params)
                if req.status_code == 200:
                    res = json.loads(req.text)
                    for tweet in res['statuses']:
                        data_count += 1
                        all_count += 1
                        print(all_count)
                        if tweet['in_reply_to_screen_name'] == None:
                            list=[]
                            #print(tweet['user']['screen_name'])
                            print(tweet['text'])
                            mecab_test=self.word_natural.mecab_list(tweet['text'])
                            twitter_result=self.word_natural.word_datacheck(mecab_test)

                            if twitter_result=="Pos":
                                pos_tweet=True
                                neg_tweet=False
                                addRow = pd.DataFrame([tweet['user']['screen_name'],
                                                       tweet['text'],
                                                       mecab_test,
                                                       pos_tweet,
                                                       neg_tweet,
                                                       tweet['retweet_count'],
                                                       tweet['favorite_count']],
                                                      index=self.pos_pd.columns).T  # .Tで行と列を入れ替える
                                self.pos_pd = self.pos_pd.append(addRow,
                                                                 ignore_index=True)
                            # ignore_index=True パラメータを指定することで、新たな行番号を割り当てることができます。
                            elif twitter_result == "Neg":
                                pos_tweet = False
                                neg_tweet = True
                                addRow = pd.DataFrame([tweet['user']['screen_name'],
                                                       tweet['text'],
                                                       mecab_test,
                                                       pos_tweet,
                                                       neg_tweet,
                                                       tweet['retweet_count'],
                                                       tweet['favorite_count']],
                                                      index=self.pos_pd.columns).T  # .Tで行と列を入れ替える
                                self.neg_pd = self.neg_pd.append(addRow,
                                                                 ignore_index=True)
                            # ignore_index=True パラメータを指定することで、新たな行番号を割り当てることができます。
                            elif twitter_result=="None":
                                continue

                            getdata_count+=1
                            #tweet_id =int(tweet['id'])-1
                            print('*******************************************')

                else:
                    print("Failed: %d" % req.status_code)

                tweet_id = int(tweet['id']) - 1
                certification+=1
                print("certification="+str(certification))


            print("waiting......")
            time.sleep(910)

        print(data_count)
        print(getdata_count)
        print(all_count)

url = 'https://api.twitter.com/1.1/search/tweets.json'
keyword = '在宅勤務 -filter:links'
api=Twitter_API()

api.word_natural = Word_data()
api.word_natural.Emotion=api.word_natural.csv_read()
print(api.word_natural.Emotion)


# Enedpointへ渡すパラメーター
api.api_word(url,keyword)
print(api.pos_pd)
print(api.neg_pd)
print("posツイートのいいね平均="+str(api.pos_pd["good"].mean()))
print("negツイートのいいね平均="+str(api.neg_pd["good"].mean()))
api.pos_pd.to_csv("pos.csv" , encoding='utf_8_sig')
api.neg_pd.to_csv("neg.csv" , encoding='utf_8_sig')
