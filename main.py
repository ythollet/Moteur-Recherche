import pandas as pd
from dotenv import load_dotenv

# Librairies projet
from API.reddit import Reddit
from API.arxiv import Arxiv

# Charge les variables du fichier .env nécessaires aux accès aux API.
load_dotenv()


def _load_data() -> pd.DataFrame:
    """Charge et regroupe les documents provenant de Reddit et d'Arxiv

    Return: pd.DataFrame: Documents des deux sources
    """

    # On charge les données Reddit dans un DataFrame
    df_reddit = Reddit._load_data_reddit()

    # On charge les données Arxiv dans un DataFrame
    df_arxiv = Arxiv.load_data_arxiv()

    # Reconstruit un index commun (colonne id)
    df = pd.concat(
        [df_reddit, df_arxiv],
        ignore_index = True
    ).reset_index(names = 'id')

    return df


def main():

    # Chargement des données Reddit et Arxiv en DataFrame
    df = _load_data()

    # 3.1 : affiche le nombre de documents avant filtrage.
    print(f'Nombre de documents : {len(df)}\n')

    # Conserve les identifiants à supprimer après le parcours du DataFrame.
    list_id_row_to_drop = []

    # 3.2 : calcule les statistiques et repère les textes à exclure.
    for row in df.itertuples():

        # Écarte les textes manquants avant les opérations sur les chaînes.
        if pd.isna(row.texte):
            list_id_row_to_drop.append(row.id)
            continue

        print(f'Document {row.id}')
        print(f'Mots : {len(row.texte.split())}')
        print(f'Phrases : {len(row.texte.split("."))}\n')

        # Si le document contient moins de 100 caractères
        if len(row.texte) < 100:

            # On l'ajoute à la liste des éléments à supprimer
            list_id_row_to_drop.append(row.id)

    # Les id correspondent à l'index : supprime les textes manquants ou trop courts.
    df.drop(index = list_id_row_to_drop, inplace = True)

    # Assemble les textes retenus en les séparant par un espace.
    all_docs = ' '.join(df['texte'])


if __name__ == '__main__':
    main()
