import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from nltk import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from joblib import dump, load

TOP_100_PATH = '../data/popular_100_memes.csv'
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
            if j > 3000:
                break

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

X_text = [' '.join(parse_blocks(meme['boxes'])) for meme in memes_data]

plt.hist(y)
plt.show()

# implementing best results
vectorizer = TfidfVectorizer(max_df=0.5, min_df=3, ngram_range=(1,2))
# vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(X_text)
print(vectors.shape)
scaled_vectors = StandardScaler().fit_transform(vectors.toarray())

model = LogisticRegression(C=1.0,penalty='l2',solver='lbfgs', tol=0.00001)
# model = LogisticRegression()

X_train, X_test, y_train, y_test = train_test_split(scaled_vectors, y, train_size=0.8, test_size=0.2)
model = model.fit(X_train, y_train)
pred = model.predict(X_test)
print(accuracy_score(y_test, pred))

plt.hist(pred)
plt.show()

dump(vectorizer, '../prediction/meme_vectorizer.joblib')
dump(model, '../prediction/meme_predictor.joblib')