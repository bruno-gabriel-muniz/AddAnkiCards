import sqlite3 as sql
import os.path as path
import os
import requests
import json
from time import sleep
import gtts


class AddAnkiCards():
    """
    Classe que adiciona os cartões não usados no Anki e atualiza o DB
    """

    def __init__(self, num_cards, Tipo_cards):
        """
        Funcao que construi a classe já separando os textos e as traducoes
        """
        # lemos o tipo dos cartoes
        self.Tipo_cards = Tipo_cards
        # Lemos o nome do DB
        self.DBName = ("GeneralDB.db")
        # Abrimos o DB que contem as frases
        conexaoDb = sql.connect(self.DBName)
        cursor = conexaoDb.cursor()

        # Depois, lemos as proximas frases a serem adcionadas
        frases_geral_list = cursor.execute("SELECT" +
                                           " FraseId, FraseOrig," +
                                           " FraseTrad, TagLingua" +
                                           " FROM FrasesNaoUsadas" +
                                           " ORDER BY FraseId ASC LIMIT " +
                                           f"{num_cards}"
                                           ).fetchall()

        # Verificamos se existem frases o suficiente
        if num_cards > frases_geral_list[-1][0] - frases_geral_list[0][0] + 1:
            # caso nao haja frases o suficientes retornamos nada
            # e informamos ao resto do programa
            self.Tradução_frase = "Erro_Sem_Frases"
            return None
        # E caso tenha frases o suficiente as adcionamos nos dados da classe
        self.Tradução_frase = frases_geral_list

        # Finalmente, fechamos a conexão com o DB
        cursor.close()
        conexaoDb.close()

    def addCloze(self):
        """
        Método que adiciona os cloze cartões no modo cloze
        """
        # Para adicionar os cartões, passamos por cada um,
        # criamos e salvamos o audio, editamos o corpo do cartao
        # atraves de um pouco de HTML e jogamos isso na api que vai
        # adicionar o cartão de forma automatica
        for fraseETraducao in range(len(self.Tradução_frase)):
            audio = gtts.gTTS(self.Tradução_frase[fraseETraducao][1])

            audio.save(path.join("/home", f"{os.environ["USERNAME"]}",
                                 ".local", "share", "Anki2", "Usuário 1",
                                 "collection.media", "AddCardsAudio" +
                                 f"{self.Tradução_frase[fraseETraducao][
                                     0]:0>6}.mp3"))
            campoText = (f'id: {self.Tradução_frase[fraseETraducao][0]}<br>' +
                         "{{" + f"c1::{self.Tradução_frase[fraseETraducao][1]}"
                         + "}} -> {{c1::[sound:AddCardsAudio" +
                         f"{self.Tradução_frase[fraseETraducao][0]:0>6}" +
                         ".mp3]}}<br><ul>{{" +
                         f"c2::{self.Tradução_frase[fraseETraducao][2]}" +
                         "}}</ul>")

            requisisao = {'action': "addNote",
                          'params':
                              {
                                  "note":
                                  {
                                      "deckName": "conhecimentos::3.inglês New f::3. inglês new f 4",
                                      "modelName": "cloze",
                                      "fields":
                                      {
                                          "text": campoText,
                                          "Back Extra": ""
                                      },
                                      "options": {
                                          "allowDuplicate": False,
                                          "duplicateScope": "deck"
                                      },
                                      "tags": [
                                          "Linguas::inglês::ler_e_falar::1.0"
                                      ]
                                  }
                              },
                              'version': 6}
            requisisao = json.dumps(requisisao)
            resultado = requests.post('http://127.0.0.1:8765', requisisao)

            # Finalmente mostramos o codigo do resultado da api, verifcamos
            # se houve um erro (paramos o programa e relatamos no terminal,
            # se esse for o caso).
            print(resultado)
            resultado = resultado.json()
            if resultado['error'] != None:
                print(resultado)
                return None
        # E e atualizamos o DB
        self.atualizaDB()

    def atualizaDB(self):
        """
        Método que atualiza o banco de dados do programa 
        """
        # Conectamos com o DB do programa
        conexaoDb = sql.connect(self.DBName)
        cursor = conexaoDb.cursor()

        # Passamos por cada frase que será atualizada
        for frase in self.Tradução_frase:

            # Colocamos ela no banco de dados das frases usadas
            cursor.execute("INSERT INTO FrasesUsadas " +
                           "(FraseId, FraseOrig, FraseTrad, TagLingua)" +
                           "VALUES (" +
                           f"{frase[0]}, \"{frase[1]}\", \"{frase[2]}\", \"{frase[3]}\")")
            # A retiramos do DB das não usadas
            cursor.execute("DELETE FROM FrasesNaoUsadas WHERE" +
                           f" FraseId = {frase[0]}")

        # salvamos o que foi feito e encerramos a conexão
        conexaoDb.commit()
        cursor.close()
        conexaoDb.close()


Test = AddAnkiCards(3, "cloze")
Test.addCloze()
