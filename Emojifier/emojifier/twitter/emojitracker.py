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
from multiprocessing import Pool
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from sseclient import SSEClient

EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.UNICODE_EMOJI.values())
ID_FILE = 'best.json'
NUM_TWEETS = 1000

def get_ids():
    data = None
    with open(ID_FILE, 'r') as f:
        data = json.load(f)
    
    idToEmoji = {}
    for emoji in data:
        if emoji['char'] in EMOJIS:
            idToEmoji[emoji['id']] = emoji['char']
    return idToEmoji

def get_tweets_id(id):
    print("Getting emojis for: {}".format(idToEmoji[id]))
    start = time.time()
    URL = 'https://stream.emojitracker.com/subscribe/details/' + str(id)
    tweets = SSEClient(URL)
    results = []
    for tweet in tweets:
        tweetData = json.loads(tweet.data)
        if len(results) >= NUM_TWEETS:
            print("Finished for emoji {}. Time taken: {}".format(idToEmoji[id], time.time() - start))
            return results
        try:
            if detect(tweetData['text']) == 'en':
                results.append(tweetData['text'] + '\n')
        except LangDetectException:
            continue

idToEmoji = get_ids()
progress = 0
N = len(idToEmoji)
ids = list(idToEmoji.keys())
ids.reverse()
print("# of emojis to get tweets for: {}".format(N))

# Using multiprocessing to speed things up
pool = Pool(processes=8)
data = pool.map(get_tweets_id,ids)
data = [i for sublist in data for i in sublist]
with open('best-twitter-data.txt', 'w') as f:
    f.writelines(data)