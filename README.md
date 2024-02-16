# Reddit Sentiment Analyzer

## Description

Reddit Sentiment Analyzer is a web application designed to analyze and visualize the sentiment of comments on Reddit posts. This application allows users to select a subreddit, view recent posts, and analyze the sentiments of comments for each post, categorizing them as positive, neutral, or negative. It also highlights the most frequently used words in the comments.

## Features

- **Subreddit Selection**: Choose from popular subreddits or search for specific ones.
- **Post Browsing**: View a list of recent posts from the selected subreddit.
- **Sentiment Analysis**: Analyze and categorize comments into positive, neutral, or negative sentiments.
- **Keyword Extraction**: Identify and display the top keywords from the comments.

## Technologies Used

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript (jQuery)
- Sentiment Analysis: TextBlob
- Reddit API: PRAW (Python Reddit API Wrapper)
- Deployment: [Deployed Platform - e.g., Render, Heroku]

## Setup and Installation

1. Clone the Repository:
    ```bash
    git clone [repository-url]
    ```
2. Create and Activate a Virtual Environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Unix or MacOS
    venv\Scripts\activate     # On Windows
    ```
3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set Up Environment Variables:
    - Rename `.env.example` to `.env`.
    - Fill in your Reddit API credentials and other necessary settings.
5. Run the Application:
    ```bash
    flask run
    ```

## Usage

1. Open the application in your web browser.
2. Select a subreddit from the dropdown menu.
3. Browse through the list of posts and select one to view its comments.
4. The application will display sentiment analysis results and the top keywords for the comments.

## Contributing

Contributions to the Reddit Sentiment Analyzer are welcome! Please read our Contributing Guidelines for more information.

## License

This project is licensed under the MIT License.

