"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""

import couchdb
from preprocess import *
from argparse import ArgumentParser
from twitter import Twitter, OAuth, TwitterHTTPError

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
     'AQWlN7Zwpm4rYWIV2krL81jYBKH1Nj0LFc6hfkYAALfC691hCR'],
    # Zeyu (David)'s Token'
    ['1644801547-Kv3f5yGWqa6x4JhP4StNX7M1MCk7iFdo47hHijm',
     'EsscWBNzIALLk5NAAT7U44OkM8kOE93VS3hms3OFqzXOW',
     'F3T6td0kAxMwKJrfCPIPJYB6B',
     '88zrERXmEoqFQvDIxHxKDqpMyBtOagA15O2OgiKSeNsnnD3aY5']
]

# database names of streaming database
dbname = ["melbourne", "sydney", "brisbane", "perth"]

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
    Havest tweets using search API and store them to database
    """
    index = args.index

    # Set up couch db
    couch = couchdb.Server("http://115.146.94.116:5984/")
    inputDB = couch[dbname[index]]
    outputDB = [
        couch["smelbourne"],
        couch["ssydney"],
        couch["sbrisbane"],
        couch["sperth"]
    ]

    # Twitter API authentication
    oauth = OAuth(
        token[index][0],
        token[index][1],
        token[index][2],
        token[index][3]
    )

    t = Twitter(auth=oauth, retry=True)

    # keep track the user ids that already been searched
    ids = set()
    for doc_id in inputDB:
        doc = inputDB[doc_id]
        # get the user id from tweet
        userID = doc["user"]["id"]
        # make tweets that has been processed as searched
        if "searched" not in doc:
            doc["searched"] = True
            inputDB.save(doc)
            # check if user id has been searched
            if userID not in ids:
                ids.add(userID)
                # make user time line request
                try:
                    result = t.statuses.user_timeline(
                        user_id=userID,
                        count=200
                    )

                    # handling results
                    for tweet in result:
                        # filter out tweets that has no location data
                        if tweet["place"] != None:
                            # store tweets into different db by location
                            if tweet["place"]["name"] == "Melbourne":
                                # preprocess (sentiment + SLA)
                                tweet = preprocess(tweet, lexicon)
                                outputDB[0].save(tweet)
                            elif tweet["place"]["name"] == "Sydney":
                                tweet = preprocess(tweet, lexicon)
                                outputDB[1].save(tweet)
                            elif tweet["place"]["name"] == "Brisbane":
                                tweet = preprocess(tweet, lexicon)
                                outputDB[2].save(tweet)
                            elif tweet["place"]["name"] == "Perth (WA)":
                                tweet = preprocess(tweet, lexicon)
                                outputDB[3].save(tweet)
                # handing unautherized error
                except TwitterHTTPError as err:
                    if err.e.code == 401:
                        print "Not authorized to access user timeline, \
                        with user id ", userID
                    else:
                        raise
        else:
            ids.add(userID)


def main():
    args = parse_args()
    # build up lexicon
    swn_lexicon = build_swn_lexicon()
    harvest(args, swn_lexicon)


if __name__ == '__main__':
    main()
