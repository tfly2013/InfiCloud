import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '724923138233012224-CtQQ4qB08Cx0ubb8wTi3Hlu5M9uoZMP'
ACCESS_SECRET = '7nyzJpJNi3ojCW63tPM7h7n7qXwExeZqcar4ZO7YpID6P'
CONSUMER_KEY = 'KYCiQNaYLBOlPRm0YIrALqgKG'
CONSUMER_SECRET = 'FXJKLs7Ft7DvcF0OAIbtScy5n5bn19tnyQpYswDkvvZkt1SUSm'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(track="Melbourne", language="en")

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 1000
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print(json.dumps(tweet))
    
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
    if tweet_count <= 0:
        break 
