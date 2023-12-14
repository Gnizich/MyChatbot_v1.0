import os
import time
import requests
from newspaper import Article, ArticleException
import constants as c
from transformers import pipeline
from datetime import datetime, timedelta
from random import randint
import Voice_Tools3 as v

# Constants
MIN_SENTENCE_LENGTH = 10
MAX_SENTENCE_LENGTH = 100

# Summarizer
summarizer = pipeline("summarization")

# User agents list
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
]


# Function to get articles
def get_articles(question, date):
    print(question)

    # Get random user agent
    user_agent = user_agents[randint(0, len(user_agents) - 1)]

    # Make request
    url = 'https://newsapi.org/v2/everything?'
    params = {
        'q': '"' + question + '"',
        'from': date,
        'sortBy': 'popularity',
        'apiKey': c.Get_NewsAPI(),
        'pageSize': 100,
        'page': 1
    }
    headers = {'User-Agent': user_agent}

    response = requests.get(url, params=params, headers=headers)

    # Parse response
    data = response.json()
    try:
        articles = data['articles']
    except KeyError:
        print("No 'articles' key found in API response")
        return []

    return articles


# Main function
def present_custom_news(question, mp3file, instruct):
    # Get articles
    articles = get_articles(question, datetime.strftime(datetime.now() - timedelta(days=2), '%Y-%m-%d'))

    print("ARTICLES:", articles)

    # Initialize variables
    count = 1
    custom_articles = 'Today\'s Custom News Summary: '

    # Iterate through articles
    for article in articles:

        print("ARTICLE TYPE:", type(article))

        # Check if Forbes (skip if so)
        if 'forbes.com' in article.get('url', ''):
            print(f"Skipping Forbes article: {article.get('url')}")
            continue

        # Create Article
        print(f"Downloading article: {article.get('url')}")
        a = Article(article.get('url'))
        print(a)
        try:
            # Download article
            a.download()

        except ArticleException as e:
            # Handle download errors
            print(f"Error downloading article: {e}")
            continue

            # Parse article
            a.parse()

            # Summarize article
            try:
                summarized = summarizer(a.text, max_length=200, min_length=50, do_sample=False)
                summary = summarized[0]['summary_text']

            except Exception as e:
                print(f"Error summarizing article: {e}")
                summary = "Summary could not be generated."

            # Add to summary
            custom_articles += 'Article ' + str(count) + ': ' + a.title + "\n" + summary + "\n\n"
            count += 1
            print(count)
            # Sleep for a bit
            time.sleep(randint(2, 5))

    # Print and play summary
    print(custom_articles)
    if instruct == 'silent':
        v.Play_Prompt(custom_articles, mp3file, 'silent')
    else:
        v.Play_Prompt(custom_articles, mp3file, 'speak')

# Run it
#present_custom_news('Taylor Swift news', 'custom', 'silent')