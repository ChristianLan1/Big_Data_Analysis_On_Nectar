import tweepy_search as tSearch
import tweepy_stream as tStream
import time
import sys

if __name__ == "__main__":
    server_path = ""
    a=sys.argv
    if(len(a) == 4):
        ip = a[1]
        username = a[2] 
        password = a[3]
        server_path = 'http://' + username +':' + password +'@'+ip+':5984/'
    else:
        server_path = 'http://'+a[1]
    tStream.run(server_path)
    # wait for streamming for a while to start searching
    # time.sleep(200)
    tSearch.run(server_path)
