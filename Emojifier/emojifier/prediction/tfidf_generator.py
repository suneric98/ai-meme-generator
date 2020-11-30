from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import json
import random

vectorizer = load('emoji_vectorizer.joblib')
clf = load('emoji_predictor.joblib')
PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
SELECTED_EMOJIS_PATH = '../data/best-emojis.json'
with open(SELECTED_EMOJIS_PATH, 'r') as f:
    EMOJIS = json.load(f)
EMOJI_CHARS = [e['char'] for e in EMOJIS]

def makeGroups(lst, n):
    groups = []
    for i in range(0, len(lst), n):
        groups.append(lst[i:i+n])
    return groups



def generateEmojipasta(text):
    tokens = text.split()
    groups = makeGroups(tokens, random.randint(2, 4))
    finalText = []
    for group in groups:
        group = " ".join(group)
        clean = "".join([l for l in group if l not in PUNC])
        clean = clean.lower()
        feats = vectorizer.transform([clean])
        pred = clf.predict(feats)[0]
        finalText.append(group)
        finalText.append(EMOJI_CHARS[pred])
    return " ".join(finalText)

def main():
    while True:
        print("Enter text")
        text = input()
        if text == "quit":
            break
        answer = generateEmojipasta(text)
        print(answer)

if __name__ == "__main__":
    main()
