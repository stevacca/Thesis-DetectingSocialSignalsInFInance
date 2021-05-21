#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import numpy as np
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import nltk
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
import codecs
import json

from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer

from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import roc_curve, auc

from handle_data import read_json


def readjsons(folder, query):
    """
    Read more json in one time and return the content
    :param folder: folder name
    :param query: query string name
    :return: data
    """
    files = glob.glob(os.path.join(os.getcwd(), 'reddit_data', folder, '*.json'))
    files = [f for f in files if query in f]
    data = []
    for json_file in files:
        data += (read_json(json_file))
    return data


svm_classifier = Pipeline([
        ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                         tokenizer=nltk.word_tokenize,
                                         stop_words='english',
                                         decode_error='ignore',
                                         analyzer='word',
                                         norm='l2',
                                         use_idf=True,
                                         ngram_range=(1, 2)
                                         )),
        ('clf', SVC(probability=True,
                    C=1.0833,
                    shrinking=True,
                    kernel='linear',
                    # gamma=0.001,
                    class_weight='balanced'
                    ))
])


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


def predict_spam(data, classifier, type_data):
    """
    It predict spam
    :param data: the data where to clear the spam
    :return: the ham messages dataframe
    """

    ham_messages = []
    if type_data == 'telegram':
        # print(data)
        for index, message in data.iterrows():
            pred = classifier.predict(np.array([cleanText(message['body'])]))
            if pred != 'spam':
                ham_messages.append(message)
        print('\nI messaggi HAM sono: {}\ni messaggi SPAM sono: {}'.format(len(ham_messages), len(data)-len(ham_messages)))

        return pd.DataFrame({'id': [d.id for d in ham_messages], 'body': [d.body for d in ham_messages],
                             'date': [d.date for d in ham_messages]})
    else:
        for message in data:
            pred = classifier.predict(np.array([cleanText(message['body'])]))
            if pred != 'spam':
                ham_messages.append(message)

        print('\nI messaggi HAM sono: {}\ni messaggi SPAM sono: {}'.format(len(ham_messages),
                                                                           len(data) - len(ham_messages)))

        return pd.DataFrame({'subreddit': [d['subreddit'] for d in ham_messages],
                             'body': [d['body'] for d in ham_messages],
                             'created_utc': [d['created_utc'] for d in ham_messages],
                             'author': [d['author'] for d in ham_messages]})


def define_spam_classifier(directory, classifier):
    """
    Function to build the spam classifier
    :param directory: directory where the spam csv is located
    :return: svm classifier to detect spam messages
    """
    bow = pd.read_csv(directory, encoding='latin-1')
    bow = bow[['v1', 'v2']]
    bow.columns = ['label', 'body']

    x = [text for text in bow['body'].tolist()]
    y = [label for label in bow['label'].tolist()]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y,
        test_size=0.20,
        random_state=38)

    classifier.fit(x_train, y_train)
    print('Classifier informations:')
    print(classifier.get_params())
    print()

    preds = classifier.predict(x_test)

    import scikitplot as skplt
    import matplotlib.pyplot as plt
    # plot_roc_curve(y_test, y_score, filename=None, path=None)
    y_probas = classifier.predict_proba(x_test)
    skplt.metrics.plot_roc_curve(y_test, y_probas, cmap='inferno')

    print(y_test)
    # y_test = [0 if i == 'ham' else 1 for i in y_test]
    ypsilon = classifier.decision_function(x_test)
    print(ypsilon)
    print(f'AUC score is {roc_auc_score(y_test, ypsilon)}')
    skplt.metrics.plot_confusion_matrix(y_test, preds, normalize=False, title='Confusion Matrix')

    plt.show()

    print('\n------------------------- Spam Model metrics ------------------------\n'
          'Number of training bow: {}\n Number of test bow: {}\n\nThe accuracy of the SVM model is: {}%'.format
          (len(x_train), len(x_test), accuracy_score(y_test, preds) * 100), '\n\n',
          classification_report(y_test, preds))

    return classifier


def clean_spam_telegram(names, rangedate_from, rangedate_to, spam_classifier, spammer):
    """
    Function to clean spam from telegram messages
    :param names: group names
    :param rangedate_from: from date
    :param rangedate_to: to date
    :param spam_classifier: classifier to detect spam
    :param spammer: string obj
    :return: None
    """
    for nome in names:
        data = pd.read_csv(
            os.path.join(os.getcwd(), 'telegram_data',
                         nome + '_' + rangedate_from + '_to_' + rangedate_to + '_TELEGRAM.csv'),
            sep=None, engine='python')

        data.columns = ['0', 'id', 'body', 'to_id', 'date']
        data = data.iloc[:, 1:]
        df = predict_spam(data, spam_classifier, type_data=spammer)

        df.to_csv(os.path.join(os.getcwd(), 'telegram_data', '_clean_data', nome+'_cleanedData_'
                               + rangedate_from + '_' + rangedate_to + '.csv'))
        print('File salvato correttamente nella cartella "CLEANED_DATA"')


def clean_spam_reddit(reddit_queries, spam_classifier, spammer, folder):
    """
    Function to clean spam from reddit messages
    :param reddit_queries: query names
    :param spam_classifier: classifier
    :param spammer: string obj
    :param folder: folder name str
    :return: None
    """
    for query in reddit_queries:
        data = readjsons(folder, query=query)
        # Predict spam
        df = predict_spam(data, spam_classifier, type_data=spammer)
        # save to csv

        df.to_csv(os.path.join(os.getcwd(), 'reddit_data', '_clean_data', query + '_messages_' + folder + '.csv'))
        print('File salvato correttamente nella cartella "_clean_data"')


if __name__ == '__main__':
    # Select spammer
    spammer = "reddit" # 'telegram'  # reddit

    # If reddit spam messages set folder
    reddit_folder = '20210215_GameStop'
    reddit_queries = [
        'wallstreetbets'
    ]

    # If telegram spam messages to consider
    rangedate_from, rangedate_to = '2019-09-01', '2021-08-20'
    names = [
        # 'Bad Crypto Podcast', 'The Coin Farm',
        # 'Ripple Group',
        'CoronaCoin',
        # 'Scuderia Ferrari'
        # 'WCSE RA TALKS', 'Tron Village',
        # 'Singularity net', 'AION Network'
    ]

    # Create spam classifier
    directory_spam_bow = os.path.join('spam_data', 'spam.csv')
    spam_classifier = define_spam_classifier(directory_spam_bow, svm_classifier)

    if spammer == 'telegram':
        clean_spam_telegram(names, rangedate_from, rangedate_to, spam_classifier, spammer)

    elif spammer == 'reddit':
        clean_spam_reddit(reddit_queries, spam_classifier, spammer, reddit_folder)
