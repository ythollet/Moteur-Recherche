import os
from ensurepip import __main__

import pandas as pd
from dotenv import load_dotenv

# Librairies projet
from API.reddit import Reddit
from API.arxiv import Arxiv
from Corpus.corpus import Corpus

# Charge les variables du fichier .env nécessaires aux accès aux API.
load_dotenv()





def main():

    corpus = Corpus(
        nom = "corpus_finance"
    )

    corpus.load()

    dict_documents, df_freq = corpus.stats()

    matrix_tf = corpus.build_matrix_tf(
        in_df_freq = df_freq,
        in_dict_documents = dict_documents
    )







if __name__ == '__main__':
    main()
