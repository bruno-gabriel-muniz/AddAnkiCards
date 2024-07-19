import customtkinter as ctk

from AddAnkiCards.Db import DbConnect, DbSearch
from AddAnkiCards.logginMain import get_logger
from AddAnkiCards.PraticingEnglish.AddCardsEnglish import MainAddCardsEnglish
from AddAnkiCards.PraticingEnglish.EnglishSaveCards import MainSaveCards

MainSaveCards


class WindowMain(object):
    def __init__(
        self, dbConnect=DbConnect.DbConnect(), Logger=get_logger()
    ) -> None:
        """
        Classe que representa as janelas do programa.
        """
        self.Db = dbConnect
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
        self.DbSearched = DbSearch.DbResearcher(self.Db)
        self.InfoEnglish = list(self.DbSearched.countNotesOfEnglish())
        self.InfoEnglish = [
            f'Added Notes: {self.InfoEnglish[0]}',
            f'Stored Notes: {self.InfoEnglish[1]}',
            f'All Notes: {self.InfoEnglish[2]}',
        ]
        self.labelEnglishInfo = ctk.CTkLabel(
            self.Master,
            text=f'{self.InfoEnglish[0]:>} | '
            + f'{self.InfoEnglish[1]:<}\n{self.InfoEnglish[2]:^}',
        )
        self.labelEnglishInfo.grid(row=1, column=0, columns=2, padx=5, pady=5)
        #
        # Fazemos os botoes que vao adicionar e fazer os cartoes de ingles
        self.btnEnglishAdd = ctk.CTkButton(
            self.Master,
            height=70,
            command=self.makeWinAddCardsEnglish,
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
        self.InfoMath = list(self.DbSearched.countCardsOfMath())
        self.InfoMath = [
            f'Added Cards: {self.InfoMath[0]}',
            f'Stored Cards: {self.InfoMath[1]}',
            f'All Cards: {self.InfoMath[2]}',
        ]
        self.labelMathInfo = ctk.CTkLabel(
            self.Master,
            text=f'{self.InfoMath[0]:>} | '
            + f'{self.InfoMath[1]:<}\n{self.InfoMath[2]:^}',
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
        #
        # funcao que roda e atualiza a janeal principal
        self.updateInformation()
        self.Master.mainloop()

    def updateInformation(self):
        """
        Atualiza as informações da janela principal
        """
        #
        # atualizamos as informacoes de ingles
        self.InfoEnglish = list(self.DbSearched.countNotesOfEnglish())
        self.InfoEnglish = [
            f'Added Notes: {self.InfoEnglish[0]}',
            f'Stored Notes: {self.InfoEnglish[1]}',
            f'All Notes: {self.InfoEnglish[2]}',
        ]
        self.labelEnglishInfo.configure(
            text=f'{self.InfoEnglish[0]:>} | '
            + f'{self.InfoEnglish[1]:<}\n{self.InfoEnglish[2]:^}'
        )
        #
        # atualizamos as informacoes de matematica
        self.InfoMath = list(self.DbSearched.countCardsOfMath())
        self.InfoMath = [
            f'Added Cards: {self.InfoMath[0]}',
            f'Stored Cards: {self.InfoMath[1]}',
            f'All Cards: {self.InfoMath[2]}',
        ]
        self.labelMathInfo.configure(
            text=f'{self.InfoMath[0]:>} | '
            + f'{self.InfoMath[1]:<}\n{self.InfoMath[2]:^}'
        )

        self.Master.after(5000, self.updateInformation)

    def makeWinMakeEnglish(self):
        """
        Funcao que inicia a janela que faz/salva os cards de ingles
        """
        WinMakeEnglish(self.Master, self.colorTheme)

    def makeWinAddCardsEnglish(self):
        """
        Metodo que cria a janela que adciona os cartoes de ingles no anki.
        """
        WinAddCardsEnglish(
            self.Master, self.colorTheme, self.InfoEnglish, self.DbSearched
        )


class WinMakeEnglish(object):
    def __init__(self, master, colorTheme) -> None:
        #
        # Iniciamos a janela
        self.colorTheme = colorTheme
        self.master = master
        self.window = ctk.CTkToplevel(master)
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
        """
        Funcao que faz os cartoes de ingles e os adciona no DB.
        """
        # verificamos se os separador sao os padroes
        if self.cardSeparetor.get() != '':
            self.valueCardSeparetor = self.cardSeparetor.get()
        if self.translationSeparetor.get() != '':
            self.valueTranslationSeparetor = self.translationSeparetor.get()
        # salvamos os cartoes
        MainSaveCards.mainSaveCards(
            self.TextCards.get('0.0', 'end'),
            self.valueCardSeparetor,
            self.valueTranslationSeparetor,
            'english',
            Db=DbConnect.DbConnect(),
        )
        # atualizamos as informacoes
        self.labelInfoCards.configure(text='Added')
        # mostramos o botao para reinicializar a janela
        # e dessa forma permir a criacao de mais cartoes
        self.btnRestart = ctk.CTkButton(
            self.window,
            width=280,
            text='Restart for add more cards',
            command=self.restart,
            fg_color=self.colorTheme,
        )
        self.btnRestart.grid(row=4, column=0, columns=2)

    def restart(self):
        """
        Funcao que reinicializa a janela WinMakeEnglish
        """
        self.window.destroy()
        WinMakeEnglish(self.master, self.colorTheme)


class WinAddCardsEnglish(object):
    def __init__(
        self, master: str, colorTheme: str, InfoEnglish: list, DbSearched
    ) -> None:
        #
        # Iniciamos os meta-dados da janela,
        self.DbSearched = DbSearched
        self.colorTheme = colorTheme
        self.InfoEnglish = InfoEnglish
        #
        # A janela,
        self.window = ctk.CTkToplevel(master)
        self.window.title('Add English Cards')
        #
        # Mostramos as informacoes dos cartoes,
        self.labelInfoCards = ctk.CTkLabel(
            self.window,
            text=f'{self.InfoEnglish[0]:>} | {self.InfoEnglish[1]:<}'
            + f'\n{self.InfoEnglish[2]:^}',
        )
        self.labelInfoCards.grid(row=0, column=0, columns=2, padx=5, pady=5)
        #
        # O campo de insercao da quantidade dos cartoes
        self.quantCards = ctk.CTkEntry(
            self.window, placeholder_text='Num. of cards'
        )
        self.quantCards.grid(row=1, column=0, padx=5, pady=5)
        #
        # E o botao para adiciona-los no Anki
        self.btnAddCards = ctk.CTkButton(
            master=self.window,
            text='Add Cards',
            command=self.AddCards,
            fg_color=self.colorTheme,
        )
        self.btnAddCards.grid(row=1, column=1, padx=5, pady=5)
        #
        # E rodamos a janela
        self.window.mainloop()

    def AddCards(self):
        """
        Funcao que aciona o back-end para fazer os cartoes de ingles
        """
        #
        # Primeiro, chamamos a funcao do back end.
        MainAddCardsEnglish.AddCardsEnglish(
            int(self.quantCards.get()), Db=DbConnect.DbConnect()
        ).addCards()
        #
        # Depois atualizamos as informacoes da janela.
        self.InfoEnglish = list(self.DbSearched.countNotesOfEnglish())
        self.InfoEnglish = [
            f'Added Notes: {self.InfoEnglish[0]}',
            f'Stored Notes: {self.InfoEnglish[1]}',
            f'All Notes: {self.InfoEnglish[2]}',
        ]
        self.labelInfoCards.configure(
            text=f'{self.InfoEnglish[0]:>} | {self.InfoEnglish[1]:<}'
            + f'\n{self.InfoEnglish[2]:^}'
        )


if __name__ == '__main__':
    WindowMain()
