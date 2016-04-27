import couchdb
import nltk
import re
from argparse import ArgumentParser
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from nltk.tokenize import WordPunctTokenizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('sentiwordnet')
word_punct_tokenizer = WordPunctTokenizer()
punkt_sentence_segmenter = nltk.data.load('tokenizers/punkt/english.pickle')
DB_NAME = 'demo'
KEYWORD = 'Melbourne'

def parse_args():
    """ Read arguments from command line."""
    parser = ArgumentParser(description="Twitter harvesting application.")
    parser.add_argument('--keyword', type=str, default=KEYWORD, help=\
    'Keyword used to search for tweets.')
    parser.add_argument('--dbname', type=str, default=DB_NAME, help=\
    'Name of CouchDB database to insert data into.')
    return parser.parse_args()

def build_swn_lexicon():
    positive_words_swn = []
    negative_words_swn = []

    polarities = {}
    for synset in wn.all_synsets():
        # Get polarities for each lemma
        polarity = get_polarity_type(synset.name())
        if synset.lemmas()[0].name() in polarities:
            polarities[synset.lemmas()[0].name()].append(polarity)
        else:
            polarities[synset.lemmas()[0].name()] = [polarity]

    # Create lists of positive and negative words
    for name, polarity in polarities.items():
        # For each lemma, take the most common polarity if there are more than 1
        if len(polarity) > 1:
            word_polarity = max(set(polarity), key=polarity.count)
            polarities[name] = [word_polarity]
            if word_polarity == 1:
                positive_words_swn.append(name)
            elif word_polarity == -1:
                negative_words_swn.append(name)
        else:
            if polarity == 1:
                positive_words_swn.append(name)
            elif polarity == -1:
                negative_words_swn.append(name)
    
    positive_words_swn = set(positive_words_swn)
    negative_words_swn = set(negative_words_swn)

    return [positive_words_swn, negative_words_swn]

    # Gets the polarity from SentiWordNet
def get_polarity_type(synset_name):
    swn_synset =  swn.senti_synset(synset_name)
    if not swn_synset:
        return None
    elif swn_synset.pos_score() > swn_synset.neg_score() and swn_synset.pos_score() > swn_synset.obj_score():
        return 1
    elif swn_synset.neg_score() > swn_synset.pos_score() and swn_synset.neg_score() > swn_synset.obj_score():
        return -1
    else:
        return 0

# For a given tweet, classify it as negative (-1), neutral (0) or positive (1) using a given lexicon
# The lexicon is given as a list of two sets, with the first set containing positive words and the second set
# containing negative words
def classify(tweet, lexicon):
    score = 0
    for sentence in tweet:
        for word in sentence:
            if word.lower() in lexicon[0]:
                score += 1
            if word.lower() in lexicon[1]:
                score -= 1
    if score <= -1:
        return -1
    elif score >= 1:
        return 1
    else:
        return 0

def preprocess(tweet, lexicon):
    # Use regex to remove twitter usernames
    tweet = re.sub(r"@\w+", "", tweet)
    
    # Use regex to remove URLs
    tweet = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+", "", tweet)

    # Remove hashtags from tweet
    tweet = re.sub(r"#\w+", "", tweet)

    # Make everything lowercase, then segment with NLTK punkt sentence segmenter
    tweet = punkt_sentence_segmenter.tokenize(tweet.lower())

    #Tokenize sentences with NLTK regex WordPunct tokenizer
    processed_tweet = []

    for sentence in tweet:
        processed_tweet.append(word_punct_tokenizer.tokenize(sentence))
        
    processed_tweet['sentiment'] = classify(processed_tweet, lexicon)
        
    return processed_tweet

def harvest(args, lexicon):
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
    iterator = twitter_stream.statuses.filter(track=args.keyword, language="en")

    tweet_count = 1
    for tweet in iterator:
        tweet_count -= 1
    
        # INSERT PROCESSING HERE
        tweet = preprocess(tweet, lexicon)
    
        # Save tweet into database
        db.save(tweet)
        
        if tweet_count <= 0:
            break
    
def main():
    args = parse_args()
    swn_lexicon = build_swn_lexicon()
    harvest(args, swn_lexicon)
    
if __name__ == '__main__':
    main()
