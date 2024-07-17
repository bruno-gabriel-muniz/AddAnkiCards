import sqlite3 as sql

from AddAnkiCards.Db.DbConnect import DbConnect


def armazenaSQLite(
    lista_pag_entrada: list,
    DbConnect: sql.Connection = DbConnect('GeneralDB.db'),
    languageCards: str = 'english',
):
    """
    Funcao Que armazenas as frases em um banco de
    dados SQLite e cria as tabelas dele.
    """
    # Conectando No Banco de Dados
    FrasesDB = DbConnect
    # Criando as tabelas de frases usadas e nao usadas, caso  nao existam
    FrasesDB.execute(
        'CREATE TABLE IF NOT EXISTS FrasesNaoUsadas (FraseId INTEGER PRIM'
        + 'ARY KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, TagLingua'
        + ' TEXT);'
    )
    FrasesDB.execute(
        'CREATE TABLE IF NOT EXISTS FrasesUsadas (FraseId INTEGER PRIMARY '
        + 'KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, TagLingua TEXT);'
    )
    # inserindo as frases e as traducoes no banco de dados
    # das frases nao usadas
    for frase_e_traducao in lista_pag_entrada:
        FrasesDB.execute(
            'INSERT INTO FrasesNaoUsadas (FraseOrig, FraseTrad, TagLingua)'
            + ' VALUES ("{}", "{}", "{}");'.format(
                frase_e_traducao[0], frase_e_traducao[1], languageCards
            )
        )
    FrasesDB.commit()
    FrasesDB.close()
