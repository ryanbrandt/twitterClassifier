import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time


# streamer object for tweepy
class Listener(StreamListener):

    def __init__(self, time_limit=60, tweets=None):
        self.start_time = time.time()
        self.limit = time_limit
        self.tweets = tweets
        super(Listener, self).__init__()

    # on data received, get tweepy objects, convert to json and grab full tweet, append to tweet list
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            json_load = json.loads(data)
            texts = None
            try:
                if json_load['retweeted_status']:
                    if "extended_tweet" in json_load['retweeted_status']:
                        texts = json_load['retweeted_status']['extended_tweet']['full_text']
                    else:
                        texts = json_load['retweeted_status']['text']
            except:
                pass

            if "extended_tweet" in json_load and texts == None:
                texts = json_load['extended_tweet']['full_text']
            elif texts == None:
                try:
                    texts = json_load['text'].lower()
                except KeyError:
                    pass

            self.tweets.append(texts)

            return True

        return False

    def on_error(self, status_code):
        print('error code:', status_code)


# start listener, reset tweets list
def fetch_tweets(keyword, tweets):
    auth = tweepy.OAuthHandler('SnsHkP192Jac6s8Da2AEBZabs' , '3zWgrqbYBPjbo0Fethe7PnhItLwFJDlTt9ia40Wac0jhCJiasW')
    auth.set_access_token('4910145663-br9JBO0fGQdiSYKXYx2lWWCfAbTCYpHVI50oKBW', 'LAiMxilFzO1mwgCvuvFrDakzSM3rojkLvJqqexbR6Yi08')
    api = tweepy.API(auth)
    stream = Stream(auth, listener=Listener(time_limit=2, tweets=tweets))
    stream.filter(track=[keyword])
    # tweepy fails sometimes, get rid of Nones
    tweets = list(filter(lambda x: x is not None, tweets))
    return tweets
