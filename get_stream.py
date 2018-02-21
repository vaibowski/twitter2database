import tweepy
import csv
import pymongo
from datetime import datetime
import re

col = pymongo.MongoClient()["tweets"]["trending"]


def fetch_data(query=['Trump'],max_tweets=5):
    #authenticating the API
    api_key = '9ifeYLOoCH2qjAIPZ4fEcjlao'
    api_secret = 'BSbmY12riE84QG2XlJ24gOWMWi9Fgad0cuGLVxzLuZmYfzNKnA'
    access_token = '3466069694-TrZMbQhe5Duidvtd9N6R8UJiBBV1Uz6jaWyFBfn'
    access_token_secret = 'O4I32DLMenUYnYKxPxA1fIepR9LRA7MwhUbdDvKAjrt9L'

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #listener to receive the stream
    class Listener(tweepy.StreamListener):
        counter = 0

        def __init__(self, max_tweets=1000, *args, **kwargs):
            self.max_tweets = max_tweets
            self.counter = 0
            super().__init__(*args, *kwargs)
            self.start_time = datetime.now()

        def on_connect(self):
            self.counter = 0
            self.start_time = datetime.now()

        def on_status(self, status):
            # Incrementing the counter
            self.counter += 1

            # storing tweet in MongoDB
            col.insert_one(status._json)
            print(self.counter)
            if self.counter >= self.max_tweets:
                myStream.disconnect()
                print("Finished")

    myStreamListener = Listener(max_tweets)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # Start a filter with an error counter of 20
    for error_counter in range(20):
        try:
            myStream.filter(track=query)
            print("Tweets collected: %s" % myStream.listener.counter)
            print("Total tweets in collection: %s" % col.count())
            break
        except:
            print("ERROR# %s" % (error_counter + 1))


regex = re.compile('.*')


# search function with filters name, retweet count and favourites filter in mongoDB
# using skip and filter for pagination
def search(name=regex, rt_count=0, favourites_count=0,
           per_page=5, page_no=1):

    cursor = col.find(
        {"user.name": name, "retweet_count": {"$gte": rt_count}, "user.favourites_count": favourites_count,
        }).skip((page_no - 1) * per_page).limit(per_page)

    cursor = list(cursor)
    print(cursor)


    # exporting to csv file
    with open('trending.csv', 'w') as outfile:
        fields = ['user_name', 'retweet_count', 'favourites_count', 'created_at']
        write = csv.DictWriter(outfile, fieldnames=fields)
        write.writeheader()
        for data in cursor:
            write.writerow({
                'user_name': data['user']['name'],
                'retweet_count': data['retweet_count'],
                'favourites_count': data['user']['favourites_count'],
                'created_at': data['created_at']
            })



