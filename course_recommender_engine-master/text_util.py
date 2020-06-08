from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def clean_html_text(raw_html):
    """
    Function to clean the Description Col in Indeed Dataset
    """
    if type(raw_html)==str:
        cleantext = BeautifulSoup(raw_html, "html.parser").text
        cleantext = cleantext.replace('\r', ' ').replace('\n', ' ')[1:-1]
        return cleantext
    else:
        return None

def preprocess_text(text, remove_period=False):
    if type(text)==str:
        text = text.lower().strip()
        tokenize = nltk.word_tokenize(text)
        lemmatizer=WordNetLemmatizer()
        lemmatize_tokens = [lemmatizer.lemmatize(word) for word in tokenize]
        stop_words = stopwords.words('english')
        remove_stopwords = [w for w in lemmatize_tokens if not w in stop_words]
        if remove_period:
            remove_punctuation = [word for word in remove_stopwords if word.isalpha() or word == '.']
        else:
            remove_punctuation = [word for word in remove_stopwords if word.isalpha()]
        return remove_punctuation
    else:
        return None