from sklearn.externals import joblib
import json
import couchdb
model = joblib.load("train_model.m")

dataset=[]

user = "admin"
password = "password"
dbserver = couchdb.Server("http://admin:password@172.26.38.157:5984/")
db=dbserver["raw_tweets"]
r_db =  dbserver["tweet_results"]
count=0
dataset=["1"]

####filter cities
cities =['melbourne','sydney','adelaide','perth','brisbane']

for id in db:
    tweet=db.get(id)
    text = tweet['text']
    lang = tweet['lang']
    location = tweet['location']
    create_time = tweet['create_time']
    user_id = tweet['user_id']

    
    #find the target city
    flag = False
    for city in cities:
        #the location contains target city names
        if city in location.lower():
            #generalize city name
            flag = True
            location=city
    #not in target cities,continue
    if flag == False:
         continue

    p_tweet = {
    '_id':id,
    'user_id':user_id,
    "create_time":create_time,
    "location":location,
    "lang":lang,
    'text':text
    }
    if lang =='en':
        dataset[0]=text
        predicts = model.predict(dataset)
        if predicts[0]==1:
            r_db.save(p_tweet) 






