import ssl
import pickle
from nltk import download
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews as mr, twitter_samples as ts
import ctypes

# for ssl certificate with nltk downloader
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# download() here, get stopwords, movie_reviews and twitter_samples

# stopwords corpus is lacking! add some punctuation it misses
noise = stopwords.words('english')
missing_noise = ['.', ',', ';', ')', '(', '[', ']', ':', '?', '!', '@', 'b']
for word in missing_noise:
    noise.append(word)


# remove noise, format appropriately as features for classifier
def prepare_data(words):
    non_noise = [word.lower() for word in words if word not in noise]
    # make dict, need in this form for classifier
    word_dict = dict([(word, True) for word in non_noise])
    return word_dict


# get negative sentiment data
neg_revs = []
for fileid in mr.fileids('neg'):
    words = mr.words(fileid)
    neg_revs.append((prepare_data(words), "negative"))

for sent in ts.strings('negative_tweets.json'):
    sent = sent.split()
    neg_revs.append((prepare_data(sent), "negative"))

# get positive sentiment data
pos_revs = []
for fileid in mr.fileids('pos'):
    words = mr.words(fileid)
    pos_revs.append((prepare_data(words), "positive"))

for sent in ts.strings('positive_tweets.json'):
    sent = sent.split()
    pos_revs.append((prepare_data(sent), "positive"))

# training set
train_set = pos_revs + neg_revs
# make classifier
classifier = NaiveBayesClassifier.train(train_set)

# pickle to save
f = open('my_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()
