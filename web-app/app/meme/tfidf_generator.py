from typing import Generic
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import json
import numpy as np
import random
import pandas as pd

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

# Input: text to predict meme format
# Returns: meme prediction (in text form)


def generateMemePrediction(text):
    text = text.strip().lower()
    feats = vectorizer.transform([text])
    pred = clf.predict(feats)[0]
    generateInsight(text)
    generateProbability(text)
    return selected_memes[pred]

# Input: text to predict meme format
# Returns: probability for each meme class


def generateProbability(text):
    text = text.strip().lower()
    feats = vectorizer.transform([text])
    pred = clf.predict_proba(feats)[0]

    df = pd.DataFrame(pred)
    df.to_csv('./app/csv/meme_probability.csv', index=False, header=True)


def generateProbability2(text):
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
    default = generateProbability2(text)
    probForWords = []
    for i, _ in enumerate(words):
        probs = generateProbability2(' '.join(words[:i] + words[i+1:]))
        p = np.array(default) - np.array(probs)
        probForWords.append(p.tolist())

    for i in range(len(probForWords)):
        probForWords2 = [abs(x) for x in probForWords[i]]
        maximum = max(probForWords2)
        if maximum > 0:
            probForWords[i] = [round(x/maximum, 4) for x in probForWords2]

    df = pd.DataFrame(probForWords)
    df.insert(0, -1, words)
    df.to_csv('./app/csv/meme_insights.csv', index=False, header=True)


def main():
    while True:
        print("Enter text")
        text = input()
        if text == "quit":
            break
        answer = generateProbability2(text)
        print(answer)
        #answer = generateInsight(text)


if __name__ == "__main__":
    main()
