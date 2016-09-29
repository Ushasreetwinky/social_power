"""Retrieving 1000 tweets."""
# -*- coding: utf-8 -*-
import oauth2
import json
import retrieve_config
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import io
import logging
import os
logging.basicConfig()
screen_name = "narendramodi"


def oauth_req(url, http_method="GET", post_body="", http_headers=None):
    """Function for Authentication."""
    consumer = oauth2.Consumer(key=retrieve_config.CONSUMER_KEY,
                               secret=retrieve_config.CONSUMER_SECRET)
    token = oauth2.Token(key=retrieve_config.ACCESS_TOKEN,
                         secret=retrieve_config.ACCESS_TOKEN_SECRET)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body,
                                   headers=http_headers)
    json_write_tweets_data(content)
    return content


def construct_url(screen_name):
    """Function to construct URL,given screen_name."""
    number_of_tweets = "1000"
    url = ('https://api.twitter.com/1.1/statuses/user_timeline.json?'
           'screen_name=' + screen_name + '&count=' + number_of_tweets)
    return url


def json_write_tweets_data(content):
    """Function to write required tweet data into Json file."""
    tweets = json.loads(content[0:len(content)])
    tweets_data = []
    for tweet in tweets:
        data = {}
        print type(tweet)
        data['text'] = tweet['text']
        data['favorite_count'] = tweet['favorite_count']
        data['retweet_count'] = tweet['retweet_count']
        data['created_at'] = tweet['created_at']
        data['id'] = tweet['id']
        data['source'] = tweet['source']
        tweets_data.append(data)
        print data
    file_name = create_newfile()
    with open(file_name, 'w') as f:
        json.dump(tweets, f)
    pass


def create_newfile():
    """Function to create new file based on time."""
    newpath = r'retrieved_tweets_' + screen_name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    date = datetime.today().strftime('%m_%d_%Y_%H_%M_%S').replace(" ", "_")
    file_name = newpath + '/' + date + ".json"
    with io.FileIO(file_name, "w") as file:
        file.write("Hello!")
    return file_name


def start_session():
    """Function to start session everyday."""
    home_timeline = oauth_req(construct_url(screen_name))
    return home_timeline

scheduler = BlockingScheduler()
scheduler.add_job(start_session, 'interval', seconds=5)
scheduler.start()
