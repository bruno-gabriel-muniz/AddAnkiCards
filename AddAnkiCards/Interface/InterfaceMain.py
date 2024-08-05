import customtkinter as ctk

from AddAnkiCards.Db import DbConnect, DbSearch
from AddAnkiCards.logginMain import get_logger
from AddAnkiCards.MathTraining.MakeCardsMath import MainMakeCards
from AddAnkiCards.PraticingEnglish.AddCardsEnglish import MainAddCardsEnglish
from AddAnkiCards.PraticingEnglish.EnglishSaveCards import MainSaveCards


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
        # E fazemos a mesma coisa para as opcoes e informacoes da matematica
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
            self.Master,
            height=70,
            text='Make Cards',
            command=self.makeWinMakeMath,
            fg_color=self.colorTheme,
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

    def makeWinMakeMath(self):
        WinMakeMath(self.Master, self.colorTheme)

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
            self.window, placeholder_text='Num. of Cards'
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


class WinMakeMath(object):
    def __init__(self, master, colorTheme) -> None:
        #
        # Informacoes da janela.
        self.master = master
        self.colorTheme = colorTheme
        self.varOneOrTwoRange = 'One Range'
        self.cardsWasMaked = False
        self.countTimeForShowAddedForUser = 0
        #
        # configuracoes iniciais
        self.window = ctk.CTkToplevel(self.master)
        self.window.title('Make Math Cards')
        #
        # Abas da entrada dos intervalos
        self.tabIntervalos = ctk.CTkTabview(
            self.window,
            height=100,
        )
        self.tabIntervalos.grid(row=0, column=0, columns=2)
        self.tab1Intervalo = self.tabIntervalos.add('One Range')
        self.tab2Intervalos = self.tabIntervalos.add('Two Ranges')
        #
        # Configuracoes da primeira
        self.label1IntervaloStart = ctk.CTkLabel(
            self.tab1Intervalo, text='Start of Range'
        )
        self.label1IntervaloStart.grid(row=0, column=0, padx=5)
        #
        self.entry1IntervaloStart = ctk.CTkEntry(
            self.tab1Intervalo, placeholder_text='"1" if range is 1 to 10'
        )
        self.entry1IntervaloStart.grid(row=1, column=0, padx=5)
        #
        self.label1IntervaloEnd = ctk.CTkLabel(
            self.tab1Intervalo, text='End of Range'
        )
        self.label1IntervaloEnd.grid(row=0, column=1, padx=5)
        #
        self.entry1IntervaloEnd = ctk.CTkEntry(
            self.tab1Intervalo, placeholder_text='"10" if range is 1 to 10'
        )
        self.entry1IntervaloEnd.grid(row=1, column=1, padx=5)
        #
        # Configuracoes da segunda aba
        self.label2IntervalosRange1 = ctk.CTkLabel(
            self.tab2Intervalos, text='First Range'
        )
        self.label2IntervalosRange1.grid(row=0, column=0, padx=5)
        #
        self.entry2IntervalosRange1 = ctk.CTkEntry(
            self.tab2Intervalos, placeholder_text='"1 9" if range is 1 to 9'
        )
        self.entry2IntervalosRange1.grid(row=1, column=0, padx=5)
        #
        self.label2IntervalosRange2 = ctk.CTkLabel(
            self.tab2Intervalos, text='Second Range'
        )
        self.label2IntervalosRange2.grid(row=0, column=1, padx=5)
        #
        self.entry2IntervalosRange2 = ctk.CTkEntry(
            self.tab2Intervalos,
            placeholder_text='"10 99" if range is 10 to 99',
        )
        self.entry2IntervalosRange2.grid(row=1, column=1, padx=5)
        #
        # Entrada do tipo da operacao e a quantidade maxima de cards por nota
        self.labelTypeOperationMath = ctk.CTkLabel(
            self.window, text='Type of Operetion'
        )
        self.labelTypeOperationMath.grid(row=1, column=0, padx=5)
        self.typeOperationMath = ctk.CTkOptionMenu(
            self.window,
            values=['sum', 'sub', 'mul', 'div'],
            fg_color=self.colorTheme,
        )
        self.typeOperationMath.grid(row=2, column=0, padx=5)
        #
        self.labelNumMaxCards = ctk.CTkLabel(
            self.window, text='Max. Num. Cards Per Note'
        )
        self.labelNumMaxCards.grid(row=1, column=1, padx=5)
        self.entryNumMaxCards = ctk.CTkEntry(self.window)
        self.entryNumMaxCards.grid(row=2, column=1, padx=5)
        #
        # Numero de notas que serao cridas, o botao que as cria e a
        # quantidade de cards esperados
        self.LabelNumOfNotes = ctk.CTkLabel(
            self.window,
            text='Num. Of Notes',
        )
        self.LabelNumOfNotes.grid(row=3, column=0, padx=5)
        self.entryNumOfNotes = ctk.CTkEntry(self.window)
        self.entryNumOfNotes.grid(row=4, column=0, padx=5)
        #
        self.btnMakeCards = ctk.CTkButton(
            self.window,
            text='Make Cards',
            fg_color=self.colorTheme,
            command=self.makeCards,
        )
        self.btnMakeCards.grid(row=4, column=1, padx=5)
        #
        self.labelPredictedResult = ctk.CTkLabel(
            self.window, text='None', text_color=self.colorTheme
        )
        self.labelPredictedResult.grid(
            row=5,
            column=0,
            columns=2,
            padx=5,
            pady=5,
        )
        #
        # Atualizamos os dados da janela e rodamos ela
        self.updateInformation()
        self.window.mainloop()

    def getNumOfRanges(self):
        """
        Metodo que atualiza se serao usados um ou dois intervalos
        """
        self.varOneOrTwoRange = self.tabIntervalos.get()

    def getDataOfRanges(self) -> list | str:
        """
        Metodo que coleta os dados dos ranges e devolve erros informativos*

        *caso o usuario coloque entradas erradas
        """
        #
        # Verificamos se serao usados 1 ou 2 ranges
        if self.varOneOrTwoRange == 'One Range':
            #
            # Tentamos processar a entrada como se fosse inteiros
            try:
                result = [
                    int(str(self.entry1IntervaloStart.get())),
                    int(str(self.entry1IntervaloEnd.get())),
                ]
                if result[0] >= result[1]:
                    return (
                        'E: O valor da entrada Start '
                        + 'of Range tem que ser maior\n'
                        + 'do que o valor da entrada End of Range.'
                    )
                return result
            #
            # Caso nao funcione informamos os usuarios que a
            # entra so pode ser inteiros
            except Exception:
                return (
                    'E: O valor da entrada Start '
                    + 'of Range e End of Range\n'
                    + 'tem que ser um número inteiro.'
                )
        #
        # E fazemos a mesma coisa caso seja dois intervalos
        elif self.varOneOrTwoRange == 'Two Ranges':
            try:
                result = [
                    list(
                        map(
                            int, str(self.entry2IntervalosRange1.get()).split()
                        )
                    ),
                    list(
                        map(
                            int, str(self.entry2IntervalosRange2.get()).split()
                        )
                    ),
                ]
                #
                # testando se os valores obitidos sao numeros
                (
                    int(result[0][0])
                    + int(result[0][1])
                    + int(result[1][0])
                    + int(result[1][1])
                )
                if (
                    result[0][0] >= result[0][1]
                    or result[1][0] >= result[1][1]
                ):
                    return (
                        'E: O valor inicial da entrada de cada intervalo\n'
                        + 'tem que ser menor do que o valor final.'
                    )
                return result
            except Exception:
                return (
                    'E: O valor da entrada First Range '
                    + 'e Second Range tem que ser dois\n'
                    + 'números inteiros separado '
                    + 'por um espaço.'
                )
        else:
            # TODO: Fazer um report de log nas atualizações futuras
            raise

    def errorFound(self):
        """
        Metodo que analisa os erros e os mostra na janela.

        Devolvendo False, caso nao tenha encontrados erros,
        ou True, caso tenha.
        """
        if str(self.rangesValues).startswith('E'):
            self.labelPredictedResult.configure(
                text=self.rangesValues[3:]  # Mostrando a mensagem
                # de erro do metodo que pega
                # esses dados
            )
        elif not (
            self.varNumMaxCardsPerNoteTest == 'n'
            or (
                self.varNumMaxCardsPerNoteTest.isdecimal()
                and int(self.varNumMaxCardsPerNoteTest) > 0
            )
        ):
            self.labelPredictedResult.configure(
                text='O número máximo de cartões por notas\n'
                + 'tem que ser um inteiro positivo ou a letra n,\n'
                + 'caso você não queira colocar um limite.'
            )
        elif not (
            self.varNumOfNotesTest.isdigit()
            and int(self.varNumOfNotesTest) > 0
        ):
            self.labelPredictedResult.configure(
                text='O número de notas tem que ser\n' + 'um inteiro positivo'
            )
        else:
            return False
        return True

    def updateInformation(self):
        """
        Metodo que atualiza as informacoes da janela.

        Ela informa o que esta errado na entrada do usuario,
        os resultados esperados se todos os parametros forem
        permitido pelo programa e mostra o feedback para quando o
        usuário fazer os cartoes.
        """
        #
        # Pegamos as informacoes da janela
        self.getNumOfRanges()
        self.rangesValues = self.getDataOfRanges()
        self.varTipoOperationMath = str(self.typeOperationMath.get())
        self.varNumMaxCardsPerNoteTest = str(self.entryNumMaxCards.get())
        self.varNumOfNotesTest = str(self.entryNumOfNotes.get())
        #
        # Os analisamos em busca de erros.
        if not self.errorFound():
            #
            # Caso nao encontremos
            #
            # Caso o usuario tenha acabado de fazer os cartoes
            if self.cardsWasMaked is True:
                # Mostramos que foram feitos por dois segundos
                self.labelPredictedResult.configure(text='Added')
                self.countTimeForShowAddedForUser += 1
                if self.countTimeForShowAddedForUser >= 20:
                    self.cardsWasMaked = False
                self.window.after(100, self.updateInformation)
                return None
            #
            # Fazemos a previsao
            try:
                self.varNumMaxCardsPerNote = int(
                    self.varNumMaxCardsPerNoteTest
                )
            # Caso o numero maximo de cartoes ser n, ou seja,
            # nao existit um numero maximo
            except Exception:
                self.varNumMaxCardsPerNote = 1000000  # 1 milhao
            self.varNumOfNotes = int(self.varNumOfNotesTest)
            #
            # Verificamos se sao um ou dois intervalos
            if self.varOneOrTwoRange == 'One Range':
                #
                # Se as operacoes sao sum/mul ou sub/div
                if (
                    self.varTipoOperationMath == 'sum'
                    or self.varTipoOperationMath == 'mul'
                ):
                    #
                    # Efetuamos os calculos
                    tamanhoDoIntervalo = (
                        self.rangesValues[1] - self.rangesValues[0] + 1
                    )
                    allCards = (
                        tamanhoDoIntervalo * (tamanhoDoIntervalo - 1)
                    ) / (2) + tamanhoDoIntervalo
                    CardsPerNotes = allCards / self.varNumOfNotes
                    if CardsPerNotes >= self.varNumMaxCardsPerNote:
                        CardsPerNotes = self.varNumMaxCardsPerNote
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.varNumOfNotes:.2f} | '
                        + f'All Cards: {allCards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {CardsPerNotes * self.varNumOfNotes:.2f}\n'
                        + f'Num Cards Per Note: {CardsPerNotes:.2f}'
                    )
                else:
                    #
                    # Efetuamos os calculos
                    tamanhoDoIntervalo = (
                        self.rangesValues[1] - self.rangesValues[0] + 1
                    )
                    allCards = tamanhoDoIntervalo**2
                    CardsPerNotes = allCards / self.varNumOfNotes
                    if CardsPerNotes >= self.varNumMaxCardsPerNote:
                        CardsPerNotes = self.varNumMaxCardsPerNote
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.varNumOfNotes:.2f} | '
                        + f'All Cards: {allCards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {CardsPerNotes * self.varNumOfNotes:.2f}\n'
                        + f'Num Cards Per Note: {CardsPerNotes:.2f}'
                    )
            else:
                if (
                    self.varTipoOperationMath == 'sum'
                    or self.varTipoOperationMath == 'mul'
                ):
                    #
                    # Efetuamos os calculos
                    tamanhoDosIntervalos = [
                        self.rangesValues[0][1] - self.rangesValues[0][0] + 1,
                        self.rangesValues[1][1] - self.rangesValues[1][0] + 1,
                    ]
                    allCards = (
                        tamanhoDosIntervalos[0] * tamanhoDosIntervalos[1]
                    )
                    CardsPerNotes = allCards / self.varNumOfNotes
                    if CardsPerNotes >= self.varNumMaxCardsPerNote:
                        CardsPerNotes = self.varNumMaxCardsPerNote
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.varNumOfNotes:.2f} | '
                        + f'All Cards: {allCards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {CardsPerNotes * self.varNumOfNotes:.2f}\n'
                        + f'Num Cards Per Note: {CardsPerNotes:.2f}'
                    )
                else:
                    #
                    # Efetuamos os calculos
                    tamanhoDosIntervalos = [
                        self.rangesValues[0][1] - self.rangesValues[0][0] + 1,
                        self.rangesValues[1][1] - self.rangesValues[1][0] + 1,
                    ]
                    allCards = (
                        tamanhoDosIntervalos[0] * tamanhoDosIntervalos[1] * 2
                    )
                    CardsPerNotes = allCards / self.varNumOfNotes
                    if CardsPerNotes >= self.varNumMaxCardsPerNote:
                        CardsPerNotes = self.varNumMaxCardsPerNote
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.varNumOfNotes:.2f} | '
                        + f'All Cards: {allCards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {CardsPerNotes * self.varNumOfNotes:.2f}\n'
                        + f'Num Cards Per Note: {CardsPerNotes:.2f}'
                    )
        self.window.after(100, self.updateInformation)

    def makeCards(self):
        """
        Metodo que faz os cartoes de matematica caso nao encontre erros.

        Retorno -> None
        """
        if not (self.errorFound()):
            MainMakeCards.main_make_cards(
                self.varNumOfNotes,
                self.varOneOrTwoRange == 'Two Ranges',
                self.rangesValues,
                self.varNumMaxCardsPerNote,
                self.varTipoOperationMath,
            )
            self.cardsWasMaked = True


if __name__ == '__main__':
    WindowMain()
