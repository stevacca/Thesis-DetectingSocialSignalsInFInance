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


def from_unix_to_datestamp(date_time_stamp):
    """
    Transform from unix to datestamp date
    :param date_time_stamp: single unix format date
    :return: datestamp date
    """
    date_time_stamp = int(date_time_stamp)
    return datetime.utcfromtimestamp(date_time_stamp).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    social = 'reddit'
    tema = 'Bitcoin'

    filenames = [
        ('Libra&Facebook_messages_libra_folder.csv', '#1874CD')
        # ('Vader_sentiment_Orbita Ferrari_cleanedData_2019-09-01_2019-09-30.csv','#1874CD')
                 ]
    n_files = len(filenames)

    plotly.tools.set_credentials_file(username='stiffler93', api_key='Ospn0kRCMpCz8XwkI88g')
    fig = tools.make_subplots(rows=3, cols=1)

    for i in range(1, n_files+1):
        print(i)
        df = pd.read_csv(os.path.join(os.getcwd(), 'vad_metrics_folder', filenames[i-1][0]))
        print(df.columns)
        print(df.date)
        # df['date'] = [from_unix_to_datestamp(ts) for ts in df['date'].tolist()]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))

        df = df.set_index('date')
        ts = df.groupby('date').mean()
        query = filenames[i-1][0].split('_')[2]
        print(ts)
        # Create and style traces
        trace1 = go.Scatter(
            x=ts.index,
            y=ts.valence,
            name='Valence',
            mode='lines+markers',
            line=dict(
                color=filenames[i-1][1],
                width=4)
        )
        trace2 = go.Scatter(
            x=ts.index,
            y=ts.arousal,
            name='Arousal',
            mode='lines+markers',
            line=dict(
                color='#FF4040',
                width=4)
        )
        trace3 = go.Scatter(
            x=ts.index,
            y=ts.dominance,
            name='Dominance',
            mode='lines+markers',
            line=dict(
                color='#FFD700',
                width=4)
        )

        fig.append_trace(trace1, row=1, col=1)
        fig.append_trace(trace2, row=2, col=1)
        fig.append_trace(trace3, row=3, col=1)

    fig['layout'].update(height=600, width=800, title='Andamento delle metriche VAD su Reddit per la chiave di ricerca ' + tema .capitalize())
    py.plot(fig, filename='Sentiment Analysis Reddit')
