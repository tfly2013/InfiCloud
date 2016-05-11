"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""

import couchdb
from preprocess import *
from argparse import ArgumentParser
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream


# Tokens that contains the user credentials to access Twitter API
token = [
    # Fei's token
    ['724923138233012224-CtQQ4qB08Cx0ubb8wTi3Hlu5M9uoZMP',
     '7nyzJpJNi3ojCW63tPM7h7n7qXwExeZqcar4ZO7YpID6P',
     'KYCiQNaYLBOlPRm0YIrALqgKG',
     'FXJKLs7Ft7DvcF0OAIbtScy5n5bn19tnyQpYswDkvvZkt1SUSm'],
    # Roger's token
    ['2172130051-DFJB7TToHvJSMU6iYRs62zTxXHbZTNX9Y4Y5wx3',
     '1KEsYxYYhd79hVWf8GQslU4GMkpmZLsj03M8vVIpcG4fb',
     'D8JQLo7N5v9jTr8C6tqgvRl7t',
     'UvvzGLHrGYeFGsL7AJ0QJl4p8WOkYeJE36aPwOTOZJwHvT54g2'],
    # Kimple's token
    ['1879356786-obaH7zmTg2ws0Pi6mY6JbFMErMjqKxzbBGuH9ZY',
     'pI6Wnj9CJDIscF5cVVoVe8tWJ396jITVHNOai4deWTW5l',
     'ZsIYOPOghaoCIfj4BG76S5fGw',
     'lcffivvg1gSiMkvN0dmHXuce3fcBoWeyr8qmSmokxm3aSIF3dq'],
    # Bofan's Token
    ['724926978873298946-GzUWebFMysrG5c9B0QLCKwUIS334Ff2',
     'TkQgu1VyUb9OsfYn8XJIEW3DSn9ROEqdjRdn39gCrUF39',
     'FiwgzSsEsYA9p5KjCnzr82Lhw',
     'AQWlN7Zwpm4rYWIV2krL81jYBKH1Nj0LFc6hfkYAALfC691hCR']
]

# database names of streaming database
dbname = ["melbourne", "sydney", "brisbane", "perth"]

# bounding box coordinates that used as location filter
coordinate = ["144.593742,-38.433859,145.512529,-37.511274",
              "150.520929,-34.118347,151.343021,-33.578141",
              "152.668523, -27.767441,153.31787, -26.996845",
              "115.617614, -32.675715,116.239023, -31.624486"]


def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="Twitter harvesting application using streaming api."
    )
    parser.add_argument(
        '--index',
        type=int,
        default=0,
        help='Index of virtual machine'
    )
    return parser.parse_args()


def harvest(args, lexicon):
    """
    Havest tweets using Streaming API and store them to database
    """
    index = args.index

    # Set up couch db
    couch = couchdb.Server("http://115.146.94.116:5984/")
    db = couch[dbname[index]]

    # Twitter API authentication
    oauth = OAuth(
        token[index][0],
        token[index][1],
        token[index][2],
        token[index][3]
    )

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth=oauth)

    # Get a sample of the public data following through Twitter
    iterator = twitter_stream.statuses.filter(
        locations=coordinate[index],
        language="en"
    )

    # continuously retrieving tweets
    for tweet in iterator:
        # preprocessing
        tweet = preprocess(tweet, lexicon)

        # Save tweet into database
        db.save(tweet)


def main():
    args = parse_args()
    # build up lexicon
    swn_lexicon = build_swn_lexicon()
    harvest(args, swn_lexicon)


if __name__ == '__main__':
    main()
