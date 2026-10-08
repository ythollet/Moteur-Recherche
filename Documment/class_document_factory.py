from Documment.class_arxiv_document import ArxivDocument
from Documment.class_reddit_document import RedditDocument


class DocumentFactory:

    @staticmethod
    def create_document(
        in_row,
    ):

        # On regarde le type de document
        match in_row.type:

            # Si les données proviennent de Reddit
            case 'Reddit':

                document = RedditDocument(
                    titre = in_row.titre,
                    date = in_row.date,
                    url = in_row.url,
                    texte = in_row.texte,
                    type = in_row.type,
                    auteur = in_row.auteur,
                    nb_comments = in_row.nb_comments,
                )

            # Si les données proviennes d'Arxiv
            case 'Arxiv':

                document = ArxivDocument(
                    titre = in_row.titre,
                    date = in_row.date,
                    url = in_row.url,
                    texte = in_row.texte,
                    type = in_row.type,
                    list_auteurs = in_row.list_auteurs,
                )

            # Si la source de données est inattendue
            case _:
                raise Exception(f'source inconnue : {in_row.type}')

        return document
