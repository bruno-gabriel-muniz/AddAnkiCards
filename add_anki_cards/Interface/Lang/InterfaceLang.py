from logging import Logger
from sqlite3 import Connection, Cursor
from typing import NoReturn

import customtkinter as ctk

from add_anki_cards.Db import DbConnect, DbSearch
from add_anki_cards.logging_main import get_logger
from add_anki_cards.models.Lang.AddCardsLang import MainAddCardsLang
from add_anki_cards.models.Lang.LangSaveCards import MainSaveCards


class WinMakeEnglish:
    """Classe que representa a janela que faz/salva os cards de ingles."""

    def __init__(
        self,
        master: ctk.CTk,
        config_user: dict[str, tuple | str],
        db: Connection,
        logger: Logger = get_logger(),
    ) -> None:
        """Metodo construtor da classe."""
        #
        # Iniciamos a janela
        self.logger = logger
        self.db = db
        self.config = config_user
        self.color_theme = self.config['color_theme']
        data_font = self.config['font']
        self.font = ctk.CTkFont(
            data_font[0], weight=data_font[1], size=data_font[2]
        )
        self.master = master
        self.window = ctk.CTkToplevel(master)
        self.window.title('Make Cards English')
        self.window.resizable(0, 0)
        #
        # Criamos os label que irao informar o usuario
        self.labelCardSeparetor = ctk.CTkLabel(
            self.window, font=(self.font, 15), text='Cards Separetor'
        )
        self.labelCardSeparetor.grid(row=0, column=0, padx=5, pady=5)
        self.labelTranslationSeparetor = ctk.CTkLabel(
            self.window, font=(self.font, 15), text='Translation Separetor'
        )
        self.labelTranslationSeparetor.grid(row=0, column=1, padx=5, pady=5)
        #
        # Criamos a entrada dos separadores
        self.cardSeparetor = ctk.CTkEntry(
            self.window,
            placeholder_text='|',
            font=self.font,
        )
        self.valueCardSeparetor = '|'
        self.cardSeparetor.grid(row=1, column=0, padx=5, pady=5)
        self.translationSeparetor = ctk.CTkEntry(
            self.window,
            placeholder_text=';',
            font=self.font,
        )
        self.valueTranslationSeparetor = ';'
        self.translationSeparetor.grid(row=1, column=1, padx=5, pady=5)
        #
        # Criamos a caixa de texto para informa os status dos
        # novos cartoes e botao que os cria
        self.labelInfoCards = ctk.CTkLabel(  # informacoes
            self.window,
            font=(self.font, 15),
            text_color=self.color_theme,
            text='No Added',
        )
        self.labelInfoCards.grid(row=2, column=0, padx=5, pady=5)
        self.btnMake_cards = ctk.CTkButton(  # o botao
            self.window,
            command=self.make_cards,
            text='Make Cards',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.btnMake_cards.grid(row=2, column=1, pady=5, padx=5)
        # a caixa de texto
        self.TextCards = ctk.CTkTextbox(self.window, 300, 200, font=self.font)
        self.TextCards.grid(row=3, column=0, columns=2)
        #
        # e rodamos a janela
        self.logger.info('Rodando a janela que faz/salva os cards de Inglês')
        self.window.bind('<Escape>', self.close_window)
        self.window.bind('<Return>', self.make_cards)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.mainloop()

    def make_cards(self, event=None) -> NoReturn:
        """Met. que faz os cartoes de ingles e os adciona no DB."""
        self.logger.info('Analizando os Separadores')
        # verificamos se os separador sao os padroes
        if self.cardSeparetor.get() != '':
            self.valueCardSeparetor = self.cardSeparetor.get()
        if self.translationSeparetor.get() != '':
            self.valueTranslationSeparetor = self.translationSeparetor.get()
        # salvamos os cartoes
        self.logger.info('Salvando os cartoes de Inglês')
        MainSaveCards.main_save_cards(
            self.TextCards.get('0.0', 'end'),
            self.valueCardSeparetor,
            self.valueTranslationSeparetor,
            'english',
            db=self.db,
            logger=self.logger,
        )
        self.logger.info('Atualizando as informacoes')
        # atualizamos as informacoes
        self.labelInfoCards.configure(text='Added')
        # mostramos o botao para reinicializar a janela
        # e dessa forma permir a criacao de mais cartoes
        self.btnRestart = ctk.CTkButton(
            self.window,
            width=280,
            text='Restart for add more cards',
            command=self.restart,
            fg_color=self.color_theme,
        )
        self.btnRestart.grid(row=4, column=0, columns=2)

    def restart(self) -> NoReturn:
        """Met. que reinicializa a janela WinMakeEnglish."""
        self.logger.info('Reiniciando a janela WinMakeEnglish')
        self.db.close()
        self.window.after(100, self.window.destroy())
        WinMakeEnglish(
            self.master,
            self.color_theme,
            self.font,
            self.db,
            self.logger,
        )

    def close_window(self, event=None) -> NoReturn:
        self.logger.info('Fechando a janela MakeEnglish')
        self.window.destroy()
        self.db.close()
        return None


class WinAddCardsLang:
    """Class que representa a janela que add os cards de ingles no anki."""

    def __init__(
        self,
        master: ctk.CTk,
        config_user: dict[str, tuple | str],
        info_english: list,
        db: Connection | Cursor = DbConnect.db_connect(),
        logger: Logger = get_logger(),
    ) -> None:
        """Metodo construtor da classe."""
        self.logger = logger
        #
        # Iniciamos os meta-dados da janela,
        self.db = db
        self.db_searched = DbSearch.DbResearcher(self.db)
        self.config = config_user
        self.color_theme = self.config['color_theme']
        data_font = self.config['font']
        self.font = ctk.CTkFont(
            data_font[0], weight=data_font[1], size=data_font[2]
        )
        self.info_english = info_english
        #
        # A janela,
        self.window = ctk.CTkToplevel(master)
        self.window.title('Add English Cards')
        self.window.resizable(0, 0)
        #
        # Mostramos as informacoes dos cartoes,
        self.labelInfoCards = ctk.CTkLabel(
            self.window,
            text=f'{self.info_english[0]:>} | {self.info_english[1]:<}'
            + f'\n{self.info_english[2]:^}',
            font=self.font,
        )
        self.labelInfoCards.grid(row=0, column=0, columns=2, padx=5, pady=5)
        #
        # O campo de insercao da quantidade dos cartoes
        self.quantCards = ctk.CTkEntry(
            self.window,
            placeholder_text='Num. of Cards',
            font=self.font,
        )
        self.quantCards.grid(row=1, column=0, padx=5, pady=5)
        #
        # E o botao para adiciona-los no Anki
        self.btnAdd_cards = ctk.CTkButton(
            master=self.window,
            text='Add Cards',
            font=self.font,
            command=self.add_cards,
            fg_color=self.color_theme,
        )
        self.btnAdd_cards.grid(row=1, column=1, padx=5, pady=5)
        #
        # E rodamos a janela
        self.logger.info('Rodando a janela que adciona os cartoes de Inglês')
        self.window.bind('<Return>', self.add_cards)
        self.window.bind('<Escape>', self.close_window)
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.mainloop()

    def add_cards(self, event=None) -> NoReturn:
        """Met. que aciona o back-end para fazer os cartoes de ingles."""
        #
        # Primeiro, chamamos a funcao do back end.
        self.logger.info('Adicionando os cartoes de Inglês')
        MainAddCardsLang.AddCardsLang(
            int(self.quantCards.get()),
            db=self.db,
            logger=self.logger,
        ).add_cards()
        #
        # Depois atualizamos as informacoes da janela.
        self.logger.info('Atualizando as informacoes da janela')
        self.info_english = list(self.db_searched.count_notes_of_english())
        self.info_english = [
            f'Added Notes: {self.info_english[0]}',
            f'Stored Notes: {self.info_english[1]}',
            f'All Notes: {self.info_english[2]}',
        ]
        self.labelInfoCards.configure(
            text=f'{self.info_english[0]:>} | {self.info_english[1]:<}'
            + f'\n{self.info_english[2]:^}'
        )

    def close_window(self, event=None) -> NoReturn:
        self.logger.info('Fechando a janela AddEnglish.')
        self.window.destroy()
        self.db.close()
