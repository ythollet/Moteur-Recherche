# Moteur-Recherche

## Tests de Corpus et du moteur

Depuis la racine du projet, installer les dépendances de développement puis lancer :

```shell
uv sync --locked
uv run python -m pytest -v
```

Les tests utilisent `pytest` (dépendance de développement) et trois documents fictifs.
Ils vérifient le Singleton, les tris et leur limite, la reconstruction des auteurs,
la sauvegarde puis le rechargement, une recherche sans correspondance et les
fréquences des mots. La sauvegarde se fait dans un dossier temporaire, sans
modifier le corpus réel ni interroger les API. Les tests via l'interface restent
à effectuer séparément.

Les tests du moteur vérifient les matrices TF et TF-IDF, la normalisation de la
requête, les scores cosinus, le classement, le nombre de résultats, les filtres
par source et les mots affichés dans le graphique. Les requêtes sans mot connu
sont aussi testées : le moteur conserve actuellement les documents avec un
score nul. La fixture commune aux tests est définie dans `tests/conftest.py`.

## Collecte Reddit

La collecte combine les communautés `personalfinance`, `financialindependence`
et `Bogleheads`. Pour chacune, elle récupère les publications populaires avec
`hot(limit=None)`, dans les limites imposées par Reddit. Les textes de moins
de 100 caractères sont exclus. Les publications sont regroupées dans une liste ;
les republications ne sont pas dédoublonnées.

Pour renouveler les données brutes depuis un notebook lancé à la racine :

```python
from dotenv import load_dotenv
from API.reddit import Reddit

load_dotenv()
Reddit.main_fetch_data()
```

Cette opération utilise les accès Reddit du fichier `.env` et remplace
`RawData/reddit.csv` après une collecte réussie et non vide. Sauvegarder ce
fichier avant la collecte pour conserver l'ancienne version.
La variable locale `subreddits`, dans `main_fetch_data`, permet de choisir
les communautés à parcourir.

Le corpus final `CorpusData/corpus_finance.csv` n'est pas actualisé automatiquement.
Pour le reconstruire, conserver une copie de l'ancien fichier sous un autre nom,
puis appeler `Corpus("corpus_finance").load()` dans une nouvelle session Python.
Le chargement reconstruira le corpus depuis les données brutes et le sauvegardera.
Redémarrer ensuite l'application pour reconstruire son moteur en cache.

## Collecte Arxiv

La requête combine onze expressions sur les finances personnelles, les
investisseurs particuliers, la culture financière, la retraite, l'endettement,
l'emprunt immobilier et le choix de portefeuille. Les expressions sont reliées
par `OR` : un article peut correspondre à l'une d'elles. La collecte demande
jusqu'à 1 000 articles, classés par pertinence ; seuls les résumés sont indexés.

Pour renouveler les données brutes depuis un notebook lancé à la racine :

```python
from API.arxiv import Arxiv

Arxiv.fetch_data()
```

Sauvegarder `RawData/arxiv.csv` avant cet appel, qui le remplace si des articles
sont trouvés. Reconstruire ensuite le corpus final et redémarrer l'application,
comme indiqué pour Reddit. Élargir la requête peut aussi introduire des articles
moins proches des questions pratiques : contrôler les résultats après collecte.

## Interface web Streamlit (bonus 2)

Depuis la racine du projet, avec Python 3.13 et uv :

```shell
uv sync --locked
uv run streamlit run app.py
```

`pyproject.toml` déclare les dépendances et `uv.lock` fixe leurs versions.
`requirements.txt` est un export des dépendances d'exécution pour une
installation avec `pip install -r requirements.txt`. Après une modification
des dépendances et la mise à jour de `uv.lock`, le régénérer avec :

```shell
uv export --frozen --no-dev --no-emit-project --output-file requirements.txt
```

Ouvrir http://localhost:8501, saisir des mots-clés, choisir le nombre de
résultats et éventuellement la source, puis cliquer sur **Rechercher**.
Le tableau reprend le classement TF-IDF du moteur existant.

L'application utilise `CorpusData/corpus_finance.csv` sans interroger les API.
Si ce fichier manque, un message d'erreur est affiché. Le moteur est conservé
en cache entre les interactions ; après modification du corpus, redémarrer
l'application pour reconstruire le moteur.

### Visualisation du vocabulaire (bonus 7)

Sous les résultats, un diagramme en barres interactif affiche les mots les plus
importants du corpus, avec un curseur de 5 à 30 mots. Le filtre Source s'applique
aussi au graphique. Le score est la moyenne des poids TF-IDF sur les documents
de la source choisie, en conservant l'IDF du corpus complet. Les scores nuls
et les mots de moins de trois caractères sont exclus. Le graphique porte sur
le corpus sélectionné, indépendamment de la requête et du nombre de résultats.

### Avec Docker Compose

Pour construire et démarrer uniquement Streamlit :

```shell
docker compose up -d --build streamlit
```

Ouvrir http://localhost:8501. Pour consulter les journaux ou arrêter ce service :

```shell
docker compose logs streamlit
docker compose stop streamlit
```

Le service `moteur-recherche` conserve l'interface Jupyter sur le port 8888.
`docker compose up -d --build` démarre les deux interfaces.
Les fichiers sont copiés dans les images : pour prendre en compte une
modification du code ou du corpus, reconstruire avec `--build`.
