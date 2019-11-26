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

    import glob, os
    files = []
    for file in glob.glob(os.path.join(os.getcwd(), 'sentiment_results',social+'_sentiment',"*.csv")):
        files.append(file)

    # Credentials
    plotly.tools.set_credentials_file(username='stiffler93', api_key='Ospn0kRCMpCz8XwkI88g')
    fig = tools.make_subplots(rows=1, cols=1)
    df = pd.DataFrame(columns=['Unnamed: 0', 'subreddit', 'body', 'created_utc', 'author', 'sentiment',
       'sentiment_code'])

    for file in files:
        df1 = pd.read_csv(file)
        # print(df1)
        df = df.append(df1)
    print('Numero totale di righe ', len(df))

    if social == 'reddit':
        df['date'] = [from_unix_to_datestamp(ts) for ts in df['created_utc'].tolist()]
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
    df['n_mes'] = [1 for i in df['date']]
    df = df.set_index('date')
    ts = df.groupby('date').n_mes.sum()


    trace = go.Histogram(histfunc="sum",
        x=ts.index,
        y=ts,
        name='N. messaggi ',
                         marker=dict(color='#FFC125'),
                         xbins=dict(size='D1'),  # 1 day
                         autobinx=False
    )

    fig['layout'].update(height=600, width=800,
                         title='Numerosità giornaliera dei messaggi su '+social.capitalize()+' per il tema '
                               + tema.capitalize())
    fig.append_trace(trace, 1, 1)
    py.plot(fig, filename='Sentiment Analysis Reddit')
