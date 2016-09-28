# -*- coding: utf-8 -*-
import oauth2
import json
CONSUMER_KEY= "8wTeesdKMnjWzWnCpngAyx7zZ"
CONSUMER_SECRET= "Yj6FVS8GiXWj17apkSsRNAgielCuoKs5rSrP9dycnVg2Fdp9Pa"

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
	consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth2.Token(key=key, secret=secret)
	client = oauth2.Client(consumer, token)
	resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
	content=content[0:(len(content))]
	tweets=json.loads(content)
	for tweet in tweets:
		print tweet['text']
	with open('tweets.json', 'w') as f:
		json.dump(tweets, f)
	return content
 
home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=narendramodi&count=1', '603487927-u1NiV4sk971JuMuBu3EzCT39nqnlnztrk6w5nTXi', 'AVDaHk0p88LjP0xahEqBiqIqofgKqeKzaBx8vrqAQQB2D' )
