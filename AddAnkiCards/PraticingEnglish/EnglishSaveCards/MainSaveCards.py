from AddAnkiCards.Db.DbConnect import DbConnect
from AddAnkiCards.PraticingEnglish.EnglishSaveCards import (
    AddDBSaveCards,
    ReadSaveCards,
)


def mainSaveCards(
    newCards: str,
    separatorCards: str,
    separetorTranslate: str,
    languageCards: str = 'english',
    Db=DbConnect(),
):
    """
    Funcao principal da leitura do arquivo com as frases.
    """
    # variável que contem as linhas da página
    # com as frases e as traducoes separadas
    lista_pag_entrada = ReadSaveCards.reader(
        newCards, separatorCards, separetorTranslate
    )
    AddDBSaveCards.armazenaSQLite(
        lista_pag_entrada, languageCards=languageCards, DbConnect=Db
    )
