from dotenv import load_dotenv

# Librairies projet
from Corpus.corpus import Corpus
from SearchEngine.class_search_engine import SearchEngine

# Charge les variables du fichier .env nécessaires aux accès aux API.
load_dotenv()


def main():

    corpus = Corpus(
        nom = "corpus_finance"
    )

    search_engine = SearchEngine(
        in_corpus = corpus
    )

    texte = input("Saisissez votre recherche : ")

    search_engine.search(
        in_text = texte
    )







if __name__ == '__main__':
    main()
