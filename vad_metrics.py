import csv
import pandas as pd
from nltk.corpus import stopwords
from datetime import datetime

import numpy as np
import string
import re
import os


''' This script allows to measure the VAD metrics:
Valence --> from unhappy too happy
Arousal --> from calm to excited
Dominance --> from controlled to in control
'''


def clean_text(text):
    try:
        stop_words = set(stopwords.words('english'))
        translator = str.maketrans('', '', string.punctuation)
        text = re.sub(r'http\S+', '', text.lower()) #delete unuseful chars
        text = re.sub("\d+", "", text) #delete digits
        text = text.translate(translator)
        return [w for w in text.split() if w not in stop_words]
    except:
        return ''


# Calculate VAD measure
def calulate_VAD(new_sentence, metrics):

    sentence = clean_text(new_sentence)  # clean the text from punctuations, stopwords and digits
    results = []
    for s_word in sentence:
        if s_word in metrics.word.tolist():
            # print(f'The word {word} is into the VAD metrics')
            row_values = metrics[metrics['word'].isin([s_word])].values.tolist()
            results += row_values

    valences, arousals, dominances = [], [], []
    for word, valence, arousal, dominance in results:
        valences.append(float(valence))
        arousals.append(float(arousal))
        dominances.append(float(dominance))

    if len(results) == 0:
        vad_valence, vad_arousal, vad_dominance = None, None, None
    elif len(results) > 1:

        # calcolo il massimo, il minimo e la media delle valenze in lista
        mean_valence = np.mean(valences).astype(np.float)
        max_valence, min_valence = max(valences), min(valences)

        # VAD Equation
        # VALENCE
        vad_valence = 0
        if (mean_valence > min_valence) and (mean_valence < max_valence):
            vad_valence = round(max_valence - min_valence, 2)
        elif mean_valence > max_valence:
            vad_valence = mean_valence - min_valence
        elif min_valence > mean_valence:
            vad_valence = max_valence - mean_valence

        # calcolo il massimo, il minimo e la media delle valenze in lista
        mean_arousal = np.mean(arousals).astype(np.float)
        max_arousal, min_arousal = max(arousals), min(arousals)
        # AROUSAL
        # VAD Equation
        vad_arousal = 0
        if (mean_arousal > min_arousal) and (mean_arousal < max_arousal):
            vad_arousal = round(max_arousal - min_arousal, 2)
        elif mean_arousal > max_arousal:
            vad_arousal = mean_arousal - min_arousal
        elif min_arousal > mean_arousal:
            vad_arousal = max_arousal - mean_arousal

        # calcolo il massimo, il minimo e la media delle valenze in lista
        mean_dominance = np.mean(dominances).astype(np.float)
        max_dominance, min_dominance = max(dominances), min(dominances)
        # AROUSAL
        # VAD Equation
        vad_dominance = 0
        if (mean_dominance > min_dominance) and (mean_dominance < max_dominance):
            vad_dominance = round(max_dominance - min_dominance, 2)
        elif mean_dominance > max_dominance:
            vad_arousal = mean_arousal - min_arousal
        elif min_dominance > mean_dominance:
            vad_dominance = max_dominance - mean_dominance
    else:
        vad_valence, vad_arousal, vad_dominance = valences[0], arousals[0], dominances[0]

    print(f'The valence is {str(vad_valence)}, the arousal is {str(vad_arousal)},'
          f' while the dominance is {str(vad_dominance)}')
    return [new_sentence, vad_valence, vad_arousal, vad_dominance]


# Take sentences and return a pandas dataframe
def vad_dataset(vads, dataframe, text_col, date_col):
    results_all = []
    for index, values in dataframe.iterrows():
        vad_result = calulate_VAD(values[text_col], vads)
        results_all.append((values[text_col], vad_result, values[date_col]))

    data_frame = pd.DataFrame({'sentence': [s[0] for s in results_all],
                               'valence': [s[1][1] for s in results_all],
                               'arousal': [s[1][2] for s in results_all],
                               'dominance': [s[1][3] for s in results_all],
                               'date': [s[2] for s in results_all]})
    data_frame['date'] = data_frame.date.apply(lambda x: from_unix_to_datestamp_date(x))
    data_frame = data_frame.dropna()

    return data_frame


# correct if the population S.D. is expected to be equal for the two groups.

def cohen_d(x, y):
    from statistics import mean, stdev
    from math import sqrt

    # test conditions
    c0 = [2, 4, 7, 3, 7, 35, 8, 9]
    c1 = [i * 2 for i in c0]

    cohens_d = (mean(c0) - mean(c1)) / (sqrt((stdev(c0) ** 2 + stdev(c1) ** 2) / 2))

    print(cohens_d)


def cohen_d111(x, y, metrics):
    sentence_x = clean_text(x)  # clean the text from punctuations, stopwords and digits
    sentence_y = clean_text(y)
    results_x, results_y = [], []
    valences, arousals, dominances = [], [], []
    for word in sentence_x:
        if word in metrics.word.tolist():
            # print(f'The word {word} is into the VAD metrics')
            row_values = df[df['word'].isin([word])].values.tolist()
            results_x += row_values

    for word in sentence_y:
        if word in metrics.word.tolist():
            # print(f'The word {word} is into the VAD metrics')
            row_values = df[df['word'].isin([word])].values.tolist()
            results_y += row_values

    from statistics import mean, stdev
    from math import sqrt

    # test conditions
    c0 = [2, 4, 7, 3, 7, 35, 8, 9]
    c1 = [i * 2 for i in c0]

    cohens_d = (mean(c0) - mean(c1)) / (sqrt((stdev(c0) ** 2 + stdev(c1) ** 2) / 2))

    print(cohens_d)


def vad_metrics():
    """
    Function to load the txt file where vad metrics values are
    :return: vad metrics dataframe
    """
    results = []
    with open(os.path.join(os.getcwd(), 'vad_metrics_folder', 'VAD_values.txt'), newline='') as inputfile:
        for row in csv.reader(inputfile):
            results.append(row)

    data_frame = pd.DataFrame({'word': [r[0] for r in results],
                               'valence': [r[1] for r in results],
                               'arousal': [r[2] for r in results],
                               'dominance': [r[3] for r in results]})
    return data_frame


def from_unix_to_datestamp_date(datestamp):
    """
    Change the format of the date from datestamp to unix
    :param datestamp: the datestamp format
    :return: the date in unix codification
    """
    datestamp = datetime.utcfromtimestamp(datestamp).strftime('%Y-%m-%d %H:%M:%S')

    return datestamp


if __name__ == '__main__':
    # Import file to calculate VAD
    file_name = 'Libra&Facebook_messages_libra_folder.csv'
    file_folder = os.path.join(os.getcwd(), 'reddit_data', 'clean_data', file_name)
    df = pd.read_csv(file_folder)

    # Import VAD metrics
    vad_metrics = vad_metrics()

    # Calculate vad metrics
    df = vad_dataset(vad_metrics, df, 'body', 'created_utc')

    # Save the dataframe
    df.to_csv(os.path.join(os.getcwd(), 'vad_metrics_folder', file_name))
