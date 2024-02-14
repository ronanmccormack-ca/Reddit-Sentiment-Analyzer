# app/views.py
from app import app, reddit
from flask import render_template, jsonify
from textblob import TextBlob
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string

# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams

# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def get_top_phrases(comments, top_n=5, ngram_size=2):
    if not comments:
        return []

    # Tokenize and clean up the words from comments
    words = []
    for comment in comments:
        tokens = nltk.word_tokenize(comment)
        # Remove punctuation and make lowercase
        tokens = [word.lower() for word in tokens if word.isalpha()]
        words.extend(tokens)

    # Remove stopwords
    filtered_words = [word for word in words if word not in stopwords.words('english')]

    # Create ngrams
    phrases = ngrams(filtered_words, ngram_size)

    # Count and get the most common phrases
    phrase_counts = Counter(phrases)
    top_phrases = phrase_counts.most_common(top_n)

    # Format phrases for returning
    formatted_phrases = [' '.join(phrase) for phrase, count in top_phrases]

    return formatted_phrases

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

    return jsonify(sentiment_counts)

@app.route('/get_top_phrases/<post_id>/<int:ngram_size>')
def get_top_phrases_route(post_id, ngram_size):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)

    comments_text = [comment.body for comment in submission.comments.list()]
    top_phrases = get_top_phrases(comments_text, top_n=5, ngram_size=ngram_size)

    return jsonify(top_phrases)
