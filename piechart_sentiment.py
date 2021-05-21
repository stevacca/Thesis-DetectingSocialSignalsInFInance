import pandas as pd
import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # BITCOIN
    files_sentiment = [
        # 'Vader_sentiment_Bitcoin_messages_subreddit_bitcoin_tesi.csv',
        #                'Vader_sentiment_BitcoinMarkets_messages_subreddit_BitcoinMarkets_tesi.csv',
                       'Vader_sentiment_EthTrader_messages_subreddit_EthTrader_tesi.csv',
                       'Vader_sentiment_Ethereum_messages_subreddit_ethereum_tesi.csv'
                       ]
    names = ['r/BitcoinMarkets', 'r/EthTrader']
    i = 0
    fig1, ax1 = plt.subplots(ncols=2)
    for file in files_sentiment:

        df = pd.read_csv(os.path.join(os.getcwd(), 'sentiment_results', 'reddit_sentiment', file))

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