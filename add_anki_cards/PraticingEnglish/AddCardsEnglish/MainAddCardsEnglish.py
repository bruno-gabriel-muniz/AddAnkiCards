import json
import sqlite3 as sql
from logging import Logger
from os import makedirs, path

import requests
from gtts import gTTS

from add_anki_cards import logging_main
from add_anki_cards.Db import DbConnect

logger = logging_main.get_logger()


class AddCardsEnglish:
    """Classe que adiciona os cartoes nao usados no Anki e atualiza o DB."""

    def __init__(
        self,
        num_cards: int,
        name_deck: str = 'PraticingEnglish',
        name_tag: str = 'PraticingEnglish::Praticing',
        user: str = 'User_Default',
        logger: Logger = logging_main.get_logger(),
        db: sql.Connection | sql.Cursor = DbConnect.db_connect(),
        api_anki_connect: str = 'http://127.0.0.1:8765',
    ) -> None:
        """Func. q constrói a classe já separando os textos e as traducoes."""

        self.user = user
        self.logger = logger
        self.logger.info('AddCardsEnglish Iniciado')
        self.api_anki_connect = api_anki_connect
        self.db = db
        self.name_deck = name_deck
        self.name_tag = name_tag
        cursor = self.db.cursor()

        frases_geral_list = cursor.execute(
            'SELECT'
            + ' FraseId, FraseOrig,'
            + ' FraseTrad, TagLingua'
            + ' FROM FrasesNaoUsadas'
            + ' ORDER BY FraseId ASC LIMIT '
            + f'{num_cards}'
        ).fetchall()

        # Verificamos se existem frases o suficiente
        quant_cards_restante = (
            frases_geral_list[-1][0] - frases_geral_list[0][0] + 1
        )

        if num_cards > quant_cards_restante:
            # Carregando a mensagem de erro no self.logger
            self.logger.warning(
                'Cartoes insuficientes: faltaram ' + f'{quant_cards_restante}'
            )
            self.traducoes_frases = 'Erro_Sem_Frases'
            return None

        self.traducoes_frases = frases_geral_list
        self.logger.info(
            'Cartões que serão adicionados: ' + f'{self.traducoes_frases}'
        )
        cursor.close()
        return None

    def format_text_card_cloze(self, traducao_frase: int = 0):
        """Metodo que formata os cartoes."""
        self.logger.info(f'Formatando o cartão {traducao_frase}')
        return (
            f"""id: {self.traducoes_frases[traducao_frase][0]}<br>
{{{{c2::{self.traducoes_frases[traducao_frase][1]}}}}} ->"""
            + f""" {{{{c2::[sound:AddCardsAudio{self.traducoes_frases[
                traducao_frase][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c1::{self.traducoes_frases[traducao_frase][2]}}}}}
    </ul>
"""
        )

    def add_cards(self):
        """Metodo que adiciona os cloze cartoes no modo cloze."""

        # Para adicionar os cartoes, passamos por cada um,
        # criamos e salvamos o audio, editamos o corpo do cartao
        # atraves de um pouco de HTML e jogamos isso na api que vai
        # adicionar o cartao de forma automatica
        self.logger.info(f'Adicionando os cartões {self.traducoes_frases}')
        result_card_list = []
        result_audio_list = []

        for idx, traducao_frase in enumerate(self.traducoes_frases):
            self.logger.info(f'Adicionando o cartão {traducao_frase}')
            self.logger.info('Criando o audio')
            audio = gTTS(traducao_frase[1])
            home_path = path.expanduser('~')
            colection_media = path.join(
                home_path,
                '.AddAnkiCardsData',
                self.user,
                'collection.media',
            )
            if not path.exists(colection_media):
                makedirs(colection_media)
            path_audio = path.join(
                colection_media,
                f'AddCardsAudio{traducao_frase[0]:0>6}.mp3',
            )
            audio.save(path_audio)
            self.logger.info('Formatando o texto')
            campo_text = self.format_text_card_cloze(idx)
            self.logger.info(f'Campo Texto = {campo_text}')
            self.logger.info('Fazendo a requisicao para o Anki')
            requisisao_card = {
                'action': 'addNote',
                'params': {
                    'note': {
                        'deckName': f'{self.name_deck}',
                        'modelName': 'cloze',
                        'fields': {'text': campo_text, 'Back Extra': ''},
                        'options': {
                            'allowDuplicate': False,
                            'duplicateScope': 'deck',
                        },
                        'tags': [f'{self.name_tag}'],
                    }
                },
                'version': 6,
            }
            requisisao_audio = {
                'action': 'storeMediaFile',
                'params': {
                    'path': path_audio,
                    'filename': (
                        'AddCardsAudio' + f'{traducao_frase[0]:0>6}.mp3'
                    ),
                },
                'version': 5,
            }
            self.logger.info(f'Requisicao = {requisisao_card}')
            requisisao_card = json.dumps(requisisao_card)
            requisisao_audio = json.dumps(requisisao_audio)
            result_card = requests.post(
                self.api_anki_connect, requisisao_card, timeout=10
            )
            result_audio = requests.post(
                self.api_anki_connect, requisisao_audio, timeout=10
            )

            # Finalmente mostramos o codigo do resultCardado da api, verifcamos
            # se houve um erro (paramos o programa e relatamos no terminal,
            # se esse for o caso).
            self.logger.info('Analisando a presença de erros')
            result_card = result_card.json()
            result_audio = result_audio.json()
            result_card_list.append(result_card)
            result_audio_list.append(result_audio)
            if result_card['error'] is not None:
                self.logger.error(
                    f"Error API AnkiConnect: {result_card['error']}"
                )
                return result_card_list
            if result_audio['error'] is not None:
                self.logger.error(
                    f"Error API AnkiConnect:{result_audio['error']}"
                )
                return result_audio_list
            self.logger.info(
                f'Frases com id = {traducao_frase[0]} ' + 'adicionadas no Anki'
            )
        self.logger.info('Atualizando o DB')
        self.update_db()  # E atualizamos o DB
        self.logger.info(f'Resultados = {result_card_list}')
        return result_card_list

    def update_db(self):
        """Metodo que atualiza o banco de dados do programa."""
        cursor = self.db.cursor()

        for frase in self.traducoes_frases:

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
        self.db.commit()
        cursor.close()
        self.logger.info('Banco de dados atualizado com sucesso')
