from _tkinter import TclError
from logging import Logger
from os import path
from sqlite3 import Connection, Cursor
from tkinter import PhotoImage
from typing import NoReturn, Union

import customtkinter as ctk
import requests
from CTkTable import CTkTable

from add_anki_cards.Db import DbConnect, DbSearch
from add_anki_cards.logging_main import get_logger
from add_anki_cards.ManagerUsers.ManagerUsers import (
    CreationUserError,
    ManagerUsers,
    ReadConfig,
    RenameUserError,
)
from add_anki_cards.MathTraining.AddCardsMath import MainAddCardsMath
from add_anki_cards.MathTraining.MakeCardsMath import MainMakeCards
from add_anki_cards.PraticingEnglish.AddCardsEnglish import MainAddCardsEnglish
from add_anki_cards.PraticingEnglish.EnglishSaveCards import MainSaveCards


class Tooltip:
    def __init__(
        self,
        master_widget: ctk.CTk | ctk.CTkToplevel,
        widget: Union[ctk.CTkBaseClass],
        data_config: dict[str, Union[ctk.CTkFont, str, tuple]],
        text: str,
        logger: Logger = None,
        delay: int = 500,
    ) -> None:
        """
        Classe versátil para criar dic. de ferramenta (tooltips) em app's ctk.

        Args:
            master_widget: O widget pai para a tooltip.
            widget: O widget ao qual a tooltip está vinculada.
            data_config: Um dicionário contendo configurações para a tooltip:
                - `font`: A fonte do texto da tooltip.
                - `color_theme`: O tema de cores do texto da tooltip.
                - `theme_dark_or_light`: O modo de tema da janela da tooltip.
            text: O texto a ser exibido na tooltip.
        """
        if logger:
            self.logger = logger
        else:
            self.logger = get_logger('User_Default')
        self.master_widget = master_widget
        self.widget = widget
        self.data_config = data_config
        self.delay = delay
        self.text = text
        self.short_text = self.text[: self.text.find('\n')]
        self.tooltip_win = None
        if isinstance(self.widget, ctk.CTkButton):
            self.logger.info(
                f'Iniciando o tooltip do widget: {self.widget},'
                + f' {self.widget.cget("text")}'
            )
        elif isinstance(self.widget, (ctk.CTkEntry, ctk.CTkTextbox)):
            self.logger.info(
                f'Iniciando o tooltip do widget: {self.widget},'
                + f' {self.widget.cget("placeholder_text")}'
            )
        else:
            self.logger.info(
                f'Iniciando o tooltip do widget: {self.widget},'
                + f' {self.short_text}'
            )

        # Binds para mostrar o texto
        self.widget.bind('<Enter>', self._schedule_tooltip)
        self.widget.bind('<Leave>', self._hide_tooltip)

    def _schedule_tooltip(self, event=None):
        """Agenda a exibição do tooltip após o atraso definido."""
        self._after_id = self.widget.after(self.delay, self._show_tooltip)

    def _show_tooltip(self) -> None:
        """Met. q mostra o texto"""

        # verificando se a win tá aberta
        if not (self.tooltip_win is None):
            return None
        self.logger.debug(f'Mostrando o tooltip: {self.short_text}')
        # Criando ela caso não esteja.
        x = self.widget.winfo_rootx() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_win = ctk.CTkToplevel(self.master_widget)
        self.tooltip_win.wm_overrideredirect(True)
        self.tooltip_win.geometry(f'+{x}+{y}')
        self.tooltip_win._set_appearance_mode(
            self.data_config['theme_dark_or_ligth']
        )

        # Configurando o label da classe
        self.label = ctk.CTkLabel(
            self.tooltip_win,
            text=self.text,
            font=self.data_config['font'],
            text_color=self.data_config['color_theme'],
            corner_radius=5,
        )
        self.label.pack(padx=5, pady=2)

    def _hide_tooltip(self, event=None) -> None:
        """Met. q escode a dica."""
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

        if self.tooltip_win:
            self.logger.debug(f'Escondendo o tooltip: {self.short_text}')
            self.tooltip_win.destroy()
            self.tooltip_win = None


class WindowSelectUser:
    """Classe responsável pelo login dos usuários."""

    def __init__(self):
        """Inicializa a classe WindowSelectUser."""
        self.logger = get_logger()
        self.logger.info('Coletando os dados dos usuários.')

        # Acessando os diretórios do programa e coletando os usernames.
        path_home = path.expanduser('~')
        self.data_path = path.join(path_home, '.AddAnkiCardsData')
        self.manager_users = ManagerUsers()
        (
            self.all_users_list,
            self.users_list,
            self.hidden_users_list,
        ) = self.manager_users.load_users()
        self.is_show_all_users_list = False

        # Iniciando a janela de login.
        self.logger.info('Iniciando a janela de login')
        self.master = ctk.CTk()
        self.master.title('Select User Window')

        # Lendo as configurações padrões.
        self.logger.info('Lendo as Configurações padrões.')
        self.data_config = ReadConfig('User_Default', self.data_path).get()
        self.color_theme = self.data_config['color_theme']
        self.font = self.data_config['font']
        self.theme_dark_or_ligth = self.data_config['theme_dark_or_ligth']
        self.master._set_appearance_mode(self.theme_dark_or_ligth)
        self.master.resizable(0, 0)

        # Tentando acionar o icone.
        self.logger.info('Tentando acionar o ícone do app.')
        try:
            self.icon = 'logoApp.ico'
            self.master.iconbitmap(self.icon, True)
        except TclError:
            self.icon = 'logoApp.png'
            self.master.iconphoto(True, PhotoImage(self.icon))

        # Criando o frame de seleção e criação de usuários.
        self.logger.info('Montando o frame de seleção de usuários.')
        self._make_frame_users()

        # Botão de login.
        self.logger.info('Mostrando o botão de login')
        self._make_btn_login()

        # Fazendo os tooltips da interface
        self.logger.info('Preparando os tooltips dos widgets')
        self._make_tooltips()

        # Fazendo as binds da janela
        self.logger.info('Definindo os atalhos da interface.')
        self._make_binds()

        # Rodando a janela
        self.logger.info('Rodando a janela de login.')
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.master.mainloop()

    def _make_frame_users(self) -> None:
        """Cria o frame para seleção e criação de usuários.

        Este método inicializa o frame que contém a lista de usuários
        disponíveis e o botão para expandir a criação de novos usuários.
        """
        self.frame_users = ctk.CTkFrame(self.master)
        self.frame_users.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.frame_users_expd = False

        # Lista com os usuários disponíveis
        self.option_menu_users = ctk.CTkOptionMenu(
            self.frame_users,
            values=self.users_list,
            fg_color=self.color_theme,
            font=self.font,
            anchor='center',
        )
        self.option_menu_users.grid(row=0, column=0, padx=5, pady=5)

        # Botão para expandir a criação de usuário.
        self.btn_add_user = ctk.CTkButton(
            self.frame_users,
            command=self.add_user,
            text='+',
            font=self.font,
            width=35,
            fg_color=self.color_theme,
            anchor='center',
        )
        self.btn_add_user.grid(row=0, column=1, padx=5, pady=5)

        # Cria o restante do frame quando ele está expandido.
        self.logger.info(
            'Preparando os widgets do frame exp para criação de users.'
        )
        self._make_frame_users_exp()

    def _make_frame_users_exp(self) -> None:
        """Cria os elementos do frame quando expandido.

        Este método adiciona os elementos necessários para a criação de
        um novo usuário quando o frame está expandido.
        """
        self.entry_name_new_user = ctk.CTkEntry(
            self.frame_users,
            placeholder_text='Name new user: ',
            font=self.font,
        )

        self.btn_make_new_user = ctk.CTkButton(
            self.frame_users,
            command=self.make_user,
            text='↵',
            font=self.font,
            width=35,
            fg_color=self.color_theme,
            anchor='center',
        )

        self.label_status = ctk.CTkLabel(
            self.frame_users,
            text='',
            font=self.font,
            text_color=self.color_theme,
        )

    def _make_btn_login(self) -> None:
        """Cria o botão de login.

        Este método inicializa o botão de login na interface principal.
        """
        self.master.grid_rowconfigure(1, weight=1)
        self.btn_make_login = ctk.CTkButton(
            self.master,
            text='Login',
            font=self.font,
            command=self.make_login,
            fg_color=self.color_theme,
        )
        self.btn_make_login.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew'
        )

    def _make_tooltips(self) -> None:
        """Cria os tooltip da interface."""
        Tooltip(
            self.master,
            self.option_menu_users,
            self.data_config,
            'Usuário que fará o login.'
            + '\nHot Key: "Tab".'
            + '\n"Ctrl + h" para mostra usuários ocultos.',
            self.logger,
        )
        Tooltip(
            self.master,
            self.btn_add_user,
            self.data_config,
            'Btn para expandir o menu de criação de usuários.'
            + '\nHot Key: "Ctrl + Enter"',
            self.logger,
        )
        Tooltip(
            self.master,
            self.entry_name_new_user,
            self.data_config,
            'Entrada do nome do novo usuário.',
            self.logger,
        )
        Tooltip(
            self.master,
            self.btn_make_new_user,
            self.data_config,
            'Botão para criar o novo usuário.'
            + '\nHot Key: "Enter" quando o menu está expandido.',
            self.logger,
        )
        Tooltip(
            self.master,
            self.btn_make_login,
            self.data_config,
            'Fazer Login.' + '\nHot Key: "Enter".',
            self.logger,
        )

    def _make_binds(self) -> None:
        """Configura os atalhos de teclado.

        Este método associa teclas específicas a ações na interface,
        permitindo uma navegação mais rápida e intuitiva.
        """
        self.master.bind('<Control-h>', self.show_all_users)
        self.master.bind('<Control-Return>', self.add_user)
        self.master.bind('<Tab>', self.get_next_user)
        self.master.bind('<Return>', self.make_login)
        self.master.bind('<Escape>', self.close_window)

    def get_next_user(self, event=None) -> NoReturn:
        """Seleciona o próximo usuário da lista de usuários."""
        options = self.option_menu_users._values
        next_index = (options.index(self.option_menu_users.get()) + 1) % len(
            options
        )
        self.option_menu_users.set(options[next_index])
        self.logger.info(
            f'Selecionando o próximo usuário: "{options[next_index]}".'
        )

    def update_option_menu_user(self) -> None:
        """Atualiza os nomes de usuários do option menu."""
        self.logger.info('Atualizando a lista de usuários disponíveis.')
        (
            self.all_users_list,
            self.users_list,
            self.hidden_users_list,
        ) = self.manager_users.load_users()
        if self.is_show_all_users_list:
            self.option_menu_users.configure(values=self.all_users_list)
        else:
            self.option_menu_users.configure(values=self.users_list)

    def show_all_users(self, event=None) -> NoReturn:
        """Mostra todos os usuários, incluindo os ocultos."""
        self.update_option_menu_user()
        if not self.is_show_all_users_list:
            self.logger.info('Mostrando usuários ocultos e normais.')
            self.option_menu_users.configure(values=self.all_users_list)
            self.is_show_all_users_list = True
        else:
            self.logger.info('Mostrando apenas usuários normais.')
            while self.option_menu_users.get().startswith('.'):
                self.get_next_user()
            self.option_menu_users.configure(values=self.users_list)
            self.is_show_all_users_list = False

    def make_login(self, event=None) -> NoReturn:
        """Realiza o login do usuário selecionado."""
        user = self.option_menu_users.get()
        self.logger.info(f'Fazendo login com: {user}')
        self.master.after(100, self.master.destroy())
        WindowMain(
            DbConnect.db_connect(user=user),
            get_logger(user=user),
            user,
            self.icon,
        )

    def add_user(self, event=None) -> NoReturn:
        """Expande ou contrai o menu de adição de usuário."""
        if not self.frame_users_expd:
            self.logger.info('Expandindo o menu add_user.')
            self.entry_name_new_user.grid(row=1, column=0)
            self.btn_make_new_user.grid(row=1, column=1)
            self.btn_add_user.configure(text='-')
            self.master.bind('<Return>', self.make_user)
            self.frame_users_expd = True
        else:
            self.logger.info('Contraindo o menu add_user.')
            self.btn_make_new_user.grid_forget()
            self.entry_name_new_user.grid_forget()
            if self.label_status.grid_info():
                self.label_status.grid_forget()
            self.btn_add_user.configure(text='+')
            self.master.bind('<Return>', self.make_login)
            self.frame_users_expd = False

    def make_user(self, event=None) -> NoReturn:
        """Cria um novo usuário."""
        self.logger.info('Tentando adicionar um novo usuário.')
        new_name = self.entry_name_new_user.get()
        find_err, error_msg = self.manager_users.new_name_user_is_valid(
            new_name,
        )
        if find_err:
            self._handle_user_creation_error(CreationUserError(error_msg))
            return None
        self.manager_users.make_user(new_name)
        self.logger.info('Atualizando a janela de login.')
        self.update_option_menu_user()
        if self.is_show_all_users_list or not new_name.startswith('.'):
            self.option_menu_users.set(new_name)
        self.label_status.configure(text=f'Usuário {new_name} foi criado.')
        self.logger.info(f'O usuário: {new_name}, foi criado.')
        self.add_user()

    def _handle_user_creation_error(self, e: CreationUserError) -> NoReturn:
        """Trata os na criação de usuário já conhecidos e tratados."""
        if str(e) == 'O nome não pode estar em branco.':
            self.logger.info(f'Erro de valor tratado: {e}.')
            self.label_status.configure(text=e)
            self.label_status.grid(row=2, column=0, columnspan=2)
        elif str(e) == 'O novo nome não pode ser igual ao do usuário padrão.':
            self.logger.info(f'Erro de valor tratado: {e}')
            self.label_status.configure(text=e)
            self.label_status.grid(row=2, column=0, columnspan=2)
        elif str(e) == "O nome não pode conter os char's: / ou \\":
            self.logger.info(f'Erro de valor tratado: {e}')
            self.label_status.configure(text=e)
            self.label_status.grid(row=2, column=0, columnspan=2)
        elif str(e) == 'Outro usuário já possui este nome.':
            self.logger.info(f'Erro de valor tratado: {e}')
            self.label_status.configure(text=e)
            self.label_status.grid(row=2, column=0, columnspan=2)
        else:
            self.logger.error(f'Erro inesperado: {e}')
            self.label_status.configure(text=f'Erro inesperado:\n{e}')
            self.label_status.grid(row=2, column=0, columnspan=2)

    def _handle_unexpected_error(self, e: Exception) -> NoReturn:
        """Trata erros inesperados."""
        self.logger.error(f'Erro inesperado:\n{e}')
        self.label_status.configure(text=f'Erro inesperado:\n{e}')
        self.label_status.grid(row=2, column=0, columnspan=2)

    def close_window(self, event=None) -> NoReturn:
        """Fecha a janela de login."""
        self.logger.info('Fechando a janela de login.')
        self.master.destroy()


class WindowMain:
    """Classe que representa as janelas do programa."""

    def __init__(
        self,
        db: Connection = DbConnect.db_connect(),
        logger: Logger = get_logger(),
        user: str = 'User_Default',
        icon: str | PhotoImage = 'logoApp.ico',
    ) -> None:
        """Metodo construtor da classe."""
        self.logger = logger
        #
        self.logger.info('Conectando no Banco de Dados')
        self.db = db
        #
        self.user = user
        self.to_change_user = False
        #
        # Iniciamos a janela
        self.logger.info('Iniciando a janela principal.')
        self.icon = icon
        self.Master = ctk.CTk()
        self.Master.resizable(0, 0)
        if self.icon.endswith('.ico'):
            self.Master.iconbitmap(self.icon, True)
        else:
            self.Master.iconphoto(True, PhotoImage(self.icon))
        #
        # Definindo as configurações de aparencia.
        data_path = path.join(path.expanduser('~'), '.AddAnkiCardsData')
        self.config = ReadConfig(self.user, data_path).get()
        self.font = self.config['font']
        self.Master._set_appearance_mode(self.config['theme_dark_or_ligth'])
        self.color_theme = self.config['color_theme']
        self.Master.title('Add Anki Cards')
        #
        #
        self.menu_main = ctk.CTkFrame(self.Master, fg_color='#666666')
        self.menu_main.grid_columnconfigure(0, weight=1)
        self.menu_main.grid(
            row=0, column=0, columns=2, padx=0, pady=0, sticky='ew'
        )
        self.label_name_user = ctk.CTkLabel(
            self.menu_main,
            text=self.user,
            font=self.font,
        )
        self.label_name_user.grid(row=0, column=0, padx=5, sticky='w')
        self.btn_config_user = ctk.CTkButton(
            self.menu_main,
            command=self.config_user,
            text='⚙',
            font=(self.font, 20),
            width=35,
            fg_color='transparent',
        )
        self.btn_config_user.grid(row=0, column=1, sticky='e')
        self.btn_change_user = ctk.CTkButton(
            self.menu_main,
            command=self.change_user,
            text='Change User',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.btn_change_user.grid(row=0, column=2, padx=2, sticky='e')
        #
        # Fazemos o titulo da parte do ingles
        self.LabelEnglish = ctk.CTkLabel(
            self.Master, text='English', font=(self.font, 30)
        )
        self.LabelEnglish.grid(row=1, column=0, columns=2, padx=5, pady=5)
        #
        # Coletamos os dados dos cartoes e mostramos na janela
        self.logger.info('Coletando os dados dos cartoes de Inglês')
        self.db_searched = DbSearch.DbResearcher(self.db)
        self.info_english = list(self.db_searched.count_notes_of_english())
        self.info_english = [
            f'Added Notes: {self.info_english[0]}',
            f'Stored Notes: {self.info_english[1]}',
            f'All Notes: {self.info_english[2]}',
        ]
        self.labelEnglishInfo = ctk.CTkLabel(
            self.Master,
            text=f'{self.info_english[0]:>} | '
            + f'{self.info_english[1]:<}\n{self.info_english[2]:^}',
            font=self.font,
        )
        self.labelEnglishInfo.grid(row=2, column=0, columns=2, padx=5, pady=5)
        #
        # Fazemos os botoes que vao adicionar e fazer os cartoes de ingles
        self.btnEnglishAdd = ctk.CTkButton(
            self.Master,
            height=70,
            command=self.make_win_add_cards_english,
            text='Add Cards',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.btnEnglishAdd.grid(row=3, column=0, padx=5, pady=5)
        #
        #
        self.btnEnglishMake = ctk.CTkButton(
            self.Master,
            command=self.make_win_make_english,
            height=70,
            text='Make Cards',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.btnEnglishMake.grid(row=3, column=1, padx=5, pady=5)
        #
        # Fazemos a divisoria
        ctk.CTkCanvas(self.Master, height=0, width=300).grid(
            row=4, column=0, columns=2, pady=5
        )
        #
        # E fazemos a mesma coisa para as opcoes e informacoes da matematica
        self.LabelMath = ctk.CTkLabel(
            self.Master, text='Math', font=(self.font, 30)
        )  # titulo
        self.LabelMath.grid(row=5, column=0, columns=2, padx=5, pady=5)
        #
        # Informacoes
        self.logger.info('Coletando os dados dos cartoes de Matematica')
        self.InfoMath = list(self.db_searched.count_cards_of_math())
        self.InfoMath = [
            f'Added Cards: {int(self.InfoMath[0])}',
            f'Stored Cards: {int(self.InfoMath[1])}',
            f'All Cards: {int(self.InfoMath[2])}',
        ]
        self.labelMathInfo = ctk.CTkLabel(
            self.Master,
            text=f'{self.InfoMath[0]:>} | '
            + f'{self.InfoMath[1]:<}\n{self.InfoMath[2]:^}',
            font=self.font,
        )
        self.labelMathInfo.grid(row=6, column=0, columns=2, padx=5, pady=5)
        #
        # Botoes
        self.btnMathAdd = ctk.CTkButton(
            self.Master,
            height=70,
            text='Add Cards',
            font=self.font,
            fg_color=self.color_theme,
            command=self.make_win_add_cards_math,
        )
        self.btnMathAdd.grid(row=7, column=0, padx=5, pady=5)
        #
        #
        self.btnMathMake = ctk.CTkButton(
            self.Master,
            height=70,
            text='Make Cards',
            font=self.font,
            command=self.make_win_make_math,
            fg_color=self.color_theme,
        )
        self.btnMathMake.grid(row=7, column=1, padx=5, pady=5)
        #
        # funcao que roda e atualiza a janeal principal
        self.logger.info('Rodando a janela principal')
        self.update_information()
        self.Master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.Master.bind('<Escape>', self.close_window)
        self.Master.mainloop()
        if self.to_change_user:
            WindowSelectUser()
        return None

    def change_user(self) -> NoReturn:
        self.Master.after(100, self.Master.destroy())
        self.to_change_user = True

    def config_user(self) -> NoReturn:
        WinConfigUser(
            self,
            self.icon,
            self.config,
            self.user,
            DbConnect.db_connect(self.user),
            self.logger,
        )

    def update_information(self) -> None:
        """Atualiza as informações da janela principal."""
        self.logger.info('Atualizando as informacoes da janela principal')
        #
        # atualizamos as informacoes de ingles
        self.info_english = list(self.db_searched.count_notes_of_english())
        self.info_english = [
            f'Added Notes: {self.info_english[0]}',
            f'Stored Notes: {self.info_english[1]}',
            f'All Notes: {self.info_english[2]}',
        ]
        self.labelEnglishInfo.configure(
            text=f'{self.info_english[0]:>} | '
            + f'{self.info_english[1]:<}\n{self.info_english[2]:^}'
        )
        #
        # atualizamos as informacoes de matematica
        self.InfoMath = list(self.db_searched.count_cards_of_math())
        self.InfoMath = [
            f'Added Cards: {self.InfoMath[0]:,.0f}',
            f'Stored Cards: {self.InfoMath[1]:,.0f}',
            f'All Cards: {self.InfoMath[2]:,.0f}',
        ]
        self.labelMathInfo.configure(
            text=f'{self.InfoMath[0]:>} | '
            + f'{self.InfoMath[1]:<}\n{self.InfoMath[2]:^}'
        )

        self.Master.after(5000, self.update_information)

    def make_win_make_english(self) -> NoReturn:
        """Funcao que inicia a janela que faz/salva os cards de ingles."""
        self.logger.info('Iniciando a janela que faz/salva os cards de Inglês')
        WinMakeEnglish(
            self.Master,
            self.color_theme,
            self.font,
            DbConnect.db_connect(user=self.user),
            self.logger,
        )

    def make_win_add_cards_english(self) -> NoReturn:
        """Met. que cria a janela que adciona os cartoes de ingles no anki."""
        self.logger.info('Iniciando a janela que adciona os cartoes de Inglês')
        WinAddCardsEnglish(
            self.Master,
            self.color_theme,
            self.font,
            self.info_english,
            DbConnect.db_connect(user=self.user),
            self.logger,
        )

    def make_win_make_math(self) -> NoReturn:
        """Funcao que inicia a janela que faz/salva os cards de Matematica."""
        self.logger.info(
            'Iniciando a janela que faz/salva os cards de Matematica'
        )
        WinMakeMath(
            self.Master,
            self.color_theme,
            self.font,
            DbConnect.db_connect(user=self.user),
            self.logger,
        )

    def make_win_add_cards_math(self) -> NoReturn:
        """Met. que cria a janela que adciona os cartoes de ingles no anki."""
        self.logger.info(
            'Iniciando a janela que adciona os cartoes de Matematica'
        )
        WinAddCardsMath(
            self.Master,
            self.color_theme,
            self.font,
            DbConnect.db_connect(user=self.user),
            self.logger,
        )

    def close_window(self, event=None) -> None:
        self.logger.info('Fechando a janela principal.')
        self.Master.destroy()
        self.db.close()
        return None


class WinConfigUser:
    """Classe para configurar o usuário."""

    def __init__(
        self,
        master: WindowMain,
        icon,
        config_user: dict[str, tuple | str],
        user: str = 'User_Default',
        db: Connection = DbConnect.db_connect(),
        logger: Logger = get_logger(),
    ) -> None:
        """
        Inicializa a classe WinConfigUser.

        Parâmetros:
            master (WindowMain): Janela principal.
            color_theme (str): Tema de cor da interface.
            font (ctk.CTkFont): Fonte utilizada na interface.
            icon (str | None): Ícone da janela.
            user (str): Nome do usuário. Padrão é 'User_Default'.
            db (Connection): Conexão com o banco de dados.
            logger (Logger): Logger para registrar eventos.
        """
        self.logger = logger
        self.logger.info('Lendo as configurações do usuário.')
        self.master = master
        self.config = config_user
        self.color_theme = self.config['color_theme']
        self.font = self.config['font']
        self.data_path = path.join(path.expanduser('~'), '.AddAnkiCardsData')
        self.logger.info('Iniciando o a classe de gerenciamento de users.')
        self.manager_user = ManagerUsers(self.data_path)
        self.user = user
        self.db = db
        self.icon = icon

        # Criando a janela de configuração.
        self.logger.info('Iniciando a janela.')
        self.window = ctk.CTkToplevel(self.master.Master)
        self.window.resizable(0, 0)
        self.window.title(f'Config {self.user}')

        # Criando as abas de configurações.
        self.logger.info('Criando as abas de configurações.')
        self.tab_view_config = ctk.CTkTabview(
            self.window,
            height=75,
            width=50,
            fg_color='#000000',
        )
        self.list_names_tab_view = []

        # Criando a aba de configuração de nome
        self.logger.info('Criando a aba de configuração do nome.')
        self._make_tab_username()
        self.list_names_tab_view.append('Config Name')

        # Criando o label e o botão apply
        self.logger.info('Criando o label e o btn de apply.')
        self._make_btn_label_apply()

        # Criando os atalhos
        self.logger.info('Criando as binds da interface.')
        self._make_binds()

        # Criando os Tooltips
        self.logger.info('Criando os tooltips da interface.')
        self._make_tooltips()

        # Rodando a janela
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.mainloop()

    def _make_tab_username(self) -> None:
        """Cria a aba de configuração de nome de usuário."""
        self.tab_name_user = self.tab_view_config.add('Config Name')
        self.tab_name_user.configure(height=75, width=50)

        # Entry para o novo nome.
        self.logger.debug('Criando a caixa entrada para o novo nome.')
        self.entry_alter_name = ctk.CTkEntry(
            self.tab_name_user,
            placeholder_text=f'{self.user}',
            font=self.font,
        )
        self.tab_name_user.grid_rowconfigure(0, weight=1)
        self.tab_name_user.grid_columnconfigure(0, weight=1)
        self.entry_alter_name.grid(
            row=0, column=0, padx=5, pady=5, stick='nsew'
        )

        # Btn para alterar o nome de usuário.
        self.should_apply_change_username = False
        self.txt_change_username = ''
        self.logger.debug('Criando o botão para alterar o nomo de usuário.')
        self.btn_change_username = ctk.CTkButton(
            self.tab_name_user,
            command=self.change_username,
            text='Change Username',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.tab_name_user.grid_rowconfigure(0, weight=1)
        self.tab_name_user.grid_columnconfigure(1, weight=1)
        self.btn_change_username.grid(
            row=0, column=1, padx=5, pady=5, stick='nsew'
        )

        # Btn para ocultar o usuário.
        self.logger.debug('Criando o btn para ocultar o usuário.')
        self.should_apply_hidden_user = False
        self.txt_hidden_user = ''
        self.btn_hidden_user = ctk.CTkButton(
            self.tab_name_user,
            command=self.hide_user,
            text='Hide User',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.tab_name_user.grid_rowconfigure(1, weight=1)
        self.tab_name_user.grid_columnconfigure(0, weight=1)
        self.btn_hidden_user.grid(row=1, column=0, columns=2, stick='nsew')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.tab_view_config.grid(
            row=0, column=0, padx=5, pady=5, sticky='nsew'
        )

    def _make_btn_label_apply(self) -> None:
        """Cria o botão e o label para aplicar as mudanças."""

        # Criando o botão que informa o que será feito no apply.
        self.logger.debug('Criando o label do apply.')
        self.txt_steps_for_apply = 'Steps for apply:\n'
        self.label_steps_for_apply = ctk.CTkLabel(
            self.window,
            text=self.txt_steps_for_apply,
            font=self.font,
            text_color=self.color_theme,
        )
        self.label_steps_for_apply.grid(row=1, column=0, columns=2)

        # Criando o btn do apply
        self.logger.debug('Criando o btn de apply')
        self.should_apply_changes = False
        self.btn_apply = ctk.CTkButton(
            self.window,
            command=self.make_apply,
            text='Apply',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.window.grid_rowconfigure(2, weight=1)
        self.btn_apply.grid(
            row=2,
            column=0,
            columns=2,
            padx=5,
            pady=5,
            sticky='ew',
        )

    def _make_binds(self) -> None:
        """Configura os atalhos de teclado."""
        self.window.bind('<Return>', self.make_apply)
        self.window.bind('<Tab>', self.get_next_tab)

    def _make_tooltips(self) -> None:
        Tooltip(
            self.window,
            self.entry_alter_name,
            self.config,
            'Novo nome do usuário.',
            self.logger,
        )
        Tooltip(
            self.window,
            self.btn_change_username,
            self.config,
            'Btn para acionar a alteração do nome na aplicação.',
            self.logger,
        )
        Tooltip(
            self.window,
            self.btn_hidden_user,
            self.config,
            'Btn para ocultar o usuário.',
            self.logger,
        )
        Tooltip(
            self.window,
            self.btn_apply,
            self.config,
            'Btn para aplicar as alterações no usuário.',
            self.logger,
        )

    def get_next_tab(self, event=None) -> None:
        """Seleciona a próxima aba de configuração."""
        try:
            current_idx = self.list_names_tab_view.index(
                self.tab_view_config.get()
            )
            self.tab_view_config.set(self.list_names_tab_view[current_idx + 1])
        except IndexError:
            self.tab_view_config.set(self.list_names_tab_view[0])
        except Exception as e:
            raise e
        return None

    def change_username(self) -> None:
        """Altera o nome de usuário."""
        if self.should_apply_changes and self.should_apply_change_username:
            self.logger.info('Aplicando a alteração do nome.')
            self.make_change_user_name()
        else:
            if not self.should_apply_change_username:
                self.logger.info('Preparando para alterar o nome de usuário.')
                self.rename_to = self.entry_alter_name.get()
                (
                    name_is_valid,
                    error_msg,
                ) = self.manager_user.new_name_user_is_valid(self.rename_to)
                if not name_is_valid:
                    self.txt_change_username = ''
                    self.update_label_apply()
                    self._handle_rename_user_error(error_msg)
                    return None
                self.txt_change_username = (
                    f'Rename user "{self.user}" to "{self.rename_to}".\n'
                )
                self.update_label_apply()
                self.btn_change_username.configure(text='N:Change Username')
                self.should_apply_change_username = True
            else:
                self.logger.info('Cancelando a alteração de nome do user.')
                self.txt_change_username = ''
                self.update_label_apply()
                self.btn_change_username.configure(text='Change Username')
                self.should_apply_change_username = False

            # Reconfigurnado a opição de esconder usuário.
            self.hide_user()
            self.hide_user()

    def make_change_user_name(self) -> None:
        """Realiza a alteração do nome de usuário."""
        if self.should_apply_hidden_user:
            self.manager_user.rename_user(self.user, self.rename_hidden)
            if self.user == 'User_Default':
                self.manager_user.make_user('User_Default')
            self.user = self.rename_hidden
        else:
            self.manager_user.rename_user(self.user, self.rename_to)
            if self.user == 'User_Default':
                self.manager_user.make_user('User_Default')
            self.user = self.rename_to

    def hide_user(self) -> None:
        """Esconde o usuário."""
        if self.should_apply_changes and self.should_apply_hidden_user:
            self.make_hide_user()
        else:
            if not self.should_apply_hidden_user:
                if self.should_apply_change_username:
                    if self.rename_to.startswith('.'):
                        self.txt_hidden_user = (
                            f'Rename user "{self.user}"'
                            + f' to "{self.rename_to}".\n'
                        )
                        self.rename_hidden = self.rename_to
                    else:
                        self.txt_hidden_user = (
                            f'Rename user "{self.user}"'
                            + f' to ".{self.rename_to}".\n'
                        )
                        self.rename_hidden = f'.{self.rename_to}'
                elif self.user.startswith('.'):
                    self.txt_hidden_user = (
                        f'Rename user "{self.user}"'
                        + f' to "{self.user[1:]}".\n'
                    )
                    self.rename_hidden = self.user[1:]
                else:
                    self.txt_hidden_user = (
                        f'Rename user "{self.user}"' + f' to ".{self.user}".\n'
                    )
                    self.rename_hidden = f'.{self.user}'
                self.update_label_apply()
                self.btn_hidden_user.configure(text='N:Hide User')
                self.should_apply_hidden_user = True
            else:
                self.txt_hidden_user = ''
                self.update_label_apply()
                self.btn_hidden_user.configure(text='Hide User')
                self.should_apply_hidden_user = False

    def make_hide_user(self) -> None:
        """Realiza a ação de esconder o usuário."""
        if not self.should_apply_change_username:
            self.manager_user.rename_user(self.user, self.rename_hidden)
            if self.user == 'User_Default':
                self.manager_user.make_user('User_Default')
            self.user = self.rename_hidden

    def update_label_apply(self) -> None:
        """Atualiza o label de passos para aplicar."""
        self.txt_steps_for_apply = 'Steps for apply:\n'
        self.txt_steps_for_apply += self.txt_change_username
        self.txt_steps_for_apply += self.txt_hidden_user
        self.label_steps_for_apply.configure(text=self.txt_steps_for_apply)

    def restart_apply(self) -> NoReturn:
        """Reinicia os passos para aplicar."""
        self.steps_for_apply = []
        self.txt_steps_for_apply = 'Steps for apply:\n'
        self.label_steps_for_apply.configure(text=self.txt_steps_for_apply)

    def make_apply(self, event=None) -> None:
        """Aplica as mudanças."""
        try:
            self.should_apply_changes = True
            self.change_username()
            self.hide_user()
        except (RenameUserError, ValueError) as e:
            self._handle_rename_user_error(e)
            return
        except Exception as e:
            self._handle_unexpected_error(e)
        else:
            self.close_window()
            self.master.close_window()
            WindowMain(
                DbConnect.db_connect(self.user),
                get_logger(self.user),
                self.user,
                self.icon,
            )

    def _handle_rename_user_error(
        self, e: RenameUserError | ValueError
    ) -> None:
        if str(e) in (
            'Outro usuário já possui este nome.',
            'O novo nome não pode estar em branco.',
            "O nome não pode conter os char's: / ou \\",
            'O novo nome não pode ser igual ao antigo.',
            'O nome antigo ainda não foi definido no app.',
        ):
            self.logger.info(f'ErroEsperado: {e}')
            self.label_steps_for_apply.configure(text=e)
        else:
            self.logger.error(f'Erro inesperado:\n{e}')
            self.label_steps_for_apply.configure(
                text=f'Desculpe ocorreu um erro interno:\n{e}'
            )

    def _handle_unexpected_error(self, e: Exception) -> None:
        """Trata erros inesperados."""
        self.logger.error(f'Erro inesperado:\n{e}')
        self.label_steps_for_apply.configure(
            text=f'Desculpe ocorreu um erro interno:\n{e}'
        )

    def close_window(self, event=None) -> None:
        """Fecha a janela de configuração."""
        self.db.close()
        self.logger.info('Fechando a janela de config.')
        self.window.destroy()


class WinMakeEnglish:
    """Classe que representa a janela que faz/salva os cards de ingles."""

    def __init__(
        self,
        master: WindowMain,
        color_theme: str,
        font: ctk.CTkFont,
        db: Connection,
        logger: Logger = get_logger(),
    ) -> None:
        """Metodo construtor da classe."""
        #
        # Iniciamos a janela
        self.logger = logger
        self.db = db
        self.color_theme = color_theme
        self.font = font
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


class WinAddCardsEnglish:
    """Class que representa a janela que add os cards de ingles no anki."""

    def __init__(
        self,
        master: str,
        color_theme: str,
        font: ctk.CTkFont,
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
        self.font = font
        self.color_theme = color_theme
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
        MainAddCardsEnglish.AddCardsEnglish(
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


class WinMakeMath:
    """Class que representa a janela que faz/salva os cards de matematica."""

    def __init__(
        self,
        master: WindowMain,
        color_theme: str,
        font: ctk.CTkFont,
        db: Connection,
        logger: Logger = get_logger(),
    ) -> None:
        """Metodo construtor da classe."""
        #
        # Informacoes da janela.
        self.logger = logger
        self.db = db
        self.master = master
        self.color_theme = color_theme
        self.font = (font,)
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
            self.logger.warning(f'InputError: {self.erro_msg}')
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
        master: WindowMain,
        color_theme: str,
        font: ctk.CTkFont,
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
        self.color_theme = color_theme
        self.font = font
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


if __name__ == '__main__':
    WindowSelectUser()
