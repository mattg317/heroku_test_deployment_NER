import spacy
import tweepy
import time
import pandas as pd
import os

# For testing locally
# from config import (consumer_key,
#                     consumer_secret,
#                     access_token,
#                     access_token_secret)


# For deploying to Heroku
# Get config variable from environment variables
consumer_key = os.environ.get(consumer_key)
consumer_secret = os.environ.get(consumer_secret)
access_token = os.environ.get(access_token)
access_token_secret = os.environ.get(access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Load model
nlp = spacy.load('en')


def update_twitter():

    # Create dictionary to hold text and label entities# Creat
    tweet_dict = {
        "text": [],
        "label": [],
    }

    # Get tweets from a users timeline
    user_tweets = api.user_timeline("EpcotCentre")

    # Loop through tweets
    for tweet in user_tweets:

        # Use nlp on each tweet
        doc = nlp(tweet["text"])

        # Check if nlp returns no entities
        if not doc.ents:
            print("No entities to visualize")
            print("----------------------------")
        else:
            # Print the entities for each doc
            for ent in doc.ents:
                # Store entities in dictionary
                tweet_dict["text"].append(ent.text)
                tweet_dict["label"].append(ent.label_)
    # Convert dictionary to DataFrame
    tweet_df = pd.DataFrame(tweet_dict)
    tweet_df.head()

    # Group by labels# Group
    label_frequency = tweet_df.groupby(['label']).count()

    # Get bar graph as a figure and tweet chart
    bar = label_frequency.plot.bar()
    fig = bar.get_figure()
    fig.savefig('box.png')
    api.update_with_media("box.png", "Break down of tweet labels")


# Have the Twitter bot update once a day for a week
days = 0
while days < 7:
    print("Updating Twitter")

    # Update the twitter
    update_twitter()

    # Wait a day
    time.sleep(86400)

    # Update day counter
    days += 1
