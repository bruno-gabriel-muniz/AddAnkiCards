from logging import Logger
from sqlite3 import Connection
from typing import NoReturn

import customtkinter as ctk
import requests
from CTkTable import CTkTable

from add_anki_cards.Db import DbSearch
from add_anki_cards.logging_main import get_logger
from add_anki_cards.models.Math.AddCardsMath import MainAddCardsMath
from add_anki_cards.models.Math.MakeCardsMath import MainMakeCards


class WinMakeMath:
    """Class que representa a janela que faz/salva os cards de matematica."""

    def __init__(
        self,
        master: ctk.CTk,
        config_user: dict[str, tuple | str],
        db: Connection,
        logger: Logger = get_logger(),
    ) -> None:
        """Metodo construtor da classe."""
        #
        # Informacoes da janela.
        self.logger = logger
        self.db = db
        self.master = master
        self.config = config_user
        self.color_theme = self.config['color_theme']
        data_font = self.config['font']
        self.font = ctk.CTkFont(
            data_font[0], weight=data_font[1], size=data_font[2]
        )
        self.erro_msg = ''
        self.var_one_or_two_range = 'One Range'
        self.cardsWasMaked = False
        self.countTimeForShowAddedForUser = 0
        #
        # configuracoes iniciais
        self.window = ctk.CTkToplevel(master)
        self.window.title('Make Math Cards')
        self.window.resizable(0, 0)
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
            self.tab1Intervalo,
            text='Start of Range',
            font=(self.font, 12, 'bold'),
        )
        self.label1IntervaloStart.grid(row=0, column=0, padx=5)
        #
        self.entry1IntervaloStart = ctk.CTkEntry(
            self.tab1Intervalo,
            placeholder_text='"1" if range is 1 to 10',
            font=(self.font, 12, 'bold'),
        )
        self.entry1IntervaloStart.grid(row=1, column=0, padx=5)
        #
        self.label1IntervaloEnd = ctk.CTkLabel(
            self.tab1Intervalo,
            text='End of Range',
            font=(self.font, 12, 'bold'),
        )
        self.label1IntervaloEnd.grid(row=0, column=1, padx=5)
        #
        self.entry1IntervaloEnd = ctk.CTkEntry(
            self.tab1Intervalo,
            placeholder_text='"10" if range is 1 to 10',
            font=(self.font, 12, 'bold'),
        )
        self.entry1IntervaloEnd.grid(row=1, column=1, padx=5)
        #
        # Configuracoes da segunda aba
        self.label2IntervalosRange1 = ctk.CTkLabel(
            self.tab2Intervalos,
            text='First Range',
            font=(self.font, 12, 'bold'),
        )
        self.label2IntervalosRange1.grid(row=0, column=0, padx=5)
        #
        self.entry2IntervalosRange1 = ctk.CTkEntry(
            self.tab2Intervalos,
            placeholder_text='"1 9" if range is 1 to 9',
            font=(self.font, 12, 'bold'),
        )
        self.entry2IntervalosRange1.grid(row=1, column=0, padx=5)
        #
        self.label2IntervalosRange2 = ctk.CTkLabel(
            self.tab2Intervalos,
            text='Second Range',
            font=(self.font, 12, 'bold'),
        )
        self.label2IntervalosRange2.grid(row=0, column=1, padx=5)
        #
        self.entry2IntervalosRange2 = ctk.CTkEntry(
            self.tab2Intervalos,
            placeholder_text='"10 99" if range is 10 to 99',
            font=(self.font, 12, 'bold'),
        )
        self.entry2IntervalosRange2.grid(row=1, column=1, padx=5)
        #
        # Entrada do tipo da operacao e a quantidade maxima de cards por nota
        self.labelTypeOperationMath = ctk.CTkLabel(
            self.window,
            text='Type of Operetion',
            font=(self.font, 12, 'bold'),
        )
        self.labelTypeOperationMath.grid(row=1, column=0, padx=5)
        self.typeOperationMath = ctk.CTkOptionMenu(
            self.window,
            values=['sum', 'sub', 'mul', 'div'],
            font=(self.font, 12, 'bold'),
            fg_color=self.color_theme,
            anchor='center',
        )
        self.typeOperationMath.grid(row=2, column=0, padx=5)
        #
        self.labelNumMaxCards = ctk.CTkLabel(
            self.window,
            text='Max. Num. Cards Per Note',
            font=(self.font, 12, 'bold'),
        )
        self.labelNumMaxCards.grid(row=1, column=1, padx=5)
        self.entryNumMaxCards = ctk.CTkEntry(
            self.window,
            font=(self.font, 12, 'bold'),
        )
        self.entryNumMaxCards.grid(row=2, column=1, padx=5)
        #
        # Numero de notas que serao cridas, o botao que as cria e a
        # quantidade de cards esperados
        self.LabelNumOfNotes = ctk.CTkLabel(
            self.window,
            text='Num. Of Notes',
            font=(self.font, 12, 'bold'),
        )
        self.LabelNumOfNotes.grid(row=3, column=0, padx=5)
        self.entryNumOfNotes = ctk.CTkEntry(
            self.window,
            font=(self.font, 12, 'bold'),
        )
        self.entryNumOfNotes.grid(row=4, column=0, padx=5)
        #
        self.btnMake_cards = ctk.CTkButton(
            self.window,
            text='Make Cards',
            font=(self.font, 12, 'bold'),
            fg_color=self.color_theme,
            command=self.make_cards,
        )
        self.btnMake_cards.grid(row=4, column=1, padx=5)
        #
        self.labelPredictedResult = ctk.CTkLabel(
            self.window,
            text='None',
            text_color=self.color_theme,
            font=(self.font, 12, 'bold'),
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
        self.logger.info('Rodando a janela WinMakeMath')
        self.window.bind('<Escape>', self.close_window)
        self.window.bind('<Return>', self.make_cards)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.update_information()
        self.logger.info(
            'Analisando erros e coletando os valores das entradas.'
        )
        self.window.mainloop()

    def get_num_of_ranges(self) -> None:
        """Met. que atualiza se serao usados um ou dois intervalos."""
        self.var_one_or_two_range = self.tabIntervalos.get()
        return None

    def get_data_of_ranges(self) -> list | str:
        """Met. que coleta os dados dos ranges e devolve erros informativos."""
        self.get_num_of_ranges()
        if self.var_one_or_two_range == 'One Range':
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
        elif self.var_one_or_two_range == 'Two Ranges':
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
                assert isinstance(
                    int(result[0][0])
                    + int(result[0][1])
                    + int(result[1][0])
                    + int(result[1][1]),
                    int,
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
            self.logger.warning(
                'O usuário usou uma entrada inválida desconhecida'
            )
            return 'E: Erro desconhecido.'

    def error_found(self) -> bool:
        """
        Metodo que analisa os erros e os mostra na janela.

        Devolvendo False, caso nao tenha encontrados erros,
        ou True, caso tenha.
        """
        if str(self.ranges_values).startswith('E'):
            erro_msg = self.ranges_values[3:]
        elif not (
            self.var_num_max_cards_per_note_test == 'n'
            or (
                self.var_num_max_cards_per_note_test.isdecimal()
                and int(self.var_num_max_cards_per_note_test) > 0
            )
        ):
            erro_msg = """O número máximo de cartões por notas
tem que ser um inteiro positivo ou a letra n,
caso você não queira colocar um limite."""
        elif not (
            self.var_num_of_notes_test.isdigit()
            and int(self.var_num_of_notes_test) > 0
        ):
            erro_msg = 'O número de notas tem que ser\num inteiro positivo'
        else:
            return False
        if self.erro_msg != erro_msg:
            self.logger.info(f'InputError: {self.erro_msg}')
            self.erro_msg = erro_msg
            self.labelPredictedResult.configure(text=self.erro_msg)
        return True

    def update_information(self) -> None:
        """
        Metodo que atualiza as informacoes da janela.

        Ela informa o que esta errado na entrada do usuario,
        os resultados esperados se todos os parametros forem
        permitido pelo programa e mostra o feedback para quando o
        usuário fazer os cartoes.
        """
        #
        # Pegamos as informacoes da janela
        self.ranges_values = self.get_data_of_ranges()
        self.var_tipo_operation_math = str(self.typeOperationMath.get())
        self.var_num_max_cards_per_note_test = str(self.entryNumMaxCards.get())
        self.var_num_of_notes_test = str(self.entryNumOfNotes.get())
        #
        # Os analisamos em busca de erros.
        if not self.error_found():
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
                self.window.after(100, self.update_information)
                return None
            #
            # Fazemos a previsao
            try:
                self.var_num_max_cards_per_note = int(
                    self.var_num_max_cards_per_note_test
                )
            # Caso o numero maximo de cartoes ser n, ou seja,
            # nao existit um numero maximo
            except Exception:
                self.var_num_max_cards_per_note = 1000000  # 1 milhao
            self.var_num_of_notes = int(self.var_num_of_notes_test)
            #
            # Verificamos se sao um ou dois intervalos
            if self.var_one_or_two_range == 'One Range':
                #
                # Se as operacoes sao sum/mul ou sub/div
                if self.var_tipo_operation_math in ('sum', 'mul'):
                    #
                    # Efetuamos os calculos
                    tamanho_do_intervalo = (
                        self.ranges_values[1] - self.ranges_values[0] + 1
                    )
                    all_cards = (
                        tamanho_do_intervalo * (tamanho_do_intervalo - 1)
                    ) / (2) + tamanho_do_intervalo
                    cards_per_notes = all_cards / self.var_num_of_notes
                    cards_per_notes = min(
                        cards_per_notes,
                        self.var_num_max_cards_per_note,
                    )
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.var_num_of_notes:.2f} | '
                        + f'All Cards: {all_cards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {cards_per_notes * self.var_num_of_notes:.2f}\n'
                        + f'Num Cards Per Note: {cards_per_notes:.2f}'
                    )
                else:
                    #
                    # Efetuamos os calculos
                    tamanho_do_intervalo = (
                        self.ranges_values[1] - self.ranges_values[0] + 1
                    )
                    all_cards = tamanho_do_intervalo**2
                    cards_per_notes = all_cards / self.var_num_of_notes
                    cards_per_notes = min(
                        cards_per_notes,
                        self.var_num_max_cards_per_note,
                    )
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.var_num_of_notes:.2f} | '
                        + f'All Cards: {all_cards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {cards_per_notes * self.var_num_of_notes:.2f}\n'
                        + f'Num Cards Per Note: {cards_per_notes:.2f}'
                    )
            else:
                if self.var_tipo_operation_math in ('sum', 'mul'):
                    #
                    # Efetuamos os calculos
                    tamanho_dos_intervalos = [
                        self.ranges_values[0][1]
                        - self.ranges_values[0][0]
                        + 1,
                        self.ranges_values[1][1]
                        - self.ranges_values[1][0]
                        + 1,
                    ]
                    all_cards = (
                        tamanho_dos_intervalos[0] * tamanho_dos_intervalos[1]
                    )
                    cards_per_notes = all_cards / self.var_num_of_notes
                    cards_per_notes = min(
                        cards_per_notes,
                        self.var_num_max_cards_per_note,
                    )
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.var_num_of_notes:.2f} | '
                        + f'All Cards: {all_cards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {cards_per_notes * self.var_num_of_notes:.2f}\n'
                        + f'Num Cards Per Note: {cards_per_notes:.2f}'
                    )
                else:
                    #
                    # Efetuamos os calculos
                    tamanho_dos_intervalos = [
                        self.ranges_values[0][1]
                        - self.ranges_values[0][0]
                        + 1,
                        self.ranges_values[1][1]
                        - self.ranges_values[1][0]
                        + 1,
                    ]
                    all_cards = (
                        tamanho_dos_intervalos[0]
                        * tamanho_dos_intervalos[1]
                        * 2
                    )
                    cards_per_notes = all_cards / self.var_num_of_notes
                    cards_per_notes = min(
                        cards_per_notes,
                        self.var_num_max_cards_per_note,
                    )
                    #
                    # Mostramos os resultados
                    self.labelPredictedResult.configure(
                        text=f'Num Of Notes: {self.var_num_of_notes:.2f} | '
                        + f'All Cards: {all_cards:.2f}\n'
                        + 'Cards That Will Be Used:'
                        + f' {cards_per_notes * self.var_num_of_notes:.2f}\n'
                        + f'Num Cards Per Note: {cards_per_notes:.2f}'
                    )
        self.window.after(100, self.update_information)
        return None

    def make_cards(self, event=None) -> NoReturn:
        """Met. que faz os cartoes de matematica caso nao encontre erros."""
        self.logger.info('Fazendo os cartoes de matematica.')
        if not (self.error_found()):
            MainMakeCards.main_make_cards(
                self.var_num_of_notes,
                self.var_one_or_two_range == 'Two Ranges',
                self.ranges_values,
                self.var_num_max_cards_per_note,
                self.var_tipo_operation_math,
                self.db,
                self.logger,
            )
            self.logger.info('Cartões feitos com sucesso.')
            self.cardsWasMaked = True
        else:
            self.labelPredictedResult.configure()

    def close_window(self, event=None) -> NoReturn:
        self.logger.info('Fechando a janela MakeMath.')
        self.window.destroy()
        self.db.close()
        return None


class WinAddCardsMath:
    """Class que eh a janela que adiciona os cartoes de matematica."""

    def __init__(
        self,
        master: ctk.CTk,
        config_user: dict[str, tuple | str],
        db: Connection,
        logger: Logger = get_logger(),
    ) -> None:
        """Metodo construtor da classe."""
        #
        # Configuracoes da janela
        self.logger = logger
        self.db = db
        self.master = master
        self.window = ctk.CTkToplevel(master)
        self.config = config_user
        self.color_theme = self.config['color_theme']
        data_font = self.config['font']
        self.font = ctk.CTkFont(
            data_font[0], weight=data_font[1], size=data_font[2]
        )
        self.title = self.window.title('Add Math Cards')
        self.num_cards_added = 0
        self.window.resizable(0, 0)
        #
        # Tabela que contem todos os tipos de cartoes de matematica
        self.query_for_type_cards_math = (
            'SELECT IdTipo, TipoOperacao, Intervalo, NumNotes, '
            + 'NumNotesFree, NumCardsForNotes FROM TipoCardsCalculoMental'
        )
        self.values_of_type_cards_math = DbSearch.generic_search(
            self.query_for_type_cards_math,
            self.db,
        )
        values_of_table = [
            [
                'Id of Type',
                'Type of Operation',
                'Range(s)',
                'Num of Notes',
                'Num of Notes Free',
                'Cards Per Notes',
            ]
        ]
        for type_card in self.values_of_type_cards_math:
            type_card[5] = f'{type_card[5]:.2f}'
        self.table_shows_types_of_math_notes = CTkTable(
            self.window,
            values=values_of_table + self.values_of_type_cards_math,
            font=self.font,
        )
        self.table_shows_types_of_math_notes.grid(row=0, column=0, columns=4)
        #
        # Linha da entrada do id dos tipos das notas,
        # da quantidade de notas, o botao que as adciona e
        # a quantidade de cartões que foram adicionados
        #
        # Id Do Tipo
        self.label_id_type_notes_to_be_added = ctk.CTkLabel(
            self.window,
            text='ID of the Type of Notes to be Added',
            font=self.font,
        )
        self.label_id_type_notes_to_be_added.grid(row=1, column=0)
        #
        self.entry_id_type_notes_to_be_added = ctk.CTkEntry(
            self.window,
            width=150,
            placeholder_text='Ex.: "1" if Id Of Type is 1',
            font=self.font,
        )
        self.entry_id_type_notes_to_be_added.grid(row=2, column=0)
        #
        # Numero de cartoes
        self.label_num_of_notes_to_be_added = ctk.CTkLabel(
            self.window,
            text='Num of Notes to be Added',
            font=self.font,
        )
        self.label_num_of_notes_to_be_added.grid(row=1, column=1)
        #
        self.entry_num_of_notes_to_be_added = ctk.CTkEntry(
            self.window,
            font=self.font,
        )
        self.entry_num_of_notes_to_be_added.grid(row=2, column=1)
        #
        # Botao que os adiciona
        self.btnAdd_cardsMath = ctk.CTkButton(
            self.window,
            text='Add Cards',
            font=self.font,
            fg_color=self.color_theme,
            command=self.add_cards,
        )
        self.btnAdd_cardsMath.grid(row=2, column=2)
        #
        # Informacao de quantos cartoes foram adicionados
        self.label_num_cards_added = ctk.CTkLabel(
            self.window,
            text=f'Num of Cards Added: {self.num_cards_added:.0f}',
            text_color=self.color_theme,
            font=self.font,
        )
        self.label_num_cards_added.grid(row=2, column=3)
        #
        # Rodando a janela
        self.logger.info('Rodando a janela WinAddCardsMath')
        self.window.bind('<Escape>', self.close_window)
        self.window.bind('<Return>', self.add_cards)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.mainloop()
        return None

    def add_cards(self, event=None) -> NoReturn:
        """Met. que tenta add os cards mostra os erros caso haja."""
        self.logger.info('Tentando adicionar os cartoes de matematica')
        #
        # Primeiro, tentamos rodar o programa.
        try:
            self.var_id_tipo_nota = int(
                self.entry_id_type_notes_to_be_added.get()
            )
            self.var_num_of_notes_to_be_added = int(
                self.entry_num_of_notes_to_be_added.get()
            )
            list_results = MainAddCardsMath.AddCardsMath(
                self.var_id_tipo_nota,
                self.var_num_of_notes_to_be_added,
                db=self.db,
            ).add_cards()
            self.num_cards_added = self.num_cards_added + (
                len(list_results)
                * float(
                    self.values_of_type_cards_math[self.var_id_tipo_nota - 1][
                        5
                    ]
                )
            )
            self.label_num_cards_added.configure(
                text=f'Num of Cards Added: {self.num_cards_added:.0f}'
            )
            self.logger.info('Atualizando a tabela, após adicionar os cartoes')
            self.update_table()
        #
        # Caso, nao consigamos (por caso de um problema da api),
        # retornamos uma janela de erro.
        except requests.exceptions.ConnectionError:
            self.logger.info('O usuário não tem o Anki aberto')
            self.window_of_error = ctk.CTkToplevel(self.window)
            self.window_of_error.title('Error Window')
            self.window_of_error.resizable(0, 0)
            self.label_window_error = ctk.CTkLabel(
                self.window_of_error,
                text='Anki Needs to be Open\nWith Anki Connect Installed',
                font=(self.font, 20),
            )
            self.label_window_error.grid(row=0, column=0)
        #
        except ValueError as e:
            erro_msg_espec = (
                f'Cards Insuficientes do tipo {self.var_id_tipo_nota}'
                + ' ou tipo inexistente.\n...'
            )
            self.window_of_error = ctk.CTkToplevel(self.window)
            self.window_of_error.title('Error Window')
            self.window_of_error.resizable(0, 0)
            text_label_window_error = (
                'Number of notes to be added is'
                + ' lower then number of notes free.'
            )
            if str(e)[:25] != erro_msg_espec[:25]:
                self.logger.warning(f'Erro Inesperado: {e}.\n')
                text_label_window_error = (
                    'A Internor error ocorred. Sory ):\n'
                    + f'{"Please, restart the app.":^33}'
                )
            self.label_window_error = ctk.CTkLabel(
                self.window_of_error,
                text=text_label_window_error,
                font=(self.font, 20),
            )
            self.label_window_error.grid(row=0, column=0)

    def update_table(self) -> NoReturn:
        """Met. que atualiza os dados da tabela do tipo de notas."""
        var_antigo_notes_free = self.values_of_type_cards_math[
            self.var_id_tipo_nota - 1
        ][4]
        self.table_shows_types_of_math_notes.edit(
            self.var_id_tipo_nota,
            4,
            text=f'{var_antigo_notes_free-self.var_num_of_notes_to_be_added}',
        )
        self.values_of_type_cards_math[self.var_id_tipo_nota - 1][
            4
        ] -= self.var_num_of_notes_to_be_added

    def close_window(self, event=None) -> NoReturn:
        self.logger.info('Fechando a janela AddMath')
        self.window.destroy()
        self.db.close()
