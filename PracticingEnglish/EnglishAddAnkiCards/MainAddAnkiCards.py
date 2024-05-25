import pyautogui as auto
from time import sleep
import xerox
import sqlite3 as sql
import os.path as path


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

    def addClose(self):
        """
        Método que adicionas os cartões de inglês no cloze modo cloze
        com o áudio e a tradação separados em cloze diferentes
        """
        # dando tempo para o usuário clicar no campo do cartão do Anki
        sleep(5)
        # passamos pelo for loop que vai adicionar os cartões
        for frase_e_tradução in range(len(self.Tradução_frase)):
            # escrevemos a frase nele e já colocamos a frase dentro do cloze
            xerox.copy(f"Id: {self.Tradução_frase[frase_e_tradução][0]}\n" +
                       f"{{{{c1::{self.Tradução_frase[frase_e_tradução][1]}}}}}" +
                       " -> {{c1::")

            # colamos o a frase no cartão
            auto.hotkey("ctrl", "v")
            sleep(1)
            # entramos no audio tts
            auto.hotkey("ctrl", "t")
            sleep(1)
            # ecrevemos a frase que terá o áudio
            xerox.copy(self.Tradução_frase[frase_e_tradução][1])
            auto.hotkey("ctrl", "v")

            # vamos para o opção que cria o áudio
            for press in range(4):
                auto.press("tab")
            # confirmamos o audio
            auto.press("enter")
            sleep(3)
            # saimos e vamos para o final do cartão
            for press in range(3):
                auto.press("down")
            # colocamos a sinalização final do cloze
            xerox.copy("}}")
            sleep(2)
            auto.hotkey("ctrl", "v")

            # pulamos uma linha e damos um tab para facilitar a visualização
            auto.press("enter")
            auto.write("    ", 0.1)
            # ecrevendo a tradução
            xerox.copy(
                f"{{{{c2::{self.Tradução_frase[frase_e_tradução][2]}}}}}")
            auto.hotkey("ctrl", "v")

            # e criando o cartão
            auto.hotkey("ctrl", "enter")
            sleep(2)
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
