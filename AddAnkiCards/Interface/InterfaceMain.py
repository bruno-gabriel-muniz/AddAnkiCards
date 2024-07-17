import customtkinter as ctk

from AddAnkiCards.Db import DbConnect, DbSearch
from AddAnkiCards.logginMain import get_logger
from AddAnkiCards.PraticingEnglish.EnglishSaveCards import MainSaveCards

MainSaveCards


class WindowMain(object):
    def __init__(
        self, dbConnect=DbConnect.DbConnect(), Logger=get_logger()
    ) -> None:
        """
        Classe que representa as janelas do programa.
        """
        #
        # Iniciamos a janela
        self.Master = ctk.CTk()
        self.Master.resizable(0, 0)
        #
        # Definimos a cor do tema e o titulo
        self.Master.title('Add Anki Cards')
        self.colorTheme = '#009951'
        #
        # Fazemos o titulo da parte do ingles
        self.LabelEnglish = ctk.CTkLabel(
            self.Master, text='English', font=('Arial', 30)
        )
        self.LabelEnglish.grid(row=0, column=0, columns=2, padx=5, pady=5)
        #
        # Coletamos os dados dos cartoes e mostramos na janela
        DbSearched = DbSearch.DbResearcher(dbConnect)
        (
            AddedNotesEnglish,
            StoredNotesEnglish,
            AllNotesEnglish,
        ) = DbSearched.countNotesOfEnglish()
        InfoEnglish = [
            f'Added Notes: {AddedNotesEnglish}',
            f'Stored Notes: {StoredNotesEnglish}',
            f'All Notes: {AllNotesEnglish}',
        ]
        self.labelEnglishInfo = ctk.CTkLabel(
            self.Master,
            text=f'{InfoEnglish[0]:>} | '
            + f'{InfoEnglish[1]:<}\n{InfoEnglish[2]:^}',
        )
        self.labelEnglishInfo.grid(row=1, column=0, columns=2, padx=5, pady=5)
        #
        # Fazemos os botoes que vao adicionar e fazer os cartoes de ingles
        self.btnEnglishAdd = ctk.CTkButton(
            self.Master,
            height=70,
            text='Add Cards',
            fg_color=self.colorTheme,
        )
        self.btnEnglishAdd.grid(row=2, column=0, padx=5, pady=5)
        #
        #
        self.btnEnglishMake = ctk.CTkButton(
            self.Master,
            command=self.makeWinMakeEnglish,
            height=70,
            text='Make Cards',
            fg_color=self.colorTheme,
        )
        self.btnEnglishMake.grid(row=2, column=1, padx=5, pady=5)
        #
        # Fazemos a divisoria
        ctk.CTkCanvas(self.Master, height=0, width=300).grid(
            row=3, column=0, columns=2, pady=5
        )
        #
        # E fazemos a mesma coisa para as opcoes e informacoes de informatica
        self.LabelMath = ctk.CTkLabel(
            self.Master, text='Math', font=('Arial', 30)
        )  # titulo
        self.LabelMath.grid(row=4, column=0, columns=2, padx=5, pady=5)
        #
        # Informacoes
        (
            AddedCardsMath,
            StoredCardsMath,
            AllCardsMath,
        ) = DbSearched.countCardsOfMath()
        InfoMath = [
            f'Added Cards: {AddedCardsMath}',
            f'Stored Cards: {StoredCardsMath}',
            f'All Cards: {AllCardsMath}',
        ]
        self.labelMathInfo = ctk.CTkLabel(
            self.Master,
            text=f'{InfoMath[0]:>} | ' + f'{InfoMath[1]:<}\n{InfoMath[2]:^}',
        )
        self.labelMathInfo.grid(row=5, column=0, columns=2, padx=5, pady=5)
        #
        # Botoes
        self.btnMathAdd = ctk.CTkButton(
            self.Master,
            height=70,
            text='Add Cards',
            fg_color=self.colorTheme,
        )
        self.btnMathAdd.grid(row=6, column=0, padx=5, pady=5)
        #
        #
        self.btnMathMake = ctk.CTkButton(
            self.Master, height=70, text='Make Cards', fg_color=self.colorTheme
        )
        self.btnMathMake.grid(row=6, column=1, padx=5, pady=5)
        self.Master.mainloop()

    def makeWinMakeEnglish(self):
        WinMakeEnglish(self.Master, self.colorTheme)


class WinMakeEnglish(object):
    def __init__(self, nameMaster, colorTheme) -> None:
        #
        # Iniciamos a janela
        self.colorTheme = colorTheme
        self.window = ctk.CTkToplevel(nameMaster)
        self.window.title('Make Cards English')
        #
        # Criamos os label que irao informar o usuario
        self.labelCardSeparetor = ctk.CTkLabel(
            self.window, font=('Arial', 15), text='Cards Separetor'
        )
        self.labelCardSeparetor.grid(row=0, column=0, padx=5, pady=5)
        self.labelTranslationSeparetor = ctk.CTkLabel(
            self.window, font=('Arial', 15), text='Translation Separetor'
        )
        self.labelTranslationSeparetor.grid(row=0, column=1, padx=5, pady=5)
        #
        # Criamos a entrada dos separadores
        self.cardSeparetor = ctk.CTkEntry(self.window, placeholder_text='|')
        self.valueCardSeparetor = '|'
        self.cardSeparetor.grid(row=1, column=0, padx=5, pady=5)
        self.translationSeparetor = ctk.CTkEntry(
            self.window, placeholder_text=';'
        )
        self.valueTranslationSeparetor = ';'
        self.translationSeparetor.grid(row=1, column=1, padx=5, pady=5)
        #
        # Criamos a caixa de texto para informa os status dos
        # novos cartoes e botao que os cria
        self.labelInfoCards = ctk.CTkLabel(  # informacoes
            self.window,
            font=('Arial', 15),
            text_color=self.colorTheme,
            text='No Added',
        )
        self.labelInfoCards.grid(row=2, column=0, padx=5, pady=5)
        self.btnMakeCards = ctk.CTkButton(  # o botao
            self.window,
            command=self.makeCards,
            text='Make Cards',
            fg_color=self.colorTheme,
        )
        self.btnMakeCards.grid(row=2, column=1, pady=5, padx=5)
        # a caixa de texto
        self.TextCards = ctk.CTkTextbox(self.window, 300, 200)
        self.TextCards.grid(row=3, column=0, columns=2)
        #
        # e rodamos a janela
        self.window.mainloop()

    def makeCards(self):
        if self.cardSeparetor.get() != '':
            self.valueCardSeparetor = self.cardSeparetor.get()
        if self.translationSeparetor.get() != '':
            self.valueTranslationSeparetor = self.translationSeparetor.get()

        MainSaveCards.mainSaveCards(
            self.TextCards.get('0.0', 'end'),
            self.valueCardSeparetor,
            self.valueTranslationSeparetor,
            'english',
        )
        self.labelInfoCards.config(text='Added')


if __name__ == '__main__':
    WindowMain()
