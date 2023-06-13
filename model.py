# libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import ast
import pickle

# spacy
import string
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

# sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

# warnings
import warnings

warnings.filterwarnings('ignore')

# Read the Dataset
df = pd.read_csv("data/movies_metadata.csv")
df = df[['overview', 'genres']]

# Convert from object genres into the list
df['genres'] = df['genres'].apply(ast.literal_eval)

# Drop the null values where `overview` is null
df = df.dropna(subset=['overview'])

# Remove the columns where the genres list is empty
df = df[df['genres'].map(lambda d: len(d)) > 0]

df.reset_index(drop=True, inplace=True)

# Create our list of punctuation marks
punctuations = string.punctuation

# Using Spacy to Preprocess Text Data¶
# Create our list of stopwords
nlp = spacy.load('en_core_web_sm')
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# Load English tokenizer, tagger, parser, NER and word vectors
parser = English()


#  Tokenizer function
def spacy_tokenizer(sentence):
    """Function for preprocessing steps to create the tokens
    """

    # Create token object, which is used to create documents with linguistic annotations.
    # Beautifying the text of HTML and XML data 
    review_soup = BeautifulSoup(sentence)

    # Get the text and remove the tags
    review_text = review_soup.get_text()

    # Remove the letters anf punctations
    review_letters_only = re.sub("[^a-zA-Z]", " ", review_text)

    # Convert to lower case
    review_lower_case = review_letters_only.lower()

    # Splits into words
    review_words = review_lower_case.split()

    # Remove stopwords
    meaningful_words = [word for word in review_words if word not in stop_words]

    return ' '.join(meaningful_words)


df['overview_new'] = df.overview.apply(spacy_tokenizer)

df['genre_new'] = df['genres'].apply(lambda x: [v for dic in x for k, v in dic.items() if 'name' in k])

# MultiLabelBinarizer for Genres
# initialize MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# transform the genre_new column to a series of columns with binary values
binary_labels = pd.DataFrame(mlb.fit_transform(df['genre_new']), columns=mlb.classes_)

# order columns alphabetically
binary_labels = binary_labels.sort_index(axis=1)

# split dataset into training and validation set using 80% and 20% Rule
X_train, X_val, y_train, y_val = train_test_split(movies['overview_new'],
                                                  binary_labels,
                                                  test_size=0.2,
                                                  random_state=9)

# create TF-IDF features
# TF-IDF = Term frequency - inverse document frequency
# Used to predict how important a word is for a document
# https://en.wikipedia.org/wiki/Tf%E2%80%93idfs
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_val_tfidf = tfidf_vectorizer.transform(X_val)

# Model Training
# Best Class Classifier : Logistic Regression to be used to training and testing the data

classifier = OneVsRestClassifier(LogisticRegression(penalty='l2',
                                                    solver='sag',
                                                    C=1.0,
                                                    random_state=33))

classifier.fit(X_train_tfidf, y_train)

# save the model
pickle.dump(classifier, open('model/log_model.pkl', 'wb'))

# save the MulatiLabelBinarizer
pickle.dump(mlb, open('model/mlb.pkl', 'wb'))

# save the vectorzier
pickle.dump(tfidf_vectorizer, open('model/tfidf_vectorizer.pkl', 'wb'))
