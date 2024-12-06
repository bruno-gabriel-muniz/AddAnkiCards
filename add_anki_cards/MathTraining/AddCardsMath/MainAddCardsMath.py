import json
import sqlite3 as sql
from datetime import datetime
from typing import Any

import requests

from add_anki_cards import logging_main
from add_anki_cards.Db import DbConnect


class AddCardsMath():
    """Class que adiciona os cartoes de matematica no Anki."""

    def __init__(
        self,
        id_tipo_card: int,
        quant_notes: int,
        name_deck: str = 'MathTraining',
        name_tag: str = 'MathTraining::Training',
        db: sql.Connection | sql.Cursor = DbConnect.db_connect(),
        logger: Any = logging_main.get_logger(),
        api_anki_connect: str = 'http://127.0.0.1:8765',
    ) -> None:
        """Metodo construtor da classe."""
        # Atributos do sistema
        self.logger = logger
        self.logger.debug('AddCardsMath Starting')  # Registrando
        self.api_anki_connect = api_anki_connect
        self.db = db
        self.cursor = db.cursor()
        #
        # Atributos dos cartoes
        self.name_deck = name_deck
        self.name_tag = name_tag
        self.id_tipo_card = id_tipo_card
        self.cards_for_add = self.cursor.execute(
            'SELECT Card, IdCard FROM CardsCalculoMental ' +
            f'WHERE (TipoCard = {id_tipo_card} AND DataPriRev = "-") ' +
            f'ORDER BY IdCard ASC LIMIT {quant_notes}').fetchall()
        self.quant_notes = quant_notes
        #
        # Verifica se existe cards suficientes para a quantidade pedida
        if len(self.cards_for_add) != self.quant_notes:
            self.logger.info(
                "O usuário tentou add cards indisponíveis." +
                "-" * 80 + "\n" +
                f"Data:\nNotas encontrados:{self.cards_for_add}\n" +
                "-" * 80 + "\n" +
                f"Quant de notas req: {self.quant_notes}")
            raise ValueError(
                f'Cards Insuficientes do tipo {id_tipo_card}'
                + ' ou tipo inexistente.\n'
                + f'quant_notes_free_of_type: {len(self.cards_for_add)},'
                + f' quant_notes_requested_of_type: {self.quant_notes}'
            )
        #
        #
        self.logger.debug('AddCardsMath Started')  # Registrando

    def add_cards(self):
        """Metodo que adciona os cards para o Anki."""
        self.logger.debug('Enviando os cartoes para o Anki')  # registrando
        result_list = []
        for card in self.cards_for_add:
            #
            #
            request = json.dumps(
                {
                    'action': 'addNote',
                    'params': {
                        'note': {
                            'deckName': self.name_deck,
                            'modelName': 'cloze (Hide all)',
                            'fields': {'text': card[0],
                                       'Back Extra': '',
                                       'Hide others on the back side': '1'},
                            'options': {
                                'allowDuplicate': False,
                                'duplicateScope': 'deck',
                            },
                            'tags': [self.name_tag],
                        }
                    },
                    'version': 6,
                })
            #
            #
            result = requests.post(self.api_anki_connect, request, timeout=10)
            result_list.append([result.json(), card[0], card[1]])
            self.logger.info(
                f'O cartao: {card[0][:card[0].find('<p>')]}' +
                ' foi enviado ao Anki com sucesso')  # registrando
        self.update_db()
        return result_list

    def update_db(self):
        """Met. que atualiza o DB."""
        self.logger.debug('Atualizando o Banco de Dados.')  # registrando
        #
        #
        data_pri_rev = datetime.now().strftime('%Y-%m-%d')
        # Atualizando os dados dos cartoes que foram usados, atraves do tipo
        # e do id dentro do tipo
        self.cursor.execute(
            'UPDATE CardsCalculoMental SET DataPriRev = ' +
            f'\'{data_pri_rev}\' WHERE (TipoCard = ' +
            f'{self.id_tipo_card} AND ' +
            f'IdCard > {self.cards_for_add[0][1]-1} AND ' +
            f'IdCard < {self.cards_for_add[-1][1]+1})'
        )
        num_notes_free = self.cursor.execute(
            'SELECT NumNotesFree FROM TipoCardsCalculoMental ' +
            f'WHERE IdTipo = {self.id_tipo_card}'
        ).fetchall()[0][0]
        new_num_notes_free = num_notes_free - self.quant_notes
        self.cursor.execute('UPDATE TipoCardsCalculoMental ' +
                            f'SET NumNotesFree={new_num_notes_free} ' +
                            f'WHERE IdTipo = {self.id_tipo_card}')
        self.db.commit()
        self.cursor.close()


if __name__ == '__main__':
    AddCardsMath(1, 3).add_cards()
