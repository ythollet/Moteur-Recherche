from pathlib import Path

import streamlit as st

from Corpus.corpus import Corpus
from SearchEngine.class_search_engine import SearchEngine


@st.cache_resource(show_spinner = "Chargement du corpus et construction du moteur…")
def charger_moteur() -> SearchEngine:
    """Charge une seule fois le moteur depuis le corpus sauvegardé.

    :return: Moteur de recherche prêt à être interrogé.
    :raises FileNotFoundError: Si le corpus sauvegardé est absent.
    """
    # Empêche le chargement de secours par les API si la sauvegarde manque.
    chemin_corpus = Path(__file__).resolve().parent / "CorpusData" / "corpus_finance.csv"
    if not chemin_corpus.is_file():
        raise FileNotFoundError(
            "Le corpus sauvegardé CorpusData/corpus_finance.csv est introuvable."
        )

    return SearchEngine(in_corpus = Corpus(nom = "corpus_finance"))


st.set_page_config(page_title = "Moteur de recherche", layout = "wide")
st.title("Moteur de recherche")

try:
    moteur = charger_moteur()
except Exception as erreur:
    st.error(f"Impossible de charger le moteur : {erreur}")
    st.stop()

if moteur.corpus.nb_docs == 0:
    st.warning("Le corpus sauvegardé ne contient aucun document.")
    st.stop()

st.caption(f"Corpus finance · {moteur.corpus.nb_docs} documents Reddit et Arxiv")

mots_cles = st.text_input("Mots clés", placeholder = "Exemple : investment bank")

if moteur.corpus.nb_docs > 1:
    nombre_articles = st.slider(
        "Nombre d’articles à extraire",
        min_value = 1,
        max_value = moteur.corpus.nb_docs,
        value = min(5, moteur.corpus.nb_docs),
    )
else:
    nombre_articles = 1
    st.caption("Un seul article est disponible dans le corpus.")

source = st.selectbox("Source", options = ["Toutes", "Reddit", "Arxiv"])

if st.button("Rechercher", type = "primary"):
    # Conserve les résultats quand on règle ensuite le graphique.
    st.session_state.pop("derniere_recherche", None)
    requete = mots_cles.strip()
    if not requete:
        st.warning("Saisissez au moins un mot-clé.")
    else:
        try:
            with st.spinner("Recherche dans le corpus…"):
                resultats = moteur.search(
                    in_text = requete,
                    in_nb_docs_to_return = nombre_articles,
                    in_source = None if source == "Toutes" else source,
                )

            st.session_state["derniere_recherche"] = (requete, source, resultats)
        except Exception as erreur:
            st.error(f"La recherche a échoué : {erreur}")

if "derniere_recherche" in st.session_state:
    requete_affichee, source_affichee, resultats = st.session_state["derniere_recherche"]
    st.caption(f"Résultats pour « {requete_affichee} » · Source : {source_affichee}")
    if resultats.empty:
        st.info("Aucun document pour cette source.")
    else:
        st.dataframe(
            resultats,
            width = "stretch",
            column_config = {
                "auteurs": "Auteurs",
                "url": st.column_config.LinkColumn(
                    "lien", display_text = "Ouvrir l’article"
                )
            },
        )

# Bonus 7 : exploration du vocabulaire de tout le corpus ou de la source choisie.
st.divider()
st.subheader("Mots les plus importants du corpus")
st.caption(
    f"Source : {source}. Score TF-IDF moyen sur les documents de cette source, "
    "avec l’IDF du corpus complet. Ce graphique est indépendant de la requête. "
    "Les mots de moins de trois caractères, ceux contenant une apostrophe "
    "et les scores nuls sont exclus."
)
nombre_mots = st.slider("Nombre de mots à afficher", min_value = 5, max_value = 30, value = 15)
top_mots = moteur.get_top_mots(
    in_nb_mots = nombre_mots,
    in_source = None if source == "Toutes" else source,
)
if top_mots.empty:
    st.info("Aucun mot à afficher pour cette source.")
else:
    st.bar_chart(
        top_mots.rename(columns = {"mot": "Mot", "score_tf_idf": "Score TF-IDF moyen"}),
        x = "Mot",
        y = "Score TF-IDF moyen",
        horizontal = True,
        sort = "-Score TF-IDF moyen",
        height = max(300, len(top_mots) * 25),
    )
