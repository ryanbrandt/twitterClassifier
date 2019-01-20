import tweepy
import pickle
import nltk
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
from make_classifier import prepare_data


# streamer for tweepy data, has time limit for training for each keyword
class Listener(StreamListener):

    def __init__(self, time_limit=60, tweets=None):
        self.start_time = time.time()
        self.limit = time_limit
        self.tweets = tweets
        super(Listener, self).__init__()

    # on data received, get text from json data tweepy returns, append to sentences list
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            json_load = json.loads(data)
            texts = json_load['text'].lower()
            self.tweets.append(texts)
            #print('tweet :' + str(texts.split()))
            #print('')
            #print(' --- ANALYSIS --- ')
            #prob_dict = classifier.prob_classify(prepare_data(texts.split()))
            #for sample in prob_dict.samples():
             #   print(prob_dict.prob(sample))
            #time.sleep(1)
            #print(classifier.classify(prepare_data(texts.split())))
            #print('')
            return True

        return False


    def on_error(self, status_code):
        print('error code:', status_code)


# start listener, reset tweets list
def fetch_tweets(keyword, tweets):
    auth = tweepy.OAuthHandler('SnsHkP192Jac6s8Da2AEBZabs' , '3zWgrqbYBPjbo0Fethe7PnhItLwFJDlTt9ia40Wac0jhCJiasW')
    auth.set_access_token('4910145663-br9JBO0fGQdiSYKXYx2lWWCfAbTCYpHVI50oKBW', 'LAiMxilFzO1mwgCvuvFrDakzSM3rojkLvJqqexbR6Yi08')
    api = tweepy.API(auth)
    stream = Stream(auth, listener=Listener(time_limit=5, tweets=tweets))
    stream.filter(track=[keyword])
    return tweets
