import pandas as pd
import os
import matplotlib.pyplot as plt

import seaborn as sns
from matplotlib.gridspec import GridSpec


if __name__ == '__main__':
    # BITCOIN
    files_sentiment = [
        # 'Vader_sentiment_Bitcoin_messages_subreddit_bitcoin_tesi.csv',
        #                'Vader_sentiment_BitcoinMarkets_messages_subreddit_BitcoinMarkets_tesi.csv',
                       'Vader_sentiment_CoronaCoin_cleanedData_2019-09-01_2020-03-10.csv',
                       # 'Vader_sentiment_Ethereum_messages_subreddit_ethereum_tesi.csv'
                       ]
    names = ['r/BitcoinMarkets', 'r/EthTrader']
    i = 0
    fig1, ax1 = plt.subplots(ncols=2)
    for file in files_sentiment:

        df = pd.read_csv(os.path.join(os.getcwd(), 'sentiment_results', 'telegram_sentiment', file))

        vals = df.groupby('sentiment_label').count()
        print(vals)

        # Pie chart
        labels = [str(item) for item in vals.index.tolist()]
        sizes = vals.sentiment_code.tolist()
        # only "explode" the 2nd slice (i.e. 'Hogs')

        explode = (0.05, 0.05, 0.05)
        plt.suptitle('aaaa', y=4, fontsize=18)

        ax1[i].pie(sizes,
                explode=explode,
                labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax1[i].title.set_text('Sentiment classes of Traders subreddit {}'.format(names[i]))
        ax1[i].axis('equal')
        i += 1
    # plt.title('Sentiment classes of Technical Subreddits r/Bitcoin and r/Ethereum', fontsize=18, loc='left')
    plt.tight_layout()
    plt.show()

    # sns.set(style="whitegrid")
    # # sns.set_color_codes("Spectral")
    # file1 = 'Vader_sentiment_EthTrader_messages_subreddit_EthTrader_tesi.csv'
    # df1 = pd.read_csv(os.path.join(os.getcwd(), 'sentiment_results', 'reddit_sentiment', file1))
    # vals1 = df1.groupby('sentiment_label').count()
    #
    # file2 = 'Vader_sentiment_Ethereum_messages_subreddit_ethereum_tesi.csv'
    # df2 = pd.read_csv(os.path.join(os.getcwd(), 'sentiment_results', 'reddit_sentiment', file2))
    # vals2 = df1.groupby('sentiment_label').count()
    #
    # source_data1 = pd.DataFrame(vals1).reset_index()
    # source_data2 = pd.DataFrame(vals2).reset_index()
    #
    # # flavor_data = pd.DataFrame(flavor_counts).reset_index()
    #
    # plt.figure(2, figsize=(20, 15))
    # the_grid = GridSpec(2, 2)
    #
    # plt.subplot(the_grid[0, 1],
    #             # title='Sentiment classes frequency'
    #             )
    # sns.barplot(x='sentiment_code', y='sentiment_label', data=source_data1, palette='Spectral')
    # # plt.subplot(the_grid[0, 1], title='Selected Flavors of Pies')
    # plt.xlabel("Number of occurrences")
    # plt.ylabel("Sentiment classes")
    # # sns.barplot(x='Source', y='FoodCode', data=flavor_data, palette='Spectral')
    # plt.subplot(the_grid[0, 0],
    #             # title='Sentiment classes frequency'
    #             )
    # sns.barplot(x='sentiment_code', y='sentiment_label', data=source_data2, palette='Spectral')
    #
    # plt.suptitle('Histogram of sentiment class frequency', fontsize=16)
    # plt.show()