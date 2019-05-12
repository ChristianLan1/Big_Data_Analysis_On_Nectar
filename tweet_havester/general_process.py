from sklearn.externals import joblib
import json
import couchdb
model = joblib.load("train_model.m")

def data_process(tweet,model):
    ####filter cities
    cities =['melbourne','sydney','adelaide','perth','brisbane']
    dataset=['0']
    id = tweet['_id']
    text = tweet['text']
    lang = tweet['lang']
    ##we only care English
    if lang != 'en':
        return None 
    location = tweet['location']
    create_time = tweet['create_time']

    for city in cities:
        #the location contains target city names
        if city in location.lower():
            #generalize city name
            location=city
    
    p_tweet={
    '_id':id,
    "create_time":create_time,
    "location":location,
    "lang":lang,
    'text':text,
    'if_offensive':"false"
    }
    dataset[0]=text
    predicts = model.predict(dataset)
    if predicts[0]==1:
        p_tweet['if_offensive']="true"
    return p_tweet


# tweet1={
#   "_id": "1000029867289690113",
#   "_rev": "1-6fec69500a19192444c2de7e13c37a08",
#   "create_time": "2018-05-25 15:04:34",
#   "user_id": 847624802,
#   "text": "@maiiron_ Teve loco que até Jesus Cristo citou. Buguei meu",
#   "lang": "pt",
#   "location": "Sydney"
#     }
# tweet2={
#   "_id": "1000108067982200832",
#   "_rev": "1-d23d7bd9bf292aee6423360ac45abb76",
#   "create_time": "2018-05-25 20:15:19",
#   "user_id": 3104553206,
#   "text": "Finished #plant18 https://t.co/GOWl6bsQUO",
#   "lang": "en",
#   "location": "Kimba"
# }
# tweet3={
#   "_id": "1000641327279824896",
#   "_rev": "1-bafd33be6cd735694ddcf9557c34656e",
#   "create_time": "2018-05-27 07:34:18",
#   "user_id": 110366337,
#   "text": "Veer's arrival &amp; Rivi's 5th bday Party https://t.co/xZmhoMgV76",
#   "lang": "en",
#   "location": "Melbourne, Australia"
# }
# p=data_process(tweet3)
# print(p)

