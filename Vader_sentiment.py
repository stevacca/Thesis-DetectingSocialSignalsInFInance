from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import pandas as pd


def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    # print(sentence)
    # TODO: Sometimes there are NAS. Solve this
    try:
        sentiment_dict = sid_obj.polarity_scores(sentence)
    except:
        sentiment_dict = {'compound': 0}
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    #
    # print("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        return "Positive", 1, sentence

    elif sentiment_dict['compound'] <= - 0.05:
        return "Negative", -1, sentence

    else:
        return "Neutral", 0, sentence


if __name__ == '__main__':
    # Reddit
    name_file = 'Libra&Facebook_messages_libra_folder.csv'
    path = os.path.join(os.getcwd(), 'reddit_data', 'clean_data')
    social = 'Reddit'
    # Telegram
    # social = 'Telegram'
    # name_file = 'Scuderia Ferrari_cleanedData_2019-09-01_2019-09-30.csv'
    # path = os.path.join(os.getcwd(), 'telegram_data', 'clean_data')

    df = pd.read_csv(os.path.join(path, name_file))
    print(df.columns)
    if social == 'telegram':
        df['created_utc'] = df['date']
    list_sentiment_results = [(row.created_utc, sentiment_scores(row.body)) for index, row in df.iterrows()]
    df = pd.DataFrame({'date': [date for date, values in list_sentiment_results],
                       'sentiment_code':[values[1] for date, values in list_sentiment_results],
                       'sentiment_label': [values[0] for date, values in list_sentiment_results],
                       'body': [values[2] for date, values in list_sentiment_results]})
    if social == 'Reddit':
        df.to_csv(os.path.join(os.getcwd(), 'sentiment_results', 'reddit_sentiment', 'Vader_sentiment_'+name_file))
    else:
        df.to_csv(os.path.join(os.getcwd(), 'sentiment_results', 'telegram_sentiment', 'Vader_sentiment_'+name_file))