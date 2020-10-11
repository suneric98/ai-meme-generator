"""
Code for stuff related to emojitracker

get_ids
Using the file obtained from the emojitracker API, gets the ids and char emoji
for each emoji it tracks

get_tweets_id
Using the emojitracker streaming api, gets tweets for a specific id and then
returns a list of those tweets
"""

import json
import emoji
import time
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from sseclient import SSEClient

EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.UNICODE_EMOJI.values())
NUM_TWEETS = 100

def get_ids():
    ID_FILE = 'emojitracker_rankings.json'
    data = None
    with open(ID_FILE, 'r') as f:
        data = json.load(f)
    
    idToEmoji = {}
    for emoji in data:
        if emoji['char'] in EMOJIS:
            idToEmoji[emoji['id']] = emoji['char']
    return idToEmoji

def get_tweets_id(id):
    URL = 'https://stream.emojitracker.com/subscribe/details/' + str(id)
    tweets = SSEClient(URL)
    results = []
    for tweet in tweets:
        tweetData = json.loads(tweet.data)
        if len(results) >= NUM_TWEETS:
            return results
        try:
            if detect(tweetData['text']) == 'en':
                results.append(tweetData['text'] + '\n')
        except LangDetectException:
            continue

# def get_tweets(idToEmoji):
#     tweets = SSEClient('https://stream.emojitracker.com/subscribe/eps')
#     for tweet in tweets:
#         print(tweet)

idToEmoji = get_ids()
progress = 0
for id in idToEmoji:
    print("Getting tweets for: {}".format(idToEmoji[id]))
    start = time.time()
    tweets = get_tweets_id(id)
    print("Finished. Time taken: {}".format(time.time() - start))
    progress += 1
    print("# of emojis left: {}".format(len(idToEmoji) - progress))

    # write to file
    with open('twitter-data.txt', 'a+') as f:
        for t in tweets:
            f.write(t)