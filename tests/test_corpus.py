"""Tests de Corpus avec des documents fictifs, sans accès aux API."""

import Corpus.corpus as module_corpus
from Corpus.corpus import Corpus


def test_singleton(corpus):
    assert Corpus('autre_nom') is corpus
    assert corpus.nom == 'test'


def test_tri_date(corpus, capsys):
    corpus.show_docs_order_by_date(2)
    texte = capsys.readouterr().out
    assert texte.index('titre: Gamma') < texte.index('titre: Beta')
    assert 'titre: Alpha' not in texte


def test_tri_titre(corpus, capsys):
    corpus.show_docs_order_by_title(2)
    texte = capsys.readouterr().out
    assert texte.index('titre: Alpha') < texte.index('titre: Beta')
    assert 'titre: Gamma' not in texte


def test_tri_limite_zero(corpus, capsys):
    corpus.show_docs_order_by_date(0)
    corpus.show_docs_order_by_title(0)
    assert capsys.readouterr().out == ''


def test_auteurs(corpus):
    assert set(corpus.authors) == {'Alice', 'Bob'}
    assert set(corpus.authors['Alice'].productions) == {0, 1}
    assert set(corpus.authors['Bob'].productions) == {1, 2}
    assert corpus.authors['Alice'].nb_docs == 2


def test_sauvegarde_rechargement(corpus, tmp_path, monkeypatch):
    # Redirige les fichiers vers le dossier temporaire fourni par pytest.
    module_fictif = tmp_path / 'Corpus' / 'corpus.py'
    monkeypatch.setattr(module_corpus, '__file__', str(module_fictif))

    def interdire_api():
        raise AssertionError('Aucun appel API attendu')

    monkeypatch.setattr(module_corpus, 'load_raw_data', interdire_api)
    corpus.save()
    assert (tmp_path / 'CorpusData' / 'test.csv').is_file()

    # Un objet neuf permet de vérifier les données réellement relues.
    monkeypatch.setattr(Corpus, '_instance', None)
    recharge = Corpus('test')
    recharge.load()

    assert recharge is not corpus
    assert recharge.id_document == 3
    assert set(recharge.documents) == set(corpus.documents)
    for identifiant, original in corpus.documents.items():
        restaure = recharge.documents[identifiant]
        assert isinstance(restaure, type(original))
        assert vars(restaure) == vars(original)
    assert set(recharge.authors) == {'Alice', 'Bob'}
    assert set(recharge.authors['Alice'].productions) == {0, 1}
    assert set(recharge.authors['Bob'].productions) == {1, 2}


def test_recherche_mot_absent(corpus):
    assert corpus.search('absent') == []


def test_statistiques_frequences(corpus):
    _, frequences = corpus.stats()
    assert corpus.nb_mots == 3
    assert frequences.loc['bank', 'nb_occ_total'] == 3
    assert frequences.loc['bank', 'nb_documents'] == 2
