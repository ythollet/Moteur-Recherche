from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:

    titre: str
    """ Titre du document """

    date: datetime
    """ Date de publication du document """

    url: str
    """ URL source du document """

    texte: str
    """ Contenu textuel du document """

    type: str
    """ Source du document (Reddit, Arxiv) """

    def infos(self):
        """
        Affiche chaque attribut et sa valeur
        """

        # Pour chaque attribut et sa valeur
        for k, v in vars(self).items():
            print(f'{k} : {v}')

    def __str__(self):
        """
        Renvoie une représentation courte contenant le titre du document.
        """

        return f'Titre : {self.titre}'


if __name__ == '__main__':

    # Exemple local pour afficher les attributs et la représentation du document.
    document = Document(
        date = datetime.now(),
        texte = 'blablabla',
        titre = 'titre1',
        url = 'http://ckhnvubvfzubaefifabù',
        type = 'Reddit'
    )
    document.infos()

    print()
    print(document)
