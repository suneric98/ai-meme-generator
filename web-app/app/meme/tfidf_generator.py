from typing import Generic
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import json
import numpy as np
import pandas as pd
import requests

vectorizer = load('./app/meme/meme_vectorizer.joblib')
clf = load('./app/meme/meme_predictor.joblib')
selected_memes = [
    'Woman Yelling At Cat',
    'Left Exit 12 Off Ramp',
    'Surprised Pikachu',
    'Is This A Pigeon',
    'Drake Hotline Bling',
    'Blank Nut Button',
    'One Does Not Simply',
    'Change My Mind',
    'Roll Safe Think About It',
    'Leonardo Dicaprio Cheers'
]

meme_ids = [
    188390779,
    124822590,
    155067746,
    100777631,
    181913649,
    119139145,
    61579,
    129242436,
    89370399,
    5496396
]

username = 'aimemegenerator'
password = 'Memeformatter1!'
URL = 'https://api.imgflip.com/caption_image'

def imgflipRequest(id, boxes):
    params = {
        'username':username,
        'password':password,
        'template_id':id,
    }
    for i,box in enumerate(boxes):
        params['boxes[{}][text]'.format(i)] = box['text']

    print(params)
    response = requests.request('POST',URL,params=params).json()
    print(response)
    if response['success'] == True:
        return response['data']['url']
    return ''

# Input: text to predict meme format
# Returns: meme prediction (in text form)
def generateMemePrediction(text):
    text = text.strip().lower()
    feats = vectorizer.transform([text])
    pred = clf.predict(feats)[0]
    generateInsight(text)
    generateProbability(text)

    splits = text.split('|')
    boxes = [{'text':text} for text in splits]
    url = imgflipRequest(meme_ids[pred], boxes)
    return selected_memes[pred], url

# Input: text to predict meme format
# Returns: probability for each meme class
def generateProbability(text):
    text = text.strip().lower()
    feats = vectorizer.transform([text])
    pred = clf.predict_proba(feats)[0]
    return pred

# Input: text to predict meme format
# Returns: a list for each word that shows the difference between the OG
# probabilities and the probability of missing that word


def generateInsight(text):
    text = text.strip().lower()
    words = text.split()
    default = generateProbability(text)
    probForWords = []
    for i, _ in enumerate(words):
        probs = generateProbability(' '.join(words[:i] + words[i+1:]))
        probForWords.append(probs.tolist())

    allProbs = []
    for i,word in enumerate(words):
        probs = [{'group':selected_memes[i], 'value':p, 'word':'default'} for i,p in enumerate(default)]
        value = {'words':['default', word], 'text':word, 'probs':probs}
        for j,p in enumerate(probForWords[i]):
            value['probs'].append({'group':selected_memes[j], 'value':p, 'word':word})
        allProbs.append(value)
    
    with open('./app/csv/meme_insights.json', 'w') as f:
        json.dump(allProbs, f)