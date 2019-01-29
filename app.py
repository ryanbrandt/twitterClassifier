from flask import Flask, render_template, request, url_for, jsonify
from forms import KeywordForm
from collections import Counter
import jinja2
import os
import classifier_app
from make_classifier import prepare_data
import pickle
import re

application = Flask(__name__)
application.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# get classifier
f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()


@application.route('/', methods=['GET', 'POST'])
def home_view():
    template = jinja_env.get_template('index.html')
    form = KeywordForm()
    tweets = []
    # on ajax request, grab stream and analyze, pass back JSON to js
    if request.method == 'POST':
        print('ajax request received')
        keyword = request.form["keyword[value]"]
        tweets = classifier_app.fetch_tweets(keyword, tweets)
        pos = []
        neg = []
        overall = []
        for tweet in tweets:
            tweet = clean_tweet(tweet)
            tweet = list(filter(lambda x:x[0]!='@', tweet.split()))
            prob_dict = classifier.prob_classify(prepare_data(tweet))
            counter = 0;
            sum = 0;
            for sample in prob_dict.samples():
                if counter == 0:
                    sum = prob_dict.prob(sample)
                    pos.append(prob_dict.prob(sample))
                    counter += 1
                else:
                    sum -= prob_dict.prob(sample)
                    neg.append(prob_dict.prob(sample))
            if sum >= 0.5:
                overall.append('positive')
            elif sum <= -0.5:
                overall.append('negative')
            else:
                overall.append('neutral')

        count = Counter(overall)
        sum = len(overall)
        if sum == 0:
            return jsonify()
        else:
            neu_pct = count['neutral']/sum*100
            pos_pct = count['positive']/sum*100
            neg_pct = count['negative']/sum*100

            return jsonify(tweets, pos, neg, overall, neu_pct, pos_pct, neg_pct)

    return render_template(template, form=form, url_for_home=url_for('home_view'), url_for_style=url_for('static',filename='styles/main.css'))


# cleans tweet, removes invalids
def clean_tweet(tweet):
    tweet = tweet.replace('rt', '')
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)