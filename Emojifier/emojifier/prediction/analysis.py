from collections import defaultdict, Counter
import numpy as np
import emoji
import json
from parsing import Tokenizer, TokenType
from tfidf_generator import getProbabilities
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('english')

# getting the twitter comments
DATA_PATH = '../data/twitter-data-cleaned.txt'
with open(DATA_PATH, 'r',  encoding="utf-8") as f:
    data = f.readlines()
data = [d.strip() for d in data if d.strip() != '']

# getting our chosen emojis
SELECTED_EMOJIS_PATH = '../data/best-emojis.json'
with open(SELECTED_EMOJIS_PATH, 'r') as f:
    EMOJIS = json.load(f)
EMOJI_CHARS = [e['char'] for e in EMOJIS]

ALL_EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.UNICODE_EMOJI.values())

# preprocessing the data

tokenizer = Tokenizer(EMOJI_CHARS)
# take 3 previous words as context for the emoji
context = {e:[] for e in EMOJI_CHARS}
emojiToId = {e:i for i,e in enumerate(EMOJI_CHARS)}

for tweet in data:
    tokens = tokenizer.tokenize(tweet)
    for i,token in enumerate(tokens):
        if token.token_type == TokenType.EMOJIS:
            closest = tokenizer.findClosestNWords(5, tokens, i)
            if closest:
                context[token.raw].append(closest)

emojiBestWords = []
emojiWorstWords = []
for i in range(len(EMOJI_CHARS)):
    emojiBestWords.append(Counter())
    emojiWorstWords.append(Counter())
    
for e, tweets in context.items():
    print('On emoji {}'.format(e))
    emojiId = emojiToId[e]
    for tweet in tweets:
        default = getProbabilities(tweet)
        wordProbs = []
        for wordIdx in range(len(tweet)): #getting probability for each word
            probs = getProbabilities(tweet[:wordIdx] + tweet[wordIdx+1:])
            p = default[emojiId] - probs[emojiId]
            wordProbs.append(p)

        maxImpactWord = tweet[np.argmax(wordProbs)]
        minImpactWord = tweet[np.argmin(wordProbs)]

        emojiBestWords[emojiId][maxImpactWord] += 1
        emojiWorstWords[emojiId][minImpactWord] += 1

# writing insight to file
lines = []
for i,e in enumerate(EMOJI_CHARS):
    lines.append('EMOJI: {}\n'.format(e))
    lines.append('BEST WORDS\n')
    for word, count in emojiBestWords[i].most_common(100):
        if word not in STOPWORDS:
            lines.append('{} | {}\n'.format(word, count))
    lines.append('WORST WORDS\n')
    for word, count in emojiWorstWords[i].most_common(100):
        if word not in STOPWORDS:
            lines.append('{} | {}\n'.format(word, count))
    lines.append('---------------------------\n\n')
with open('analysis.txt', 'w') as f:
    f.writelines(lines)