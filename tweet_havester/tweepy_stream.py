#  -*- coding: utf-8 -*-
import json
import os
import tweepy
import couchdb
import threading
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from sklearn.externals import joblib

class listener(StreamListener):
    def __init__(self,path):
        self.couch = couchdb.Server(path)
        self.model = joblib.load("./train_model.m")
    def convertValue(self,origin):
        dic = {}
        dic['_id'] = origin["id_str"]
        dic['create_time'] = origin["created_at"]
        dic['user_id'] = origin['user']['id']
        dic['text'] = origin["text"]
        dic['lang'] = origin["lang"]
        if(origin["place"] != None):
            dic['location'] = origin["place"]["name"]
        else:
            dic['location'] = "None"
        return dic
    def on_data(self,data):
        try:
            db = self.couch['raw_tweets']
            id_db = self.couch['user_id']
            pc_db = self.couch['tweet_results']
            content = json.loads(data)
            dic = self.convertValue(content)
            id_doc = {"_id":str(dic["user_id"]),"user_name":content['user']['name'],"isSearched":False}
            # print(id_doc)
            p_dic = date_process(dic,self.model)
            if p_dic != None:
                process_db.save(p_dic)
            id_db.save(id_doc)
            db.save(dic)
            # print("success")
            pass
        except:
            pass
        
        return True
    def on_error(self,status):
        print(status)

class TweetStreamHavester():
    def __init__(self,server_path):
        self.server_path = server_path
    def process(self,city):
        #args是关键字参数，需要加上名字，写成args=(self,)
        print("start streaming"+city)
        th = threading.Thread(target=TweetStreamHavester.run, args=(self,city))
        th.start()
        th.join()
    def run(self, city):
        dict = {}
        with open('./tweet_havester_config.json','r') as f:
            dict = json.load(f)
            api_token = dict[city]["API"]["stream"]
            stream_area = dict[city]["bound"]
            consumer_key = api_token["consumer_key"]
            consumer_secret = api_token["consumer_secret"]
            access_token = api_token["access_token"]
            access_token_secret = api_token["access_token_secret"]
            auth = OAuthHandler(consumer_key,consumer_secret)
            auth.set_access_token(access_token,access_token_secret)
            twitterStream = Stream(auth,listener(self.server_path))
            twitterStream.filter(locations=stream_area,is_async = True)
        
        f.close()

if __name__ == "__main__":
    couch = couchdb.Server('http://admin:password@127.0.0.1:5984/')
    # couch.create('raw_tweets')
    # couch.create('new_stream_tweet')
    server_path = 'http://127.0.0.1:5984/'
    a = TweetStreamHavester(server_path)
    try:
        a.process("melbourne")
        a.process("sydney")
        a.process("adelaide")
        a.process("brisbane")
        a.process("perth")
    except Exception as e:
        print(e)
    pass




