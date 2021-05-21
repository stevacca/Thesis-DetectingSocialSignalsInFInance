#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telethon import TelegramClient, sync
from telethon import utils
import pandas as pd
from reddit_messages_scraping import from_datestamp_to_unix_date
import os


def labelize(messages):
    """
    Function to input the label
    :param messages: messages to be labelized
    :return: labels
    """

    labels = []
    for m in messages:
        print(m[1])
        label = input("")
        if label in ["P", "N", "T"]:
            labels.append(label)
        else:
            while label not in ["P", "N", "T"]:
                print("You get wrong labelizing the message {}, try again!\n ".format(m[1]))
                label = input("")

            labels.append(label)

    return labels


def extract_data(client, query, limit):
    """
    Extract the messages using the Telethon API
    :param query: query name
    :param limit: limit call
    :return: text messages
    """
    messages = []

    for text in client.iter_messages(query, limit=limit):
        if text.message is not None:
            messages.append((text.id, text.message, text.to_id, text.date))

    return messages


def extract_to_csv(my_entities, my_client, my_from_day_timestamp, my_to_day_timestamp):
    """
    Function to extract data from the api and save in csv
    :param api_id: id of the api credentials
    :param api_hash: has api credentials
    :return: None
    """

    for ent in my_entities:
        # All of these work and do the same.
        entity = my_client.get_entity(ent[1])
        file_name = ent[0] + '_' + my_from_day_timestamp[:10] + '_to_' + my_to_day_timestamp[:10]

        data = extract_data(my_client, entity, ent[2])
        data = pd.DataFrame(data, columns=['id', 'text', 'peer_channel', 'date'])

        print(f"The group {ent[0]}:\n")
        mask = (data['date'] > my_from_day_timestamp) & (data['date'] <= my_to_day_timestamp)
        df = data.loc[mask]
        print(df[['text', 'date']])
        df.to_csv(os.path.join(saver_directory, file_name + "_TELEGRAM.csv"),
                  sep='\t', encoding='utf-8')


if __name__ == '__main__':
    # Choose the date
    from_day_timestamp = '2020-08-24 00:00:00'
    to_day_timestamp = '2020-09-06 23:59:59'

    # TELEGRAM NAME GROUP, LINK OF THE CHAT, NUMBER OF MESSAGES TO BE EXTRACTED
    entities = [
        # ('Passione Politica', 'https://t.me/PassionePolitica', 30000),
        # ('Parliamo di politica', 'https://t.me/parliamo_di_politica', 30000),
        # ('OP_Politica_Attualita', 'https://t.me/Gruppo_OP', 300000),

        # ('Scuderia Ferrari', 'https://t.me/ScuderiaFerrariFan', 1500)
        # ('QAnons Italia2', 'https://t.me/QAnons_italia', 30000),
        # ('Qanons Ven-Italia 2 Dark to Light2', 'https://t.me/QanonVeneto', 30000),
        ('Q Research Ven-Ita', 'https://t.me/Veleno57432367', 10000),

        # ('Bad Crypto Podcast', 'https://t.me/thebadcryptopodcast', 20000),
        # ('WCSE RA TALKS', 'https://t.me/wcsetalks', 25000),
        # ('Singularity net', 'https://t.me/singularitynet', 25000),
        # ('AION Network', 'https://t.me/aion_blockchain', 800)
    ]

    print(f'period of extraction data: {from_day_timestamp[:10]} to {to_day_timestamp[:10]}')

    from_day = from_datestamp_to_unix_date(from_day_timestamp)
    to_day = from_datestamp_to_unix_date(to_day_timestamp)

    saver_directory = os.path.join(os.getcwd(), 'telegram_data')

    # CREDENTIALS
    api_id = 308841
    api_hash = 'bbfdf1a9ae2c6139d8148eb2eab960a5'
    client = TelegramClient('session_name', api_id, api_hash).start()
    extract_to_csv(entities, client, from_day_timestamp, to_day_timestamp)
