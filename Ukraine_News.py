import requests
from newspaper import Article
import constants as c
import Voice_Tools3 as v
from transformers import pipeline
from datetime import datetime, timedelta

yesterday = str(datetime.now() - timedelta(days=1))[:10]

# Your existing constants
MIN_SENTENCE_LENGTH = 10
MAX_SENTENCE_LENGTH = 100

key = c.Get_NewsAPI()

def Present_Ukrainenews(mp3file, instruct):
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization")

    # Make request to NewsAPI
    url = 'https://newsapi.org/v2/everything?'

    params = {
        'q': 'ukraine',
        'from': yesterday,
        'apiKey': key
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(requests.get(url, params=params))

    articles = []
    count = 1
    Ukraine_articles = 'Today\'s Ukraine News Summary: '
    print(Ukraine_articles)
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
                Ukraine_articles += 'Article ' + str(count) + ': ' + a.title + "\n" + summary + "\n\n"
                count += 1

    print(Ukraine_articles)

    if instruct == 'silent':
        v.Play_Prompt(Ukraine_articles, mp3file, 'silent')
    else:
        v.Play_Prompt(Ukraine_articles, mp3file, 'speak')

#Present_Ukrainenews('ukraine')