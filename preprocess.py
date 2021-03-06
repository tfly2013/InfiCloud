"""
Team: Cluster and Cloud Computing Team 3
Contents: Assigment 2
Authors: Kimple Ke, Roger Li, Fei Tang, Bofan Jin, David Ye
"""

# Preprocess Module
import nltk
import re
from location import *
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from nltk.corpus import opinion_lexicon

# download all nltk relevant stuff
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('sentiwordnet')
nltk.download('words')
nltk.download('opinion_lexicon')

# tokenize each sentence into words
word_punct_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()

# sentence segmenter
punkt_sentence_segmenter = nltk.data.load('tokenizers/punkt/english.pickle')

# English words list
words_list = set(nltk.corpus.words.words())

# get the NLTK lemmatizer
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

# manually-annotated positive set
opinion_positive_words = opinion_lexicon.positive()
opinion_positive_words = [word for word in opinion_positive_words]

# manually-annotated negative set
opinion_negative_words = opinion_lexicon.negative()
opinion_negative_words = [word for word in opinion_negative_words]


def lemmatize(word):
    """
    Lemmatization
    """

    return lemmatizer.lemmatize(word)


def maxmatch(sentence, dictionary):
    """
    MaxMatch algorithm
    """

    sent_len = len(sentence)
    if sent_len == 0:
        return []

    for i in range(sent_len, 0, -1):
        firstword = sentence[:i]
        lemmatized_firstword = lemmatize(firstword)
        remainder = sentence[i:]
        if lemmatized_firstword in dictionary:
            result = [firstword] + maxmatch(remainder, dictionary)
            return result

    firstword = sentence[0]
    remainder = sentence[1:]
    result = [firstword] + maxmatch(remainder, dictionary)
    return result


def build_swn_lexicon():
    """
    Construct positive and negative lexicons
    """

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
        # For each lemma, take the most common polarity
        # if there are more than 1
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

    # combine sentiwordnet lexicons with opinion lexicons
    positive_words_swn = positive_words_swn + opinion_positive_words
    negative_words_swn = negative_words_swn + opinion_negative_words

    positive_words_swn = set(positive_words_swn)
    negative_words_swn = set(negative_words_swn)

    return [positive_words_swn, negative_words_swn]


def get_polarity_type(synset_name):
    """
    Gets the polarity from SentiWordNet
    """

    swn_synset = swn.senti_synset(synset_name)
    if not swn_synset:
        return None
    elif swn_synset.pos_score() > swn_synset.neg_score() \
            and swn_synset.pos_score() > swn_synset.obj_score():
        return 1
    elif swn_synset.neg_score() > swn_synset.pos_score() \
            and swn_synset.neg_score() > swn_synset.obj_score():
        return -1
    else:
        return 0


def classify(tweet, lexicon):
    """
    For a given tweet, classify it as negative (-1), neutral (0) or
    positive (1) using a given lexicon
    The lexicon is given as a list of two sets, with the first set
    containing positive words and the second set containing negative words
    """

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
    """
    Preprocessing will exclude tweeter name, URL and hashtags and add
    hashtags back as tokenized sentence
    """

    tweet_text = tweet["text"]

    # Use regex to remove twitter usernames
    tweet_text = re.sub(
        r"@\w+",
        "",
        tweet_text
    )

    # Use regex to remove URLs
    tweet_text = re.sub(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+",
        "",
        tweet_text
    )

    # find all hashtags in the tweet
    hashtag_pattern = re.compile(r"#\w+")
    hashtag_list = hashtag_pattern.findall(tweet_text)

    # Remove hashtags from tweet
    tweet_text = re.sub(r"#\w+", "", tweet_text)

    # Make everything lowercase, then segment with NLTK punkt
    # sentence segmenter
    tweet_text = punkt_sentence_segmenter.tokenize(tweet_text.lower())

    # Tokenize sentences with NLTK regex WordPunct tokenizer
    processed_tweet = []

    for sentence in tweet_text:
        processed_tweet.append(word_punct_tokenizer.tokenize(sentence))

    for hashtag in hashtag_list:
        sent_list = []
        sentence = hashtag[1:]
        toeknized_sent = maxmatch(sentence, words_list)
        for t in toeknized_sent:
            sent_list.append(t)
        processed_tweet.append(sent_list)

    tweet['sentiment'] = classify(processed_tweet, lexicon)

    # add sla to tweets
    if tweet['coordinates'] != None:
        lng = tweet["coordinates"]["coordinates"][0]
        lat = tweet["coordinates"]["coordinates"][1]
        tweet["sla"] = find_sla(lng, lat)

    return tweet
