# app/views.py
from app import app, reddit
from flask import render_template, jsonify
from textblob import TextBlob
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string

nltk.download('punkt')
nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer

def get_top_tfidf_words(comments, top_n=5):
    if not comments:
        return []

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(comments)
    sum_words = tfidf_matrix.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in tfidf_vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:top_n]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_subreddits')
def get_subreddits():
    subreddits = []
    for subreddit in reddit.subreddits.popular(limit=20):
        subreddits.append(subreddit.display_name)
    return jsonify(subreddits)

@app.route('/get_posts/<subreddit>')
def get_posts(subreddit):
    posts = []
    for post in reddit.subreddit(subreddit).hot(limit=15):
        posts.append({
            'title': post.title,
            'id': post.id,
            'url': post.url
        })
    return jsonify(posts)

@app.route('/get_comments/<post_id>')
def get_comments(post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)

    # Collect all comments for TF-IDF analysis
    comments_text = [comment.body for comment in submission.comments.list()]
    # Perform TF-IDF analysis to get top words
    tfidf_top_words = get_top_tfidf_words(comments_text, top_n=5)

    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}

    # Perform sentiment analysis
    for comment in submission.comments.list():
        analysis = TextBlob(comment.body)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            sentiment_counts['positive'] += 1
        elif sentiment == 0:
            sentiment_counts['neutral'] += 1
        else:
            sentiment_counts['negative'] += 1

    return jsonify({'tfidf_top_words': tfidf_top_words, 'sentiment_counts': sentiment_counts})
