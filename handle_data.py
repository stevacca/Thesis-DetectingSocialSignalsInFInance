#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from reddit_messages_scraping import from_datestamp_to_unix_date
import os

'''Permette di vedere i risultati dei dati estratti! E quanti messaggi si salvano sui 500 inizialmente scrappati'''


def read_json(path):
    """
    Function to read a json file
    :param path: path where the file is located
    :param file_name: file name
    :return: an array with the json data loaded
    """

    with open(os.path.join(path), 'r', encoding='utf8') as f:
        array = json.load(f)
        return array


def read_reddit_data_from_folder(path, query_name, from_day, to_day):
    """
    Function to read all the json files

    :param path: path where all the file are located
    :param query_name: name standard of the query
    :param from_day: starting day
    :param to_day: final day
    :return:
    """
    data = []
    for start_date in range(from_day, to_day, 1800):
        file_name = query_name + '_' + str(start_date)
        data += [read_json(path)]

    return count_messages(data)


def count_messages(data_messages):
    """

    :param data_messages:
    :return:
    """
    n_sub_reddits, n_authors = [], []
    n_messages, i = [], 0
    for message in data_messages:
        message = message[0]
        if 'body' in message.keys():
            if message['body'] != '':
                n_messages.append(message['body'])
                n_sub_reddits.append(message['subreddit'])
                n_authors.append(message['author'])

    results = []
    for i, values in enumerate(n_messages):
        results.append((n_messages[i], n_sub_reddits[i], n_authors[i]))

    return results


def create_dict_keys(list):
    """
    From list of tuples to dict with keys
    :param list:
    :return:
    """
    n_messages, n_sub_reddits, n_authors = [], [], []
    for message, subreddit, author in list:
        n_messages += [message]
        n_sub_reddits += [subreddit]
        n_authors += [author]

    return {'messages': n_messages, 'subreddits': n_sub_reddits, 'authors': n_authors}


def authors_with_max_comments(authors_with_max_comments, n_authors=10):

    top_authors = {}
    for author in authors_with_max_comments:
        if author not in top_authors.keys():
            top_authors[author] = 1
        else:
            top_authors[author] += 1

    # sort the values:
    dictionary = []
    for w in sorted(top_authors, key=top_authors.get, reverse=True):
        dictionary.append((w, top_authors[w]))

    return dictionary[:n_authors]


if __name__ == '__main__':
    query = 'coronavirus'

    # set the folder and the date
    path_loader = os.path.join(os.getcwd(), 'reddit_data', 'Coronavirus_messages_coronavirus.csv')
    from_day = '2018-01-01 00:00:00'
    to_day = '2020-08-01 03:00:00'

    print(f'period of extraction data: {from_day[:9]} to {to_day[:9]}')

    from_day = from_datestamp_to_unix_date(from_day)
    to_day = from_datestamp_to_unix_date(to_day)

    # Load all the data
    data = read_reddit_data_from_folder(path_loader, query, from_day, to_day)

    # create the dict
    data_dictionary = create_dict_keys(data)

    subreddits = data_dictionary['subreddits']
    total_messages = data_dictionary['messages']
    authors = data_dictionary['authors']

    print('The number of total messages: ', len(total_messages))
    print('The number of unique discussions: ', len(subreddits))
    print('The number of total unique authors: ', len(set(authors)))

    # count the author with more messages:
    print(authors_with_max_comments(authors, 10))
