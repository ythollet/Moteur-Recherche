"""Tests du moteur avec des valeurs attendues calculées sur trois textes."""

from math import log, sqrt

import numpy as np
import pandas as pd
import pytest

from SearchEngine.class_search_engine import SearchEngine


@pytest.fixture
def moteur(corpus, monkeypatch):
    """Construit le vrai moteur en conservant le corpus fictif déjà préparé.

    :param corpus: Corpus fictif partagé avec les tests de Corpus.
    :param monkeypatch: Outil pytest isolant le chargement depuis le disque.
    :return: Moteur utilisant les textes bank bank loan, bank market, loan market.
    """
    monkeypatch.setattr(corpus, "load", lambda: None)
    return SearchEngine(corpus)


def test_matrice_tf(moteur):
    # Colonnes explicites : le test ne dépend pas de l'ordre interne des mots.
    colonnes = [moteur.dict_mots[mot]["id_mot"] for mot in ("bank", "loan", "market")]
    matrice = moteur.build_matrix_tf().toarray()[:, colonnes]
    np.testing.assert_array_equal(matrice, [[2, 1, 0], [1, 0, 1], [0, 1, 1]])


def test_matrice_tf_idf(moteur):
    # Chaque mot apparaît dans deux des trois documents : IDF = ln(3/2).
    colonnes = [moteur.dict_mots[mot]["id_mot"] for mot in ("bank", "loan", "market")]
    attendu = np.array([[2, 1, 0], [1, 0, 1], [0, 1, 1]]) * log(3 / 2)
    np.testing.assert_allclose(moteur.idf_mots, log(3 / 2))
    np.testing.assert_allclose(moteur.matrix_tf_idf.toarray()[:, colonnes], attendu)


def test_vectorisation_normalise_et_ignore_mots_inconnus(moteur):
    vecteur = moteur.vectorize_texte("BANK, bank! inconnu 123\n").toarray()[0]
    attendu = np.zeros(3)
    attendu[moteur.dict_mots["bank"]["id_mot"]] = 2 * log(3 / 2)
    np.testing.assert_allclose(vecteur, attendu)


def test_scores_cosinus(moteur):
    scores = moteur.get_list_distances_recherche_documents(moteur.vectorize_texte("bank"))
    assert scores == pytest.approx([2 / sqrt(5), 1 / sqrt(2), 0])


def test_classement_et_format_resultats(moteur):
    resultats = moteur.search("bank", 3)
    assert isinstance(resultats, pd.DataFrame)
    assert list(resultats.index) == [0, 1, 2]
    assert list(resultats["titre"]) == ["Alpha", "Gamma", "Beta"]
    assert resultats["cos_recherche_document"].is_monotonic_decreasing
    assert {"titre", "url", "type", "auteur", "cos_recherche_document"} <= set(resultats.columns)


@pytest.mark.parametrize("nombre, attendu", [(0, 0), (1, 1), (2, 2), (10, 3)])
def test_nombre_resultats(moteur, nombre, attendu):
    assert len(moteur.search("bank", nombre)) == attendu


@pytest.mark.parametrize("source, identifiants", [("Reddit", [0, 2]), ("Arxiv", [1])])
def test_filtre_source(moteur, source, identifiants):
    resultats = moteur.search("bank", 3, source)
    assert list(resultats.index) == identifiants
    assert set(resultats["type"]) == {source}


def test_filtre_applique_avant_limite(moteur):
    # Le meilleur résultat global vient de Reddit ; Arxiv doit tout de même
    # fournir son meilleur document quand on demande un seul résultat Arxiv.
    assert list(moteur.search("bank", 1, "Arxiv").index) == [1]


def test_source_invalide(moteur):
    with pytest.raises(ValueError, match="Source inconnue"):
        moteur.search("bank", 2, "inconnue")


@pytest.mark.parametrize("requete", ["", "   ", "inconnu", "123 !!!"])
def test_requete_sans_mot_connu(moteur, requete):
    # Comportement actuel : les documents sont conservés avec un score nul.
    resultats = moteur.search(requete, 3)
    assert list(resultats.index) == [0, 1, 2]
    assert list(resultats["cos_recherche_document"]) == [0, 0, 0]


def test_top_mots(moteur):
    resultats = moteur.get_top_mots(2)
    assert list(resultats["mot"]) == ["bank", "loan"]
    assert list(resultats["score_tf_idf"]) == pytest.approx([log(3 / 2), 2 * log(3 / 2) / 3])


def test_top_mots_source(moteur):
    resultats = moteur.get_top_mots(3, "Arxiv")
    assert list(resultats["mot"]) == ["bank", "market"]
    assert list(resultats["score_tf_idf"]) == pytest.approx([log(3 / 2), log(3 / 2)])
