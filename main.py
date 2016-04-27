import couchdb
from argparse import ArgumentParser
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

DB_NAME = 'demo'
KEYWORD = 'Melbourne'


def parse_args():
    """ Read arguments from command line."""
    parser = ArgumentParser(
        description="Twitter harvesting application."
    )
    parser.add_argument(
        '--keyword',
        type=str,
        default=KEYWORD,
        help='Keyword used to search for tweets.'
    )
    parser.add_argument(
        '--dbname',
        type=str,
        default=DB_NAME,
        help='Name of CouchDB database to insert data into.'
    )
    return parser.parse_args()


def preprocess(tweet):
    return tweet


def harvest(args):
    # Variables that contains the user credentials to access Twitter API
    # these following information are obtained through registering an app
    # on apps.twitter.com
    # More tutorial can be found on the following link:
    # http://socialmedia-class.org/twittertutorial.html
    ACCESS_TOKEN = '724923138233012224-CtQQ4qB08Cx0ubb8wTi3Hlu5M9uoZMP'
    ACCESS_SECRET = '7nyzJpJNi3ojCW63tPM7h7n7qXwExeZqcar4ZO7YpID6P'
    CONSUMER_KEY = 'KYCiQNaYLBOlPRm0YIrALqgKG'
    CONSUMER_SECRET = 'FXJKLs7Ft7DvcF0OAIbtScy5n5bn19tnyQpYswDkvvZkt1SUSm'

    # Set up couch db
    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[args.dbname]

    # Twitter API authentication
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)

    # Get a sample of the public data following through Twitter
    iterator = twitter_stream.statuses.filter(
        track=args.keyword,
        language="en"
    )

    tweet_count = 10
    for tweet in iterator:
        tweet_count -= 1

        # INSERT PROCESSING HERE
        tweet = preprocess(tweet)

        # Save tweet into database
        db.save(tweet)

        if tweet_count <= 0:
            break


def main():
    args = parse_args()
    harvest(args)

if __name__ == '__main__':
    main()
