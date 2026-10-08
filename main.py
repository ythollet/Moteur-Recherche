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

    corpus.concorde('the',5)








if __name__ == '__main__':
    main()
