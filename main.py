import couchdb
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

DB_NAME = 'demo'
KEYWORD = 'Melbourne'

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '724923138233012224-CtQQ4qB08Cx0ubb8wTi3Hlu5M9uoZMP'
ACCESS_SECRET = '7nyzJpJNi3ojCW63tPM7h7n7qXwExeZqcar4ZO7YpID6P'
CONSUMER_KEY = 'KYCiQNaYLBOlPRm0YIrALqgKG'
CONSUMER_SECRET = 'FXJKLs7Ft7DvcF0OAIbtScy5n5bn19tnyQpYswDkvvZkt1SUSm'

# Set up couch db
couch = couchdb.Server("http://115.146.94.116:5984/")
db = couch[DB_NAME]

# Twitter API authentication
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(track= KEYWORD, language="en")

tweet_count = 10
for tweet in iterator:
    tweet_count -= 1

    # INSERT PROCESSING HERE

    # Save tweet into database
    db.save(tweet)
    
    if tweet_count <= 0:
        break
    
