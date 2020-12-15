from collections import defaultdict, Counter
import numpy as np
import json
from tfidf_generator import generateInsight
from nltk import word_tokenize
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('english')
DATA_PATH = '../data/memes/'

selected_memes = [
    'Woman-Yelling-At-Cat.json', 
    'Left-Exit-12-Off-Ramp.json', 
    'Surprised-Pikachu.json',
    'Is-This-A-Pigeon.json',  
    'Drake-Hotline-Bling.json', 
    'Blank-Nut-Button.json', 
    'One-Does-Not-Simply.json',
    'Change-My-Mind.json', 
    'Roll-Safe-Think-About-It.json', 
    'Leonardo-Dicaprio-Cheers.json' 
]
def open_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

memes_data = []
y = []

for i,meme in enumerate(selected_memes):
    data = open_data(DATA_PATH + meme)
    for j, d in enumerate(data):
        if ''.join(d['boxes']).strip() != '':
            memes_data.append(d)
            y.append(i)

# functions to preprocess data into a list of words, blocks separated by |
def parse_text(text):
    text = text.lower().strip()
    return word_tokenize(text)

def parse_blocks(blocks):
    result = []
    for i,b in enumerate(blocks):
        result.extend(parse_text(b))
        if i < len(blocks) - 1:
            result.extend('|')
    return result

X_words = [parse_blocks(meme['boxes']) for meme in memes_data]


memesBestWords = []
memesWorstWords = []
for i in range(len(selected_memes)):
    memesBestWords.append(Counter())
    memesWorstWords.append(Counter())

prevMeme = -1
for i,text in enumerate(X_words):
    memeIdx = y[i]
    if memeIdx != prevMeme:
        prevMeme = memeIdx
        print('On meme {}'.format(selected_memes[memeIdx]))
    wordProbs = generateInsight(' '.join(text))
    wordProbs = [prob[memeIdx] for prob in wordProbs]

    maxImpactWord = text[np.argmax(wordProbs)]
    minImpactWord = text[np.argmin(wordProbs)]

    memesBestWords[memeIdx][maxImpactWord] += 1
    memesWorstWords[memeIdx][minImpactWord] += 1

# writing insight to file
lines = []
for i,meme in enumerate(selected_memes):
    lines.append('MEME: {}\n'.format(meme))
    lines.append('BEST WORDS\n')
    for word, count in memesBestWords[i].most_common(100):
        if word not in STOPWORDS:
            lines.append('{} | {}\n'.format(word, count))
    lines.append('WORST WORDS\n')
    for word, count in memesWorstWords[i].most_common(100):
        if word not in STOPWORDS:
            lines.append('{} | {}\n'.format(word, count))
    lines.append('---------------------------\n\n')
with open('analysis2.txt', 'w') as f:
    f.writelines(lines)