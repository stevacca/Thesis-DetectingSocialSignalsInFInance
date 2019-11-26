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
    tema = 'Facebook'

    filenames = [
        ('Vader_sentiment_facebook_messages_libra_folder.csv', '#1874CD'),
        ('Vader_sentiment_Libra&Facebook_messages_libra_folder.csv','#1874CD')
        # ('Vader_sentiment_Leclerc_messages_2019_september_data.csv','#1874CD'),
        #          ('Vader_sentiment_Vettel_messages_2019_september_data.csv', '#228B22')
        # ('Vader_sentiment_ferrari_2019_september_data.csv', '#DC143C'),
                 # ('Vader_sentiment_formula1_2019_september_data.csv', '#3D59AB'),
                 # ('Vader_sentiment_scuderiaferrari_2019_september_data.csv', '#228B22') # troppe poche osservazioni
                 ]
    n_files = len(filenames)

    plotly.tools.set_credentials_file(username='stiffler93', api_key='Ospn0kRCMpCz8XwkI88g')
    fig = tools.make_subplots(rows=n_files, cols=1)

    for i in range(1, n_files+1):
        print(i)
        df = pd.read_csv(os.path.join(os.getcwd(), 'sentiment_results', social+'_sentiment', filenames[i-1][0]))
        print(df.columns)
        if social == 'reddit':
            df['date'] = [from_unix_to_datestamp(ts) for ts in df['date'].tolist()]
        else:
            df['date'] = [from_unix_to_datestamp(ts) for ts in df['date'].tolist()]
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))

        df = df.set_index('date')
        ts = df.groupby('date').sentiment_code.mean()
        query = filenames[i-1][0].split('_')[2]

        # Create and style traces
        trace = go.Scatter(
            x=ts.index,
            y=ts,
            name='Sentiment ' + query.capitalize(),
            mode='lines+markers',
            line=dict(
                color=filenames[i-1][1],
                width=4)
        )

        fig.append_trace(trace, i, 1)

    fig['layout'].update(height=600, width=800, title='Sentiment Analysis su Reddit per il tema ' + tema .capitalize())
    py.plot(fig, filename='Sentiment Analysis Reddit')
