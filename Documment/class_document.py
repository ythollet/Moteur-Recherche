from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:

    titre: str
    """ Titre du document """

    auteur: str 
    """ Nom de l’auteur """

    date: datetime 
    """ Date de publication """

    url: str
    """ URL source """

    texte: str
    """ Contenu textuel du document """

    def infos(self):

        for k,v in vars(self).items():
            print(f'{k} : {v}')


    def __str__(self):

        return f'Titre : {self.titre}'



if __name__ == '__main__':

    document = Document(
        auteur = 'Jean michel',
        date = datetime.now(),
        texte = 'blablabla',
        titre = 'titre1',
        url = 'http://ckhnvubvfzubaefifabù'
    )
    document.infos()

    print()
    print(document)