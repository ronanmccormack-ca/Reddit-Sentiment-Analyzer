# app/__init__.py
from flask import Flask
import praw

app = Flask(__name__)

reddit = praw.Reddit(
    client_id='eJLRIJM0oRMPbp9rQE6DEA',
    client_secret='fj6fZkTHo5X2m5ybabPSXqCLV66gdg',
    user_agent='sentiment'
)

from app import views