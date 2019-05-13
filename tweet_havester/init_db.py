import couchdb
import sys

def run(server_path):
    couch = couchdb.Server(server_path)
    couch.create('tweet_2014_raw')
    couch.create('raw_tweets')
    couch.create('tweet_2014_results')
    couch.create('tweet_results')
    couch.create('user_id')
    print("create all db successful")


if __name__ == "__main__":
    a=sys.argv
    if(len(a) == 4):
        ip = a[1]
        username = a[2] 
        password = a[3]
        path = 'http://' + username +':' + password +'@'+ip+':5984/'
    else:
        path = 'http://admin:password@127.0.0.1:5984/'
    run(path)
    pass
