import json
import logging
import sqlite3 as sql
from datetime import datetime

import requests

from AddAnkiCards import logginMain
from AddAnkiCards.Db import DbConnect


class AddCardsMath(object):
    '''
    Classe que adiciona os cartoes de matematica no Anki
    '''

    def __init__(self,
                 IdTipoCard: int,
                 QuantCards: int,
                 nameDeck: str = 'MathTraining',
                 nameTag: str = 'MathTraining::Training',
                 logger: logging.getLogger = logginMain.get_logger(),
                 apiAnkiConnect: str = 'http://127.0.0.1:8765',
                 DbConnect: sql.connect = DbConnect.DbConnect(),
                 ) -> None:
        # Atributos do sistema
        self.logger = logger
        self.logger.debug('AddCardsMath Starting')  # Registrando
        self.apiAnkiConnect = apiAnkiConnect
        self.db = DbConnect
        #
        # Atributos dos cartoes
        self.nameDeck = nameDeck
        self.nameTag = nameTag
        self.idTipoCard = IdTipoCard
        self.cardsForAdd = self.db.cursor().execute(
            'SELECT Card, IdCard FROM CardsCalculoMental ' +
            f'WHERE (TipoCard = {IdTipoCard} AND DataPriRev = "-") ' +
            f'ORDER BY IdCard ASC LIMIT {QuantCards}').fetchall()
        #
        # Verifica se existe cards suficientes para a quantidade pedida
        if len(self.cardsForAdd) != QuantCards:
            raise Exception(f'Cards Insuficientes do tipo {IdTipoCard}')
        #
        #
        self.logger.debug('AddCardsMath Started')  # Registrando

    def addCards(self):
        '''
        Metodo que adciona os cards
        '''
        self.logger.debug('Enviando os cartoes para o Anki')  # registrando
        resultList = []
        for card in self.cardsForAdd:
            #
            #
            request = json.dumps(
                {
                    'action': 'addNote',
                    'params': {
                        'note': {
                            'deckName': self.nameDeck,
                            'modelName': 'cloze',
                            'fields': {'text': card[0], 'Back Extra': ''},
                            'options': {
                                'allowDuplicate': False,
                                'duplicateScope': 'deck',
                            },
                            'tags': [self.nameTag],
                        }
                    },
                    'version': 6,
                })
            #
            #
            result = requests.post(self.apiAnkiConnect, request)
            resultList.append([result.json(), card[0], card[1]])
            self.logger.info(
                f'O cartao: {card[0][:card[0].find('<p>')]}' +
                ' foi enviado ao Anki com sucesso')  # registrando
        self.updateDB()
        return resultList

    def updateDB(self):
        '''
        Metodo que atualiza o DB
        '''
        print('Update')
        self.logger.debug('Atualizando o Banco de Dados.')  # registrando
        #
        #
        dataPriRev = datetime.now().strftime('%Y-%m-%d')
        # Atualizando os dados dos cartoes que foram usados, atraves do tipo
        # e do id dentro do tipo
        self.db.execute('UPDATE CardsCalculoMental SET DataPriRev = ' +
                        f'\'{dataPriRev}\' WHERE (TipoCard = ' +
                        f'{self.idTipoCard} AND ' +
                        f'IdCard > {self.cardsForAdd[0][1]-1} AND ' +
                        f'IdCard < {self.cardsForAdd[-1][1]+1})')
        self.db.commit()


if __name__ == '__main__':
    AddCardsMath(1, 3).addCards()
