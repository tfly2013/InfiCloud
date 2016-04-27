import json
import couchdb
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '724926978873298946-GzUWebFMysrG5c9B0QLCKwUIS334Ff2'
ACCESS_SECRET = 'TkQgu1VyUb9OsfYn8XJIEW3DSn9ROEqdjRdn39gCrUF39'
CONSUMER_KEY = 'FiwgzSsEsYA9p5KjCnzr82Lhw'
CONSUMER_SECRET = 'AQWlN7Zwpm4rYWIV2krL81jYBKH1Nj0LFc6hfkYAALfC691hCR'

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


couch = couchdb.Server('http://http://115.146.94.116:5984/')
db = couch['tweets'] # existing