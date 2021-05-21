#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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
import json


def clean_text(text):
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


clf = Pipeline([
        ('feature_vect', TfidfVectorizer(strip_accents='unicode',
                                         tokenizer=nltk.word_tokenize,
                                         stop_words='english',
                                         decode_error='ignore',
                                         analyzer='word',
                                         norm='l2',
                                         ngram_range=(1, 2)
                                         )),
        ('clf', SVC(probability=True,
                    degree=3,
                    class_weight='balanced',
                    coef0=0.0,
                    verbose=False,
                    tol=0.001,
                    C=10,
                    shrinking=True,
                    kernel='linear'))
])


def balance_classes(df):
    p = []
    testo = df['Content'].tolist()
    label = df['Sentiment'].tolist()
    for i in range(0, len(testo)):
        if testo[i] is not np.nan:
            p.append((testo[i], label[i]))

    neutral = []
    positive = []
    negative = []

    random.seed(11111444)
    random.shuffle(p)
    for text, label in p:
        if label == 'Negative':
            negative.append((text, label))
        elif label == 'Neutral':
            neutral.append((text, label))
        else:
            positive.append((text, label))

    results = [len(negative), len(neutral), len(positive)]
    print('The BOW dataset is composed by: \n- {} Negative \n- {} Neutral \n- {} Positive'
          .format(results[0], results[1], results[2]))
    dataset = negative[:min(results)] + neutral[:min(results)] + positive[:min(results)]

    return dataset


def sentiment(df, clf):
    labels = []
    sentiments = []
    for index, row in df.iterrows():
        message = [clean_text(row['message'])]
        predicted = clf.predict(np.array(message))
        if predicted == 'T':
            sent = 0
        elif predicted == 'N':
            sent = -1
        else:
            sent = 1

        labels.append(predicted)
        sentiments.append(sent)

    df.insert(loc=0, column='label', value=labels)
    df.insert(loc=0, column='sent', value=sentiments)

    return df


def readjson(path, file_name):
    with open(path + file_name + '.json', 'r', encoding='utf8') as f:
        array = json.load(f)
        return array


def get_telegram_classifier(clf, folder_path):

    bow_data = pd.read_csv(folder_path, sep=None, engine='python')
    list_data = []

    bow_data.columns = ['index', 'Content', 'Sentiment']

    for index, values in bow_data.iterrows():
        list_data.append((values['Content'], values['Sentiment']))

    random.seed(1)
    list_data = set(list_data)

    bow_data = pd.DataFrame({'Content': [a for a, b in list_data], 'Sentiment': [b for a, b in list_data]})

    bow_data = balance_classes(bow_data)
    x_train = [clean_text(text) for text, label in bow_data]
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


def encode_sentiment(item):
    if item == 'P':
        return 1
    elif item == 'N':
        return -1
    else:
        return 0


def calculate_sentiment(data_frame, clf):
    """
    Calculate the sentiment
    :param data_frame: dataframe
    :param clf: clf
    :return: dataframe with sentiment
    """
    data_frame['sentiment'] = data_frame['body'].apply(lambda x: clf.predict(np.array([clean_text(x)])))
    data_frame['sentiment_code'] = data_frame['sentiment'].apply(lambda x: encode_sentiment(x))
    return data_frame


if __name__ == '__main__':
    # TODO: Set the right BOW folder
    bow_folder = 'C:\\Users\\steva\\PycharmProjects\\CreateBOW\\BOW\\Telegram_cryptoTopic_BOW.csv'
    classifier = get_telegram_classifier(clf, bow_folder)

    file_list = ['_Telegram_cleanedData_2019-09-01_2019-09-17.csv']
    for file in file_list:

        dataframe = pd.read_csv(os.path.join(os.getcwd(), 'telegram_data', '_clean_data', file))
        dataframe = dataframe.drop(dataframe.columns[0], axis=1)
        dataframe = calculate_sentiment(dataframe, classifier)
        dataframe.to_csv(os.path.join(os.getcwd(), 'sentiment_results', 'telegram_sentiment', 'sentiment_.csv'))
