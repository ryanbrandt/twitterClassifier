import ssl
import pickle
from nltk import download
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples as ts
import csv

''' Make Classifier; Using Kaggle & NLTK Corpus Data '''

# for ssl certificate with nltk downloader
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# download() here, get stopwords and twitter_samples

# stopwords corpus is lacking! add some punctuation it misses
noise = stopwords.words('english')


# remove noise, format appropriately as features for classifier
def prepare_data(words):
    non_noise = [word.lower() for word in words if word not in noise]
    # make dict, need in this form for classifier
    word_dict = dict([(word, True) for word in non_noise])
    return word_dict


neg_dat = []
pos_dat = []
'''
# general tweet dataset
with open('training.csv', encoding="latin") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 0:
            neg_dat.append((prepare_data(row[5].split()), "negative"))
        elif row[0] == 4:
            pos_dat.append((prepare_data(row[5].split()), "positive"))

# GOP debate tweet dataset
with open('sentiment.csv', encoding="latin") as g:
    reader = csv.reader(g)
    for row in reader:
        if row[5] == 'Negative' and float(row[6]) > 0.5:
            neg_dat.append((prepare_data(row[15].split()), "negative"))
        elif row[5] == 'Positive' and float(row[6]) > 0.5:
            pos_dat.append((prepare_data(row[15].split()), "positive"))

# airline tweets dataset
with open('Tweets.csv', encoding="latin") as h:
    reader = csv.reader(h)
    for row in reader:
        if row[2] == 'negative' and float(row[3]) > 0.5:
            neg_dat.append((prepare_data(row[10].split()), "negative"))
        elif row[2] == 'positive' and float(row[3] > 0.5):
            pos_dat.append((prepare_data(row[10].split()), "positive"))
'''
# get more training data from nltk corpus set
for sent in ts.strings('negative_tweets.json'):
    sent = sent.split()
    neg_dat.append((prepare_data(sent), "negative"))


for sent in ts.strings('positive_tweets.json'):
    sent = sent.split()
    pos_dat.append((prepare_data(sent), "positive"))

# training set
train_set = pos_dat + neg_dat
# make classifier
classifier = NaiveBayesClassifier.train(train_set)

# pickle to save
f = open('my_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()
