import networkx as nx
import pandas as pd
import os


def create_network(data_frame, path_to_save):
    """
    Create a complex network from a pandas data frame
    :param data_frame: pandas data frame
    :param path_to_save: path where to save complex network in glm format extension
    :return: None
    """

    # initialize graph
    g_symmetric = nx.Graph()
    for index, values in data_frame.iterrows():
        g_symmetric.add_node(values['author'])
        g_symmetric.add_node(values['subreddit'])
        g_symmetric.add_edge(values['author'], values['subreddit'])

    nx.write_gml(g_symmetric, os.path.join(path_to_save))


def new_create_network(data_frame, path_to_save):
    """
    Create a complex network from a pandas data frame
    :param data_frame: pandas data frame
    :param path_to_save: path where to save complex network in glm format extension
    :return: None
    """
    dictionary_values = {}
    for index, values in data_frame.iterrows():
        if values['subreddit'] not in dictionary_values.keys():
            dictionary_values[values['subreddit']] = [values['author']]
        else:
            dictionary_values[values['subreddit']].append(values['author'])
    # for k in dictionary_values.keys():
    #     print(len(dictionary_values[k]))
    # print(dictionary_values)

    list_tuples = []
    for key in list(dictionary_values.keys())[:30]:
        values = dictionary_values[key]
        values = list(set(values))
        if len(values) > 200 and (len(values) < 1000):
            for i, val_i in enumerate(values):
                for ii, val_ii in enumerate(values):
                    if i != ii:
                        val = values[ii]
                        list_tuples.append((values[i], val))

    # list_tuples = list_tuples[:10]
    # initialize graph
    g_symmetric = nx.DiGraph()
    g_symmetric.add_edges_from(list_tuples)

    nx.write_gml(g_symmetric, os.path.join(path_to_save))


if __name__ == '__main__':

    # Insert Reddit dataframe to calculate the network
    filename = 'bitcoin_2019_august_data'
    path = os.path.join(os.getcwd(), 'reddit_data', 'clean_data', filename+'.csv')
    path_saver = os.path.join(os.getcwd(), 'complex_networks', filename+'aaaqqq.gml')

    # load dataframe
    df = pd.read_csv(path)

    # Create complex network
    # create_network(df, path_saver)
    new_create_network(df, path_saver)
    print(f'Network created as {filename}')
