# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt
from plotly import tools
import os
from bs4 import BeautifulSoup
from datetime import datetime
import plotly
import urllib.request
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')


def adjuste_data(rows):
    i = 0
    data = []

    for row in rows:
        tmp = []
        tds = row.findChildren()

        for td in tds:
            tmp.append(td.text)

        if i > 0:
            tmp[0] = tmp[0].replace(',', '')
            tmp[5] = tmp[5].replace(',', '')
            tmp[6] = tmp[6].replace(',', '')
            data.append({'date': datetime.strptime(tmp[0], '%b %d %Y'),
                         'open': float(tmp[1] if tmp != '-' else 0.0),
                         'high': float(tmp[2] if tmp != '-' else 0.0),
                         'low': float(tmp[3] if tmp != '-' else 0.0),
                         'close': float(tmp[4] if tmp != '-' else 0.0),
                         'volume': float(tmp[5] if tmp not in ['-'] else 0.0)
                            , 'mcap': float(tmp[6] if tmp is not str(float) else 0.0)
                         })

        i = i + 1

    return data


def from_unix_to_datestamp(date_time_stamp):
    """
    Transform from unix to datestamp date
    :param date_time_stamp: single unix format date
    :return: datestamp date
    """
    date_time_stamp = int(date_time_stamp)
    return datetime.utcfromtimestamp(date_time_stamp).strftime('%Y-%m-%d %H:%M:%S')

def create_cripto_dataframe(cripto_name, start_time, end_time):

    link = 'https://coinmarketcap.com/currencies/' + cripto_name + '/historical-data/?start=' + start_time + '&end=' + end_time
    with urllib.request.urlopen(link) as url:
        s = url.read()
    soup = BeautifulSoup(s, 'html.parser')
    print((soup))
    print()
    print(soup.prettify())
    pricediv = soup.find('table', {'class': 'table'})
    print(pricediv)
    # rows = pricediv.find_all('tr')
    # # table = soup.find('table', {'class': 'table'})
    # return adjuste_data(rows)

def correlation_plot(dataframe):

    a4_dims = (11.7, 8.27)
    fig, ax = plt.subplots(figsize=a4_dims)
    corr = dataframe.corr()
    sns.heatmap(corr,
                xticklabels=corr.columns,
                yticklabels=corr.columns, robust=True, annot=True, ax=ax)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=85)

    plt.show()


def create_crypto_features(dataframe, name_cripto):
    """
    Dataframe taken by coinmarketcap and with the following columns:
    {'Data', 'Aperto*', 'Alto', 'Basso', 'Vicino**', 'Volume',
       'Cap. del mercato'}

    :param dataframe: dataframe manually created from coinmarketcap.com
    :return: dataframe with three new columns: delta_price, High_differencig_1_price, Low_differencig_1_price
    """
    dataframe = dataframe[::-1]
    dataframe.columns = ['Data_'+name_cripto, 'Open_'+name_cripto, 'High_'+name_cripto,
                         'Low_'+name_cripto, 'Near_'+name_cripto, 'Volume_'+name_cripto,
                         'Cap. del mercato'+name_cripto]
    # Create two new features
    dataframe['delta_price'+name_cripto] = dataframe.apply(lambda x: x['High_'+name_cripto] - x['Low_'+name_cripto], axis=1)
    dataframe['High_differencig_1_price_'+name_cripto] = dataframe['High_'+name_cripto].diff()
    dataframe['Low_differencig_1_price_'+name_cripto] = dataframe['Low_'+name_cripto].diff()
    dataframe['date_'+name_cripto] = pd.to_datetime(dataframe['Data_'+name_cripto], errors='coerce')

    return dataframe


def concat_sentiment_scores(main_dataframe, filenames_sentiment):

    n_files = len(filenames_sentiment)
    for i in range(1, n_files + 1):
        print(i)
        dataframe = pd.DataFrame()
        # name = [name_cripto_1 if name_cripto_1  in filenames_sentiment[i-1].split('_') else name_cripto_2][0]
        name = filenames_sentiment[i - 1].split('_')[2]
        print(name)
        df = pd.read_csv(
            os.path.join(os.getcwd(), 'sentiment_results', social + '_sentiment', filenames_sentiment[i - 1]))
        df['date'] = [from_unix_to_datestamp(ts) for ts in df['date'].tolist()]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
        df['datetime'] = df['date']
        df = df.set_index('date')
        df = df.groupby('date').mean()

        dataframe['sentiment_code_' + name] = df['sentiment_code'].tolist()
        main_dataframe = pd.concat([main_dataframe, dataframe], axis=1, sort=False)
    return main_dataframe


def concat_vads_scores(main_dataframe, filenames_vads):
    n_files = len(filenames_vads)

    for i in range(1, n_files + 1):
        dataframe = pd.DataFrame()
        print(i)
        # name = [name_cripto_1 if name_cripto_1 in filenames_sentiment[i - 1].split('_') else name_cripto_2][0]
        name = filenames_vads[i-1].split('_')[0]
        print(name)
        df = pd.read_csv(
                os.path.join(os.getcwd(), 'vad_metrics_folder', filenames_vads[i - 1]))
        # df['date'] = [from_unix_to_datestamp(ts) for ts in df['date'].tolist()]
        print(df.columns)
            # print(df)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))

        df = df.set_index('date')
        df = df.groupby('date').mean()

        # dataframe['date_' + name_cripto_1] = df.index
        dataframe['valence_' + name] = df['valence'].tolist()
        dataframe['arousal_' + name] = df['arousal'].tolist()
        dataframe['dominance_' + name] = df['dominance'].tolist()
        main_dataframe = pd.concat([main_dataframe, dataframe], axis=1, sort=False)

    return main_dataframe


if __name__ == '__main__':
    name_cripto_1 = 'aion'
    name_cripto_2 = 'bitcoin'
    social = 'reddit'
    tema = 'Bitcoin'
    cripto = 'bitcoin'
    start_time, end_time = '20171201', '20180115'

    #######################
    # CRIPTOVALUTE
    # dataset aion
    df_cripto1 = pd.read_excel(os.path.join(os.getcwd(), 'data_cripto', 'aion1Dec_15Gen2017_18_data.xlsx'))
    df_cripto1 = create_crypto_features(df_cripto1, name_cripto_1)

    # dataset bitcoin
    df_cripto2 = pd.read_excel(os.path.join(os.getcwd(), 'data_cripto', 'bitcoin1Dec_15Gen2017_18_data.xlsx'))
    df_cripto2 = create_crypto_features(df_cripto2, name_cripto_2)

    # join two datframes
    main_df = pd.concat([df_cripto1, df_cripto2], axis=1, sort=False)
    # TODO: DATA ORIDNATA
    data = main_df.date_bitcoin.tolist()

    #######################
    # SENTIMENT
    # Add Sentiment scores
    filenames_sentiment = [
        'Vader_sentiment_bitcoin_messages_2017_2018_aion_data.csv',
        'Vader_sentiment_aion_messages_2017_2018_aion_data.csv'
    ]

    main_df = concat_sentiment_scores(main_df, filenames_sentiment)

    #######################
    # VAD SCORES
    # Add VAD scores
    filenames_vads = [
        'bitcoin_messages_2017_2018_aion_data.csv',
        'aion_messages_2017_2018_aion_data.csv'
        ]

    main_df = concat_vads_scores(main_df, filenames_vads)
    print(main_df)
    print(main_df.columns)


    # plot the heatmap
    df = main_df[['Open_aion', 'High_aion', 'Low_aion',
        'Cap. del mercatoaion', 'delta_priceaion',
       'High_differencig_1_price_aion', 'Low_differencig_1_price_aion',
       'Open_bitcoin', 'High_bitcoin',
       'Low_bitcoin', 'Cap. del mercatobitcoin', 'delta_pricebitcoin',
       'High_differencig_1_price_bitcoin', 'Low_differencig_1_price_bitcoin',
       'sentiment_code_aion', 'sentiment_code_bitcoin', 'valence_aion', 'arousal_aion',
       'dominance_aion', 'valence_bitcoin', 'arousal_bitcoin',
       'dominance_bitcoin']]


    df['date'] = data
    df = df.dropna()
    df = df.set_index('date')
    print(df.head())
    # df = df['2017-12-11':'2017-12-18']
    correlation_plot(df)

    ##################
    # CLASSIFIER
    rf = RandomForestRegressor(n_estimators=100,
                               n_jobs=-1,
                               oob_score=True,
                               bootstrap=True,
                               random_state=42)

    df = df.reset_index()
    df = df.loc[:, df.columns != 'date']
    print(df)
    print(df.columns)

    df = df[['delta_priceaion',
       'sentiment_code_aion', 'sentiment_code_bitcoin', 'valence_aion', 'arousal_aion',
       'dominance_aion', 'valence_bitcoin', 'arousal_bitcoin',
       'dominance_bitcoin']]

    X = df.loc[:, df.columns != 'delta_priceaion'].values
    y = df.loc[:, 'delta_priceaion'].values
    y = y.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)
    rf.fit(X_train, y_train)

    print('R^2 Training Score: {:.2f} \nOOB Score: {:.2f} \nR^2 Validation Score: {:.2f}'.format(
        rf.score(X_train, y_train),
        rf.oob_score_,
        rf.score(X_test, y_test))
    )

    importances = rf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in rf.estimators_],
                     axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    a = df.loc[:, df.columns != 'delta_priceaion']
    columns = a.columns.tolist()

    i = 0
    c = []
    for f in range(X.shape[1]):
        print("%d. feature %s (%f)" % (f + 1, columns[i], importances[indices[f]]))
        c.append(columns[i])
        i += 1
    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.show()

    # df.to_csv(os.path.join(os.getcwd(), 'senti_cripto_dataframes', query+'_cripto_'+cripto+'.csv'))
