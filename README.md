# Twitter Classifier
A pretty simple tweet classification web application I made to learn a bit more about Natural Language Processing

Uses a Naive Bayes Classifier to understand positive/negative sentiment in a given tweet

Provides users with a single webpage, where they can fetch tweets on a given desired keyword (or string of words) via an AJAX request.
 
The Users are then returned the actual stream tweets with the results of each tweet's sentiment analysis

## Main Tools ##
1) NLTK 
2) Pickle
3) Flask
4) JQuery & AJAX
5) Sentiment data from Kaggle and the NLTK Corpora Library!

I have a mini-deployment live at http://ryanbrandt.pythonanywhere.com/

Unfortunately, PythonAnywhere couldn't suppport the size of my model, so this is a reduced version is not as accurate--I intend to deploy the full version in the near future with some updates
