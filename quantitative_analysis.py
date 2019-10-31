# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import datetime as dt
from plotly import tools
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import os
from datetime import datetime

def from_unix_to_datestamp(ts):
    """
    Transform from unix to datestamp date
    :param ts: single unix format date
    :return: datestamp date
    """
    ts = int(ts)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    social = 'reddit'
    tema = 'Bitcoin'

    filenames = [
        # ('Vader_sentiment_Orbita Ferrari_cleanedData_2019-09-01_2019-09-30.csv','#1874CD'),
        #          ('Vader_sentiment_Red Passion ferrari_cleanedData_2019-09-01_2019-09-30.csv','#1874CD'),
        #          ('Vader_sentiment_Scuderia Ferrari_cleanedData_2019-09-01_2019-09-30.csv', '#1874CD')
        #          ('Vader_sentiment_Leclerc_messages_2019_september_data.csv','#1874CD'),
        #          ('Vader_sentiment_Vettel_messages_2019_september_data.csv', '#228B22')
        ('sentiment_Bitcoin_messages_2019_14Sett_29Ott.csv', '#DC143C'),
                 # ('Vader_sentiment_formula1_2019_september_data.csv', '#3D59AB'),
                 # ('Vader_sentiment_scuderiaferrari_2019_september_data.csv', '#228B22') # troppe poche osservazioni
                 ]

    n_files = len(filenames)

    # Credentials
    plotly.tools.set_credentials_file(username='stiffler93', api_key='Ospn0kRCMpCz8XwkI88g')
    fig = tools.make_subplots(rows=n_files, cols=1)

    for i in range(1, n_files+1):
        print(f'Creating plot n°{i}')

        df = pd.read_csv(os.path.join(os.getcwd(), 'sentiment_results', social+'_sentiment', filenames[i-1][0]))

        if social == 'reddit':
            df['date'] = [from_unix_to_datestamp(ts) for ts in df['created_utc'].tolist()]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
        df['n_mes'] = [1 for i in df['date']]
        df = df.set_index('date')
        ts = df.groupby('date').n_mes.sum()

        query = filenames[i-1][0].split('_')[2]

        # Create and style traces
        trace = go.Histogram(histfunc="sum",
            x=ts.index,
            y=ts,
            name='N. messaggi ' + query.capitalize(),
                             marker=dict(color='#CD2626'),
                             xbins=dict(size='D1'),  # 1 day
                             autobinx=False
        )

        fig.append_trace(trace, i, 1)


    fig['layout'].update(height=600, width=800, title='Numerosità giornaliera dei messaggi su '+social.capitalize()+' per il tema ' + tema.capitalize())
    py.plot(fig, filename='Sentiment Analysis Reddit')
