from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.stem.porter import *
from sklearn.model_selection import GridSearchCV
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import os
import pandas as pd
import numpy as np
import nltk
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

from sklearn.pipeline import Pipeline

from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns


def svc_param_selection(X, y, nfolds):
    """

    :param X:
    :param y:
    :param nfolds:
    :return:
    """
    cs = [0.001, 0.01, 0.1, 1, 2, 5, 10, 15, 20]
    gammas = [0.001, 0.01, 0.1, 1, 'auto']
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']

    param_grid = {'C': cs,
                  'gamma': gammas,
                  'kernel': kernels
                  }
    grid_search = GridSearchCV(SVC(probability=True, C=cs, shrinking=True, gamma=gammas,
                                   kernel=kernels, class_weight='balanced'),
                               param_grid,
                               cv=nfolds, iid=False, n_jobs=-1)
    # Transfor text in features
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)
    grid_search.fit(X, y)
    print('Migliori risultati:')
    print(grid_search.best_params_)
    print('Valore massimo della cross validation')
    print(np.max(grid_search.cv_results_['mean_test_score']))
    # print(grid_search.cv_results_['mean_test_score'])
    print('Massimo valore dello stimator')
    print(grid_search.best_estimator_)
    # print(grid_search.error_score)
    print(f'Risultato di Accuracy ottenuto da {nfolds} folders')
    print(grid_search.best_score_)

    return grid_search.best_params_


def cleanText(text):
    """
    A function to clean the text, remove stopwords, lemmatize and stemming,
    :param text: the text we want to clean as single sentence
    :return: the string cleaned
    """
    try:
        stop_words = set(stopwords.words('english'))
        porter = PorterStemmer()
        lemman = LancasterStemmer()
        translator = str.maketrans('', '', string.punctuation)
        text = re.sub(r'http\S+', '', text)
        text = text.translate(translator)
        return ' '.join([lemman.stem(porter.stem(w)) for w in text.split() if w not in stop_words])

    except:
        return ''


def plot_histogram(dataset, y_label, palette='Blues'):

    sns.set_context('paper')

    # create plot
    sns.countplot(x=y_label, data=dataset, palette=palette)
    plt.title('Distribuzione delle classi sul dataset originale')
    plt.show()


if __name__ == '__main__':
    # Create spam classifier
    directory_spam_bow = os.path.join('spam_data', 'spam.csv')
    bow = pd.read_csv(directory_spam_bow, encoding='latin-1')
    bow = bow[['v1', 'v2']]
    bow.columns = ['label', 'body']
    print(bow)
    print(len(bow))

    # Balance classes
    # bow = bow.groupby('label')
    # bow = bow.apply(lambda x: x.sample(bow.size().min()).reset_index(drop=True))

    # plot_histogram(bow, 'label', palette='Blues')

    x = [cleanText(text) for text in bow['body']]
    y = [label for label in bow['label']]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y,
        test_size=0.33,
        random_state=0)

    svc_param_selection(x, y, nfolds=5)
