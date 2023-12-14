import os
import requests
from newspaper import Article
import constants as c
from transformers import pipeline
from datetime import datetime, timedelta
import Voice_Tools3 as v

# Your existing constants
MIN_SENTENCE_LENGTH = 10
MAX_SENTENCE_LENGTH = 100

key = c.Get_NewsAPI()

def Present_AInews(mp3file, instruct):
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization")

    # Make request to NewsAPI
    url = 'https://newsapi.org/v2/everything?'
    # Calculate yesterday's date
    yesterday = datetime.now() - timedelta(days=2)
    yesterday_date = yesterday.strftime('%Y-%m-%d')

    params = {
        'q': 'artificial intelligence',
        'from': yesterday_date,
        'apiKey': key,
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []
    count = 1
    AIarticles = 'Today\'s AI News Summary: '

    try:
        articles = data['articles']
    except KeyError:
        print("No 'articles' key found in API response")

    for article in articles:
        if count <= 5:
            # Create Article object
            a = Article(article['url'])

            # Download and parse
            a.download()
            a.parse()

            try:
                # Use the transformers pipeline to summarize the article
                summarized = summarizer(a.text, max_length=200, min_length=50, do_sample=False)
                summary = summarized[0]['summary_text']
                arterror = False
            except Exception as e:
                print(f"Error during summarization: {e}")
                summary = "Summary could not be generated."
                arterror = True

            if arterror == False:
                print(summary)
                AIarticles += 'Article ' + str(count) + ': ' + a.title + "\n" + summary + "\n\n"
                count += 1

            print(AIarticles)

    if instruct == 'silent':
        v.Play_Prompt(AIarticles, 'ainews', 'silent')
    else:
        v.Play_Prompt(AIarticles, 'ainews', 'speak')

#Present_AInews('ainews', 'speak')
