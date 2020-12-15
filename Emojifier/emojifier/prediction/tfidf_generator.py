from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import json
import numpy as np
import random

vectorizer = load('emoji_vectorizer.joblib')
clf = load('emoji_predictor.joblib')
PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
SELECTED_EMOJIS_PATH = '../data/best-emojis.json'
with open(SELECTED_EMOJIS_PATH, 'r') as f:
    EMOJIS = json.load(f)
EMOJI_CHARS = [e['char'] for e in EMOJIS]

# helper function to convert list of words to groups of words
def makeGroups(lst, n):
    groups = []
    for i in range(0, len(lst), n):
        groups.append(lst[i:i+n])
    return groups

# takes in a list of groups of words
# returns a list of emojis, one emoji for each group
def generateEmojis(groups):
    emojisToAdd = []
    for group in groups:
        group = " ".join(group)
        clean = "".join([l for l in group if l not in PUNC])
        clean = clean.lower()
        feats = vectorizer.transform([clean])
        pred = clf.predict(feats)[0]
        emojisToAdd.append(EMOJI_CHARS[pred])
    return emojisToAdd

# given a test, splits the text into groups and creates emojis for each group
# returns a string that is the same as the original text but with emojis added
def generateEmojipasta(text):
    tokens = text.strip().split()
    groups = makeGroups(tokens, random.randint(2, 4))
    finalText = []
    emojisToAdd = generateEmojis(groups)
    for i,emoji in enumerate(emojisToAdd):
        finalText.extend(groups[i])
        finalText.append(emoji)
    return " ".join(finalText)

# given a group, returns the probabilities for each emoji for that group
def getProbabilities(group):
    group = " ".join(group)
    clean = "".join([l for l in group if l not in PUNC])
    clean = clean.lower()
    feats = vectorizer.transform([clean])
    pred = clf.predict_proba(feats)[0]
    return pred

# for each word, returns the 'insight' of that word: the difference of the
# original probabilities for each emoji and with that word missing
def generateInsight(text):
    tokens = text.strip().split()
    groups = makeGroups(tokens, random.randint(2, 4))
    default = [getProbabilities(group) for group in groups]
    probForWords = []
    for i,group in enumerate(groups): # calculating prob when removing a word
        for word_idx,_ in enumerate(group):
            probs = getProbabilities(group[:word_idx] +  group[word_idx+1:])
            p = np.array(default[i]) - np.array(probs)
            probForWords.append(p.tolist())
    return probForWords

def main():
    while True:
        print("Enter text")
        text = input()
        if text == "quit":
            break
        answer = generateEmojipasta(text)
        # generateInsight(text)
        print(answer)

if __name__ == "__main__":
    main()
