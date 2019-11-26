import requests
import json
from datetime import datetime
import os


def show_keys(data):
    """
    Function to show up the keys of a list od dictionaties
    :param data: the list with whose istances are dictionaries
    :return: None, it just print out every key dict by dict
    """

    for message in data["data"]:
        print(message.keys())
        print(message["selftext"], message["created_utc"])


def extracting_data(path, file_name, query_name, after, before):
    """
    Extract data messages from Reddit

    :param path: the path where we want to save the files we extract as json
    :param file_name: name of the file
    :param query_name: the name of the query we want to extract
    :param after: the date of start
    :param before: the date of ending
    :return: a json file with all the informations extracted from the API
    """

    url = 'https://api.pushshift.io/reddit/comment/search/?size=500&q=' \
          + query_name + '&after=' + str(after) + '&before=' + str(before)
    resp = requests.get(url=url)
    data = resp.json()

    try:
        with open(os.path.join(path, file_name + '.json'),
                  mode='w', encoding='utf8') as f:
            json.dump([message for message in data["data"]], f, ensure_ascii=False)
            print(f'the file {file_name} has been written')
    except ValueError:
        print("Something went wrong!")


def from_datestamp_to_unix_date(datestamp):
    """
    Change the format of the date from datestamp to unix
    :param datestamp: the datestamp format
    :return: the date in unix codification
    """

    dt = datetime.strptime(datestamp, '%Y-%m-%d  %H:%M:%S')
    unix_timestamp = (dt - datetime(1970, 1, 1)).total_seconds()

    return int(unix_timestamp)


if __name__ == '__main__':
    # https://www.epochconverter.com/

    query = 'Facebook'
    from_day = '2019-09-02 00:00:00'
    to_day = '2019-10-31 23:59:59' # 23:59:59
    folder_name = 'libra_folder'# '2019_august_data'
    print(f'period of extraction data: {from_day} to {to_day}')

    # build the folder you want to save the data
    saver_folder = os.path.join(os.getcwd(), 'reddit_data', folder_name)

    from_day = from_datestamp_to_unix_date(from_day)
    to_day = from_datestamp_to_unix_date(to_day)

    for start_date in range(from_day, to_day, 1800):
        end_date = start_date + 1800
        name_file = query + '_' + str(start_date)
        try:
            extracting_data(saver_folder, name_file, query, start_date, end_date)
        except ValueError:
            print(ValueError)
