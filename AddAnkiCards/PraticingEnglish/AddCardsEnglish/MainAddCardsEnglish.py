import json
import logging
import os
import os.path as path
import sqlite3 as sql

import gtts
import requests

from AddAnkiCards import logginMain
from AddAnkiCards.Db import DbConnect

logger = logginMain.get_logger()


class AddCardsEnglish(object):
    """
    Classe que adiciona os cartoes nao usados no Anki e atualiza o DB
    """

    def __init__(
        self,
        num_cards: int,
        nameDeck: str = 'PraticingEnglish',
        nameTag: str = 'PraticingEnglish::Praticing',
        logger: logging.getLogger = logginMain.get_logger(),
        Db: sql.Connection = DbConnect.DbConnect(),
        apiAnkiConnect: str = 'http://127.0.0.1:8765',
    ) -> None:
        """
        Funcao que construi a classe já separando os textos e as traducoes
        """

        self.apiAnkiConnect = apiAnkiConnect
        self.conexaoDb = Db
        self.nameDeck = nameDeck
        self.nameTag = nameTag
        cursor = self.conexaoDb.cursor()
        self.logger = logger
        self.logger.debug('AddCardsEnglish Started')

        frases_geral_list = cursor.execute(
            'SELECT'
            + ' FraseId, FraseOrig,'
            + ' FraseTrad, TagLingua'
            + ' FROM FrasesNaoUsadas'
            + ' ORDER BY FraseId ASC LIMIT '
            + f'{num_cards}'
        ).fetchall()

        # Verificamos se existem frases o suficiente
        quantCardsRestante = (
            frases_geral_list[-1][0] - frases_geral_list[0][0] + 1
        )

        if num_cards > quantCardsRestante:
            # Carregando a mensagem de erro no self.
            self.logger.error(
                'Cartoes insuficientes: faltaram ' + f'{quantCardsRestante}'
            )
            self.traducoesFrases = 'Erro_Sem_Frases'
            return None

        self.traducoesFrases = frases_geral_list
        self.logger.info(
            'The phrases that will be added are ' + f'{self.traducoesFrases}'
        )
        cursor.close()

    def formatTextCardCloze(self, traducaoFrase: int = 0):
        """
        Metodo que formata os cartoes
        """
        return (
            f"""id: {self.traducoesFrases[traducaoFrase][0]}<br>
{{{{c2::{self.traducoesFrases[traducaoFrase][1]}}}}} ->"""
            + f""" {{{{c2::[sound:AddCardsAudio{self.traducoesFrases[
                traducaoFrase][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c1::{self.traducoesFrases[traducaoFrase][2]}}}}}
    </ul>
"""
        )

    def addCards(self):
        """
        Metodo que adiciona os cloze cartoes no modo cloze.
        """

        # Para adicionar os cartoes, passamos por cada um,
        # criamos e salvamos o audio, editamos o corpo do cartao
        # atraves de um pouco de HTML e jogamos isso na api que vai
        # adicionar o cartao de forma automatica
        resultCardList = []
        resultAudioList = []

        for traducaoFrase in range(len(self.traducoesFrases)):
            audio = gtts.gTTS(self.traducoesFrases[traducaoFrase][1])
            if not path.exists(path.join('.', 'collection.media')):
                os.makedirs(path.join('.', 'collection.media'))
            pathAudio = path.join(
                os.getcwd(),
                'collection.media',
                'AddCardsAudio'
                + f'{self.traducoesFrases[traducaoFrase][0]:0>6}.mp3',
            )
            audio.save(pathAudio)
            campoText = self.formatTextCardCloze(traducaoFrase)
            self.logger.info(f'campoText = {campoText}')
            requisisaoCard = {
                'action': 'addNote',
                'params': {
                    'note': {
                        'deckName': f'{self.nameDeck}',
                        'modelName': 'cloze',
                        'fields': {'text': campoText, 'Back Extra': ''},
                        'options': {
                            'allowDuplicate': False,
                            'duplicateScope': 'deck',
                        },
                        'tags': [f'{self.nameTag}'],
                    }
                },
                'version': 6,
            }
            requisisaoAudio = {
                'action': 'storeMediaFile',
                'params': {
                    'path': pathAudio,
                    "filename": (
                        'AddCardsAudio'
                        + f'{self.traducoesFrases[traducaoFrase][0]:0>6}.mp3'),
                },
                'version': 5,
            }
            self.logger.info(f'The request is {requisisaoCard}')
            requisisaoCard = json.dumps(requisisaoCard)
            requisisaoAudio = json.dumps(requisisaoAudio)
            resultCard = requests.post(self.apiAnkiConnect, requisisaoCard)
            resultAudio = requests.post(self.apiAnkiConnect, requisisaoAudio)

            # Finalmente mostramos o codigo do resultCardado da api, verifcamos
            # se houve um erro (paramos o programa e relatamos no terminal,
            # se esse for o caso).

            resultCard = resultCard.json()
            resultAudio = resultAudio.json()
            resultCardList.append(resultCard)
            resultAudioList.append(resultAudio)
            if resultCard['error'] is not None:
                self.logger.error(f"Error API AnkiConnect: {
                                  resultCard['error']}")
                return resultCardList
            elif resultAudio['error'] is not None:
                self.logger.error(f"Error API AnkiConnect:{
                                  resultAudio['error']}")
                return resultAudioList
            self.logger.debug(
                'Phrases with id '
                + f'= {self.traducoesFrases[traducaoFrase][0]} '
                + 'have been added in Anki'
            )
        self.updateDB()  # E atualizamos o DB
        print(resultCardList)
        return resultCardList

    def updateDB(self):
        """
        Metodo que atualiza o banco de dados do programa
        """
        conexaoDb = self.conexaoDb
        cursor = conexaoDb.cursor()

        for frase in self.traducoesFrases:

            # Colocamos ela no banco de dados das frases usadas
            cursor.execute(
                'INSERT INTO FrasesUsadas '
                + '(FraseId, FraseOrig, FraseTrad, TagLingua)'
                + 'VALUES ('
                + f'{frase[0]}, "{frase[1]}", "{frase[2]}",'
                f'"{frase[3]}")'
            )
            # A retiramos do DB das nao usadas
            cursor.execute(
                'DELETE FROM FrasesNaoUsadas WHERE' + f' FraseId = {frase[0]}'
            )

        # salvamos o que foi feito e encerramos a conexao
        self.logger.debug('The database has been updated')
        conexaoDb.commit()
        cursor.close()
        conexaoDb.close()
        self.conexaoDb.close()
