import os
import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go

import plotly
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

    file_name = 'bitcoin_messages_subreddit_bitcoin.csv'

    # set the folder and the date
    path_loader = os.path.join(os.getcwd(), 'reddit_data', 'clean_data', file_name)

    df = pd.read_csv(path_loader)
    print(df.columns)
    df['dates'] = df.created_utc.map(lambda x: from_unix_to_datestamp(x))

    df['dates'] = pd.to_datetime(df.dates)
    df = df.set_index('dates')
    df = df.groupby(pd.Grouper(freq='10D')).body.count()

    # fig = px.line(df, x=df.index, y=df.values)
    # fig.show()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.index, y=df.values, name='Frequenza assoluta'))

    fig.update_layout(title_text='Blockchain Frequenza assoluta dei messaggi',
                      xaxis_rangeslider_visible=True)
    fig.show()

    config = {
        'scrollZoom': True,
        'displayModeBar': True,
        'editable': True,
        'showLink': False,
        'displaylogo': False
    }

    plotly.offline.plot(fig, filename=os.path.join('frequenza_assoluta_blockchain_subreddit_10D.html'), config=config)
