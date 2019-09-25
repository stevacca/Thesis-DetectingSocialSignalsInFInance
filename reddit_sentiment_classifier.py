#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
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
import random
import datetime


def cleanText(text):
    try:
        stop_words = set(stopwords.words('english'))
        porter = PorterStemmer()
        lemman = LancasterStemmer()
        translator = str.maketrans('', '', string.punctuation)
        text = re.sub(r'http\S+', '', text)
        text = re.sub("\d+", "", text)
        text = text.translate(translator)
        return ' '.join([lemman.stem(porter.stem(w)) for w in text.split() if w not in stop_words ])

    except:
        return ''


def createDataset(dataframe):

    data = []
    for indexes, d in dataframe.iterrows():
        if d.message is not np.nan and d.message.lower() != 'I joined the helbiz airdrop'.lower():
            data.append((d.id, cleanText(d.message), d.to_id, d.date))
    data = pd.DataFrame(data)
    data.columns = ['id', 'message', 'to_id', 'date']

    return data


# TODO: Improve the classifier with a Grid search or the hyperopt
svm_classifier = Pipeline([
        ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                         tokenizer=nltk.word_tokenize,
                                         stop_words='english',
                                         decode_error='ignore',
                                         analyzer='word',
                                         norm='l2',
                                         ngram_range=(1, 2)
                                         )),
        ('clf', SVC(probability=True,
                    C=10,
                    shrinking=True,
                    kernel='linear'))
])


def balance_classes(dataframe):
    p = []

    testo = dataframe['Content'].tolist()
    label = dataframe['Sentiment'].tolist()
    for i in range(0, len(testo)):
        if testo[i] is not np.nan:
            p.append((testo[i], label[i]))

    neutral, positive, negative = [], [], []

    random.seed(1)
    random.shuffle(p)

    for text, label in p:
        if label == -1:
            negative.append((text, 'N'))
        elif label == 0:
            neutral.append((text, 'T'))
        else:
            positive.append((text, 'P'))

    results = [len(negative), len(neutral), len(positive)]
    print('The BOW dataset is composed by: \n- {} Negative \n- {} Neutral \n- {} Positive'
          .format(results[0], results[1], results[2]))
    dataset = negative[:min(results)] + neutral[:min(results)] + positive[:min(results)]

    return dataset


def encode_sentiment(item):
    if item == 'P':
        return 1
    elif item == 'N':
        return -1
    else:
        return 0


def calculate_sentiment(data_frame, classifier):
    """

    :param data_frame:
    :param classifier:
    :return:
    """
    data_frame['sentiment'] = data_frame['body'].apply(lambda x: classifier.predict(np.array([cleanText(x)])))
    data_frame['sentiment_code'] = data_frame['sentiment'].apply(lambda x: encode_sentiment(x))
    return data_frame


def readjson(path, file_name):
    """

    :param path:
    :param file_name:
    :return:
    """
    with open(path + file_name + '.json', 'r', encoding='utf8') as f:
        array = json.load(f)
        return array


def group_by_day_data(query, month):
    messages = {}

    data = (readjson('C:\\Users\\steva\\Documents\\Alkemy_DAI\\REDDIT\\CLEANED_DATA\\',
                     'Cleaned_' + query + '_nospam'+month))
    for message in data:
        t = datetime.datetime.fromtimestamp(message['created_utc']).isoformat()[:10]
        if t in messages.keys():
            messages[t].append(message['body'])
        else:
            messages[t] = [message['body']]
    return messages


def get_reddit_classifier(clf):
    bow_data = pd.read_csv(os.path.join(os.getcwd(), 'bow_data', 'reddit_bow.csv'))
    list_data = []

    for b, i in bow_data.iterrows():
        list_data.append((i['Content'], i['Sentiment']))

    random.seed(1)
    list_data = sorted(set(list_data))

    bow_data = pd.DataFrame({'Content': [a for a, b in list_data], 'Sentiment': [b for a, b in list_data]})

    bow_data = balance_classes(bow_data)
    x_train = [cleanText(text) for text, label in bow_data]
    y_train = [label for text, label in bow_data]

    x_train, x_test, y_train, y_test = train_test_split(
        x_train, y_train,
        test_size=0.33,
        random_state=15)

    clf.fit(x_train, y_train)
    predictions = clf.predict(x_test)
    print('\n------------------------- SVM MODEL ------------------------\n '
          'Number of training BOW: {}\n Number of test BOW: {}\n\nThe accuracy of the SVM model is: {}%'.format(
           len(x_train), len(x_test), accuracy_score(y_test, predictions) * 100), '\n\n',
          classification_report(y_test, predictions))

    return clf


if __name__ == '__main__':

    classifier = get_reddit_classifier(svm_classifier)

    # Choose the files to calculate the Sentiment
    file_list = ['bitcoin_2019_august_data.csv']
    for file in file_list:
        file_name_tosave = file.split('_')[0]

        dataframe = pd.read_csv(os.path.join(os.getcwd(), 'reddit_data', 'clean_data', file))
        dataframe = dataframe.drop(dataframe.columns[0], axis=1)
        dataframe = calculate_sentiment(dataframe, classifier)
        dataframe.to_csv(os.path.join(os.getcwd(), 'sentiment_results', 'reddit_sentiment', 'sentiment_'+file))
