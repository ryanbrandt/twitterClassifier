from flask import Flask, render_template, request, url_for, jsonify
from forms import KeywordForm
import jinja2
import os
import classifier_app
from make_classifier import prepare_data
import pickle

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# get classifier
f = open('my_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

@app.route('/', methods=['GET', 'POST'])
def home_view():
    template = jinja_env.get_template('index.html')
    form = KeywordForm()
    tweets = []
    if request.method == 'POST':
        print('ajax received')
        keyword = request.form["keyword[value]"]
        tweets = classifier_app.fetch_tweets(keyword, tweets)
        pos = []
        neg = []
        for tweet in tweets:
            prob_dict = classifier.prob_classify(prepare_data(tweet.split()))
            counter = 0;
            for sample in prob_dict.samples():
                if counter == 0:
                    pos.append(prob_dict.prob(sample))
                    counter += 1
                else:
                    neg.append(prob_dict.prob(sample))



        return jsonify(tweets, pos, neg)

    return render_template(template, form=form, url_for=url_for('home_view'))
