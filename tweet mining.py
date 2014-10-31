"""
TWEETS MINNING

DESCRIPTION:
Python code for mining twitter and compute some statistics of the information

AUTHOR:
José Manuel Proudinat Silva
Datata
"""

# ************************************************************************
# IMPORT MODULES AND LIBRARIES
import twitter
import json
from prettytable import PrettyTable
from collections import Counter
from nltk.corpus import stopwords 
import matplotlib.pyplot as plt
import pandas as pd

# Write your keys and register for the twitter API
CONSUMER_KEY = 'Yk0GEQnjzar9wZOfhvcHmG3wW'
CONSUMER_SECRET = 'ULB1pi4nNyrMU3VAVqsRmCXGLXkP47buj7pyW7YxDR8X6W2faa'
OAUTH_TOKEN = '263216225-g2kAX3wEtRdnFINJx0vpZL4WuBV9dqUR0iKtPacE'
OAUTH_TOKEN_SECRET = 'P2w0yKsVkR14oh7Zf4ASIJGMBOX3dyGStOcNgytlXn2qj'

auth = twitter.oauth.OAuth(
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# ************************************************************************

# ************************************************************************
# GET TRENDING TOPICS

# We have to write the ID specifying where to search.
# The Yahoo! Where On Earth ID for the entire world is 1.
# See https://dev.twitter.com/docs/api/1.1/get/trends/place and
# http://developer.yahoo.com/geo/geoplanet/
# See http://woeid.rosselliot.co.nz/lookup/mexico to search WOEIDs

MX_WOE_ID = 23424900
WORLD_WOE_ID = 1
US_WOE_ID = 23424977

# Lets gonna see the trends
world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
mx_trends = twitter_api.trends.place(_id=MX_WOE_ID)

print world_trends
print
print mx_trends

# Now we're gonna print the trends but in JSON format
print json.dumps(world_trends, indent=1)
print
print json.dumps(mx_trends, indent=1)

# Computing the intersection of two sets of trends
world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
mx_trends_set = set([trend['name'] for trend in mx_trends[0]['trends']])

common_trends = world_trends_set.intersection(mx_trends_set)

print common_trends

# ************************************************************************
# COLLECTING SEARCH RESULTS

# Write the topic u want to search
q = "Ayotzinapa"

count = 100

# Search tweets
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']

# An example of JSON format for one tweet
print json.dumps(statuses[0], indent=1)

# ************************************************************************

# ************************************************************************
# Extracting text, screen names and hashtags from tweets

status_texts = [status['text']
                for status in statuses]

screen_names = [user_mention['screen_name']
                for status in statuses
                for user_mention in status['entities']['user_mentions']]

hashtags = [hashtag['text']
            for status in statuses
            for hashtag in status['entities']['hashtags']]

# Compute a collection of all words from all tweets
words = [w
         for t in status_texts
         for w in t.split()]

# Remove stopwords from words
stopWords = stopwords.words("spanish")
words = [word for word in words if word not in stopWords]

# Explore the first 5 items for each...
print json.dumps(status_texts[0:5], indent=1)
print json.dumps(screen_names[0:5], indent=1)
print json.dumps(hashtags[0:5], indent=1)
print json.dumps(words[0:5], indent=1)
# ************************************************************************

# ************************************************************************
# FREQUENCY DISTRIBUTION OF WORDS

for item in [words, screen_names, hashtags]:
    c = Counter(item)
    print c.most_common()[:10]  # top 10
    print

# Display tuples in a nice tabular format
for label, data in (('Word', words),
                    ('Screen Name', screen_names),
                    ('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    [pt.add_row(kv) for kv in c.most_common()[:10]]
    pt.align[label], pt.align['Count'] = 'l', 'r'  # Set column alignment
    print pt

# ************************************************************************

# ************************************************************************
# CALCULATING LEXICAL DIVERSITY OF TWEETS

# A function for computing lexical diversity


def lexical_diversity(tokens):
    return 1.0 * len(set(tokens)) / len(tokens)

# A function for computing the average number of words per tweet


def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0 * total_words / len(statuses)

print lexical_diversity(words)
print lexical_diversity(screen_names)
print lexical_diversity(hashtags)
print average_words(status_texts)
# ************************************************************************

# ************************************************************************
# FINDING THE MOST POPULAR RETWEETS

retweets = [
    # Store out a tuple of these three values ...
    (status['retweet_count'],
     status['retweeted_status']['user']['screen_name'],
     status['id'],
     status['text'])

    # ... for each status ...
    for status in statuses

    # ... so long as the status meets this condition.
    if status.has_key('retweeted_status')
]

# Slice off the first 5 from the sorted results and display each item in
# the tuple

pt = PrettyTable(field_names=['Count', 'Screen Name', 'id', 'Text'])
[pt.add_row(row) for row in sorted(retweets, reverse=True)[:5]]
pt.max_width['Text'] = 50
pt.align = 'l'
print pt
# ************************************************************************

# ************************************************************************
# Looking up for uses who have retweeted a status

# Write the id of the tweet
_retweets = twitter_api.statuses.retweets(id=528238159365431297)
print [r['user']['screen_name'] for r in _retweets]

# Note: this section have some problems
# ************************************************************************

# ************************************************************************
# PLOTTING FREQUENCIES OF WORDS

# Count the words
DFwords = pd.DataFrame(words)
words_counts = DFwords[0].value_counts()

# Plot frequency of the 10 most common words
plt.figure(figsize=(10,4))
words_counts[:10].plot(kind='barh', rot=0)
plt.draw()
plt.show()


# PLOTTING FREQUENCIES OF SCREEN NAMES

# Count the names
DFnames = pd.DataFrame(screen_names)
names_counts = DFnames[0].value_counts()

# Plot frequency of the 10 most users mentioned
plt.figure(figsize=(10,4))
names_counts[:10].plot(kind='barh', rot=0)
plt.draw()
plt.show()


# PLOTTING FREQUENCIES OF HASHTAGS

# Count the names
DFhtags = pd.DataFrame(hashtags)
htags_counts = DFhtags[0].value_counts()

# Plot frequency of the 10 most users mentioned
plt.figure(figsize=(10,4))
htags_counts[:10].plot(kind='barh', rot=0)
plt.draw()
plt.show()
# ************************************************************************

