import sqlite3 as sql
from typing import Any

from add_anki_cards.Db import DbConnect
from add_anki_cards.logging_main import get_logger
from add_anki_cards.PraticingEnglish.EnglishSaveCards import (
    AddDBSaveCards,
    ReadSaveCards,
)


def main_save_cards(
    new_cards: str,
    separator_cards: str,
    separetor_translate: str,
    language_cards: str = 'english',
    db: sql.Connection | sql.Cursor = DbConnect.db_connect(),
    logger: Any = get_logger(),
):
    """Func. principal da leitura do arquivo com as frases."""
    # variável que contem as linhas da página
    # com as frases e as traducoes separadas
    logger.info('Lendo as frases e traducoes')
    lista_pag_entrada = ReadSaveCards.reader(
        new_cards, separator_cards, separetor_translate
    )
    logger.info('Armazenando as frases e traducoes no banco de dados')
    AddDBSaveCards.armazena_sqlite(lista_pag_entrada, db, language_cards)
