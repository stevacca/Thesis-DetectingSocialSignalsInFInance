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


def show_trend(dataframe, frequency, crypto_name, col):
    """
    Function to create a plotly interactive plot of a pandas datafrma
    :param dataframe: pandas dataframe to plot
    :param freq: frequency
    :return: save the figure in direcotry
    """

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dataframe.index, y=dataframe.values, name='Frequenza assoluta', marker_color=col))

    fig.update_layout(title_text='Frequenza assoluta dei messaggi {}'.format(crypto_name),
                      xaxis_rangeslider_visible=True)
    # fig.show()

    # To save figure offline
    # config = {
    #     'scrollZoom': True,
    #     'displayModeBar': True,
    #     'editable': True,
    #     'showLink': False,
    #     'displaylogo': False
    # }
    #
    # plotly.offline.plot(fig, filename=os.path.join('frequenza_assoluta_blockchain_subreddit_'+frequency+'.html'),
    #                     config=config)


def group_dataframes(path_loader, frequency):

    df = pd.read_csv(path_loader)
    print(df.columns)
    df['dates'] = df.created_utc.map(lambda x: from_unix_to_datestamp(x))

    df['dates'] = pd.to_datetime(df.dates)
    df = df.set_index('dates')

    df = df.groupby(pd.Grouper(freq=frequency)).body.count()
    return df


if __name__ == '__main__':

    file_names = ['Bitcoin_messages_subreddit_bitcoin_tesi.csv',
                  'Ethereum_messages_subreddit_ethereum_tesi.csv',
                  # 'Libra&Facebook_messages_libra_folder.csv',
                  # 'libra_messages_subreddit_libra.csv'
                  ]

    colors = ['rgba(152, 0, 0, .8)', '#FF7F00', '#1874CD', '#4F4F4F']
    fig = go.Figure()
    for i, file in enumerate(file_names):
        color = colors[i]
        # set the folder and the date
        path_loader = os.path.join(os.getcwd(), 'reddit_data', '_clean_data', file)
        freq = 'M' # '30D'
        title_name = file.split('_')[0].capitalize()
        bitcoin_df = group_dataframes(path_loader, freq)
        # show_trend(bitcoin_df, freq, title_name, color)

        fig.add_trace(go.Bar(x=bitcoin_df.index, y=bitcoin_df.values, name='Frequenza assoluta', marker_color=color))

        fig.update_layout(title_text='Frequenza assoluta dei messaggi {}'.format(title_name),
                          xaxis_rangeslider_visible=True)
    fig.show()
