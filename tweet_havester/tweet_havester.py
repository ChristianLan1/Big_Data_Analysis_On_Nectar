import tweepy_search as tSearch
import tweepy_stream as tStream
import time

if __name__ == "__main__":
    server_path = 'http://admin:password@127.0.0.1:5984/'

    tStream.run(server_path)
    # wait for streamming for a while to start searching
    time.sleep(200)
    tSearch.run(server_path)
