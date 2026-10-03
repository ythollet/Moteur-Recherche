from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:

    titre: str
    """ Titre du document """

    date: datetime
    """ Date de publication """

    url: str
    """ URL source """

    texte: str
    """ Contenu textuel du document """

    origine : str
    """ Source du document """

    def infos(self):

        for k,v in vars(self).items():
            print(f'{k} : {v}')


    def __str__(self):

        return f'Titre : {self.titre}'





if __name__ == '__main__':

    document = Document(
        date = datetime.now(),
        texte = 'blablabla',
        titre = 'titre1',
        url = 'http://ckhnvubvfzubaefifabù',
        origine = 'Reddit'
    )
    document.infos()

    print()
    print(document)