#  -*- coding: utf-8 -*-
import json
import os
import couchdb
import tweepy
from tweepy import OAuthHandler
from sklearn.externals import joblib
import general_process as gp


class TweetSearchHavester():
    def __init__(self,couch):
        self.couch = couch
        self.model = joblib.load("./train_model.m")

    def run(self, ids , city):
        dict = {}
        with open('./tweet_havester_config.json','r') as f:
            dict = json.load(f)
            api_token = dict[city]["API"]["search"]
            stream_area = dict[city]["bound"]
            consumer_key = api_token["consumer_key"]
            consumer_secret = api_token["consumer_secret"]
            access_token = api_token["access_token"]
            access_token_secret = api_token["access_token_secret"]

            auth = OAuthHandler(consumer_key,consumer_secret)
            auth.set_access_token(access_token,access_token_secret)
            api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            for id in ids:
                try:
                    self.get_all_tweets(id,api)
                except tweepy.TweepError:
                    print ('Failed to run the command on that user, Skipping...')
                except IndexError:
                    print ('List index out of range, Skipping...')
        
        f.close()
    
    def get_all_tweets(self, user_id, api):
        new_tweets = api.user_timeline(user_id=user_id, count=50)
        db = self.couch['raw_tweets']
        process_db = self.couch['tweet_results']
        for tweet in tweepy.Cursor(api.user_timeline,id = user_id ).items(50):
            # save most recent tweets
            dic = {}
            dic['_id'] = tweet.id_str
            dic['create_time'] = str(tweet.created_at)
            dic['user_id'] = tweet.user.id
            dic['text'] = tweet.text
            dic['lang'] = tweet.lang
            if(tweet.place != None):
                dic['location'] = tweet.place.name 
            else:
                dic['location'] = tweet.user.location
            # print(dic)
            try:
                p_dic = gp.data_process(dic,self.model)
                print(p_dic)
                if p_dic != None:
                    process_db.save(p_dic)
                db.save(dic)
            except:
                pass
        # write to db
        



def run(server_path):
    couch = couchdb.Server(server_path)
    db = couch['user_id']
    # couch.create('test_db')
    dict = {}
    with open('./tweet_havester_config.json','r') as f:
        dict = json.load(f)
    cities = []
    for city in dict:
        cities.append(city)
    switch = 0
    count = 0
    ids = list()
    a = TweetSearchHavester(couch)
    while True:
        print("start a new round")
        for id in db:
            data = db[id]
            if(not data['isSearched']):
                ids.append(id)
                count+=1
            else:
                continue
            if(count > 20):
                switch = (switch+1)%5
                count = 0
                a.run(ids,cities[switch])
                for id in ids:
                    data = db[id]
                    data['isSearched'] = True
                    db.save(data)
                ids = list()
        print("finsh a round")
    