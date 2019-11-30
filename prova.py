import os
import pandas as pd
import networkx as nx


def new_create_network(data_frame, path_to_save):
    """
    Create a complex network from a pandas data frame
    :param data_frame: pandas data frame
    :param path_to_save: path where to save complex network in glm format extension
    :return: None
    """
    list_tuples = []
    for index, values in data_frame.iterrows():
        list_tuples.append((str(values['A']), str(values['B'])))
    print(list_tuples)

    # for key in list(dictionary_values.keys()):
    #     print(key)
    #     values = dictionary_values[key]
    #     values = list(set(values))
    #     # if len(values) > 200 and (len(values) < 1000):
    #     for i, val_i in enumerate(values):
    #         for ii, val_ii in enumerate(values):
    #             if i != ii:
    #                 val = values[ii]
    #                 list_tuples.append((values[i], val))
    # # print(list_tuples)
    # list_tuples = list_tuples[:10]
    # # initialize graph
    g_symmetric = nx.DiGraph()
    g_symmetric.add_edges_from(list_tuples)

    nx.write_gml(g_symmetric, os.path.join(path_to_save))


if __name__ == '__main__':
    path = 'C:\\Users\\stefa\\Documents\\network_btc.csv'
    df = pd.read_csv(path)
    new_create_network(df, 'aa.gml')