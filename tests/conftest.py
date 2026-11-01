from datetime import datetime

import pytest

from Corpus.corpus import Corpus
from Documment.class_arxiv_document import ArxivDocument
from Documment.class_reddit_document import RedditDocument


@pytest.fixture
def corpus(monkeypatch):
    """Prépare trois documents et isole le Singleton pour chaque test.

    :param monkeypatch: Outil pytest restaurant les attributs après le test.
    :return: Corpus fictif avec ses documents et ses auteurs.
    """
    monkeypatch.setattr(Corpus, '_instance', None)
    resultat = Corpus('test')
    resultat.documents = {
        0: RedditDocument(
            titre='Alpha', date=datetime(2026, 10, 1),
            url='https://example.org/alpha', texte='bank bank loan',
            type='Reddit', nb_comments=5, auteur='Alice',
        ),
        1: ArxivDocument(
            titre='Gamma', date=datetime(2026, 10, 3),
            url='https://example.org/gamma', texte='bank market',
            type='Arxiv', list_auteurs=['Alice', 'Bob'],
        ),
        2: RedditDocument(
            titre='Beta', date=datetime(2026, 10, 2),
            url='https://example.org/beta', texte='loan market',
            type='Reddit', nb_comments=3, auteur='Bob',
        ),
    }
    resultat.authors = {}
    resultat.id_document = len(resultat.documents)
    resultat.load_helper_list_auteurs()
    return resultat


