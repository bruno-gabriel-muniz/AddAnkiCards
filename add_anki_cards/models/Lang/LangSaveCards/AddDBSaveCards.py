import sqlite3 as sql

from add_anki_cards.Db import DbConnect


def armazena_sqlite(
    lista_pag_entrada: list,
    db: sql.Connection | sql.Cursor = DbConnect.db_connect('GeneralDB.db'),
    language_cards: str = 'english',
):
    """Func. q armazena as frases em um banco de dados SQLite."""
    # Conectando No Banco de Dados
    cursor_db = db.cursor()
    # Criando as tabelas de frases usadas e nao usadas, caso  nao existam
    cursor_db.execute(
        'CREATE TABLE IF NOT EXISTS FrasesNaoUsadas (FraseId INTEGER PRIM'
        + 'ARY KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, TagLingua'
        + ' TEXT);'
    )
    cursor_db.execute(
        'CREATE TABLE IF NOT EXISTS FrasesUsadas (FraseId INTEGER PRIMARY '
        + 'KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, TagLingua TEXT);'
    )
    # inserindo as frases e as traducoes no banco de dados
    # das frases nao usadas
    for frase_e_traducao in lista_pag_entrada:
        cursor_db.execute(
            'INSERT INTO FrasesNaoUsadas (FraseOrig, FraseTrad, TagLingua)'
            + f' VALUES ("{frase_e_traducao[0]}", "{frase_e_traducao[1]}", '
            + f'"{language_cards}");'
        )
    db.commit()
    cursor_db.close()
