import pandas as pd
import os
import numpy as np
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.wrappers import DtmModel
from gensim.models import LdaSeqModel
from gensim.test.utils import datapath


if __name__ == '__main__':
    filename = 'libra_messages_subreddit_libra.csv'
    path = os.path.join(os.getcwd(), 'reddit_data', '_clean_data', filename)
    df = pd.read_csv(path)
    print(df.columns)

    ldaseq = LdaSeqModel(corpus=common_corpus, time_slice=[2, 4, 3], num_topics=2, chunksize=1)
    # temp_file = datapath("model")
    # # ldaseq.save(os.path.join(os.getcwd(), 'dynamic_lda_folder', temp_file))
    # loaded_ldaseq = LdaSeqModel.load(temp_file)
    # print(loaded_ldaseq)
    #
    # doc = common_corpus[1]
    # print(doc)
    #
    # embedding = ldaseq[doc]
    # print(embedding)

    # 2
    # path_to_dtm_binary = os.path.join(os.getcwd(), 'dynamic_lda_folder', 'dtm-win64.exe')
    # model = DtmModel(path_to_dtm_binary, corpus=common_corpus, id2word=common_dictionary,
    #                  time_slices=[1] * len(common_corpus))
    #
    # print(model)