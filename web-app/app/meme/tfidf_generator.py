from typing import Generic
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import json
import numpy as np
import random

vectorizer = load('meme_vectorizer.joblib')
clf = load('meme_predictor.joblib')
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

# Input: text to predict meme format
# Returns: meme prediction (in text form)
def generateMemePrediction(text):
    text = text.strip().lower()
    feats = vectorizer.transform([text])
    pred = clf.predict(feats)[0]
    return selected_memes[pred]

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
    for i,_ in enumerate(words):
        probs = generateProbability(' '.join(words[:i] + words[i+1:]))
        p = np.array(default) - np.array(probs)
        probForWords.append(p.tolist())
    return probForWords

def main():
    while True:
        print("Enter text")
        text = input()
        if text == "quit":
            break
        answer = generateMemePrediction(text)
        print(answer)
        answer = generateInsight(text)

if __name__ == "__main__":
    main()
