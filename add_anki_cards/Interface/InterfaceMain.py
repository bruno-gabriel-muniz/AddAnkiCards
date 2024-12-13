from _tkinter import TclError
from logging import Logger
from os import path
from sqlite3 import Connection
from tkinter import PhotoImage, font
from typing import NoReturn

import customtkinter as ctk
from CTkListbox import CTkListbox

from add_anki_cards.Db import DbConnect, DbSearch
from add_anki_cards.Interface.Lang.InterfaceLang import (
    WinAddCardsLang,
    WinMakeEnglish,
)
from add_anki_cards.Interface.Math.InterfaceMath import (
    WinAddCardsMath,
    WinMakeMath,
)
from add_anki_cards.Interface.Tooltips import Tooltip
from add_anki_cards.logging_main import get_logger
from add_anki_cards.models.ManagerUsers.ManagerUsers import (
    ManagerUsers,
    ReadConfig,
)

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('green')


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
        data_font = self.data_config['font']
        self.font = ctk.CTkFont(
            data_font[0], size=data_font[2], weight=data_font[1]
        )
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
            self._handle_user_creation_error(error_msg)
            return None
        self.manager_users.make_user(new_name)
        self.logger.info('Atualizando a janela de login.')
        self.update_option_menu_user()
        if self.is_show_all_users_list or not new_name.startswith('.'):
            self.option_menu_users.set(new_name)
        self.label_status.configure(text=f'Usuário {new_name} foi criado.')
        self.logger.info(f'O usuário: {new_name}, foi criado.')
        self.add_user()

    def _handle_user_creation_error(self, e: ValueError) -> NoReturn:
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
        data_font = self.config['font']
        self.font = ctk.CTkFont(
            data_font[0], weight=data_font[1], size=data_font[2]
        )
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
            command=self.make_win_config_user,
            text='⚙',
            font=(self.font, 20),
            width=35,
            fg_color='transparent',
        )
        self.btn_config_user.grid(row=0, column=1, sticky='e')
        self.btn_change_user = ctk.CTkButton(
            self.menu_main,
            command=self.make_win_change_user,
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

    def make_win_change_user(self) -> NoReturn:
        self.Master.after(100, self.Master.destroy())
        self.to_change_user = True

    def make_win_config_user(self) -> NoReturn:
        WinConfigUser(
            self,
            self.icon,
            self.config,
            self.user,
            DbConnect.db_connect(self.user),
            self.logger,
        )

    def make_win_make_english(self) -> NoReturn:
        """Funcao que inicia a janela que faz/salva os cards de ingles."""
        self.logger.info('Iniciando a janela que faz/salva os cards de Inglês')
        WinMakeEnglish(
            self.Master,
            self.config,
            DbConnect.db_connect(user=self.user),
            self.logger,
        )

    def make_win_add_cards_english(self) -> NoReturn:
        """Met. que cria a janela que adciona os cartoes de ingles no anki."""
        self.logger.info('Iniciando a janela que adciona os cartoes de Inglês')
        WinAddCardsLang(
            self.Master,
            self.config,
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
            self.config,
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
            self.config,
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
        master: ctk.CTk,
        icon,
        config_user: dict[str, tuple | str],
        user: str = 'User_Default',
        db: Connection = DbConnect.db_connect(),
        logger: Logger = get_logger(),
    ) -> None:
        """
        Inicializa a classe WinConfigUser.

        Parâmetros:
            master (ctk.CTk): Janela principal.
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
        data_font = self.config['font']
        self.font = ctk.CTkFont(
            data_font[0], weight=data_font[1], size=data_font[2]
        )
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
            height=50,
            width=50,
        )
        self.tab_view_config.grid(
            row=0, column=0, padx=5, pady=5, sticky='nsew'
        )

        self.list_names_tab_view = []

        # Criando a aba de configuração de nome
        self.logger.info('Criando a aba de configuração do nome.')
        self._make_tab_username()
        self.list_names_tab_view.append('Config Name')

        # Criando a aba de configuração de tema
        self.logger.info('Criando a aba de configurção de aparencia.')
        self._make_tab_appearance()
        self.list_names_tab_view.append('Config Appearance')

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
        self.tab_name_user = ctk.CTkFrame(
            self.tab_view_config.add('Config Name'),
            width=50,
            height=50,
        )
        self.tab_name_user.pack()

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

    def _make_tab_appearance(self) -> None:
        """Cria a aba de configuração de aparência."""
        # Frame principal para a aba de aparência.
        self.logger.info('Criando a aba de configuração de aparência.')
        self.tab_appearance = ctk.CTkFrame(
            self.tab_view_config.add('Config Appearance'),
            width=250,
            height=250,
        )
        self.tab_appearance.pack()

        # Configuração de layout para o frame.
        self.tab_appearance.grid_columnconfigure(0, weight=10)
        self.tab_appearance.grid_rowconfigure((0, 2, 3), weight=10)

        # Dicionário de temas de cores disponíveis.
        color_themes = {
            'Red': '#880000',
            'Green': '#008800',
            'Blue': '#000088',
            'Purple': '#880088',
            'Yellow': '#888800',
            'Cyan': '#008888',
            'Orange': '#884400',
            'Pink': '#880044',
            'Brown': '#444400',
            'Gray': '#888888',
            'Black': '#000000',
            'White': '#ffffff',
        }

        # Rótulo e menu suspenso para alterar a cor do tema.
        self.logger.debug('Criando os componentes para alterar a cor do tema.')
        self.label_color_theme = ctk.CTkLabel(
            self.tab_appearance,
            text='Change color theme to:',
            font=self.font,
        )
        self.label_color_theme.grid(row=0, column=0, padx=3, pady=5)

        self.option_menu_color_theme = ctk.CTkOptionMenu(
            self.tab_appearance,
            values=sorted(color_themes.keys()),
            fg_color=self.color_theme,
            font=self.font,
        )
        self.option_menu_color_theme.grid(row=0, column=1, padx=3, pady=5)

        # Rótulo para configuração de fontes.
        self.label_fonts = ctk.CTkLabel(
            self.tab_appearance,
            text='Config Font',
            font=self.font,
        )
        self.label_fonts.grid(
            row=1, column=0, columnspan=2, padx=3, pady=5, sticky='nsew'
        )

        # Frame para busca de fontes.
        self.logger.debug('Criando a interface de busca de fontes.')
        self.frame_font_search = ctk.CTkFrame(
            self.tab_appearance,
            height=25,
            width=235,
        )
        self.frame_font_search.grid(
            row=2, column=0, columnspan=2, padx=3, pady=5, sticky='nsew'
        )

        self.entry_font_search = ctk.CTkEntry(
            self.frame_font_search,
            font=self.font,
            text_color=self.color_theme,
            placeholder_text_color=self.color_theme,
            placeholder_text='Search your font:',
        )
        self.entry_font_search.pack(side='left', fill='x', expand=True, padx=3)

        self.btn_font_search = ctk.CTkButton(
            self.frame_font_search,
            text='🔍︎',
            font=self.font,
            fg_color=self.color_theme,
            width=25,
        )
        self.btn_font_search.pack(side='right', padx=3)

        # Lista de fontes disponíveis.
        self.logger.debug('Criando a lista de fontes disponíveis.')
        fonts_available = sorted(font.families())
        self.listbox_fonts = CTkListbox(
            self.tab_appearance,
            font=self.font,
            width=300,
            border_color=self.color_theme,
        )
        self.listbox_fonts.grid(row=3, column=0, columnspan=2, padx=3, pady=5)

        for idx, font_name in enumerate(fonts_available[:20]):
            self.listbox_fonts.insert(idx, font_name)

        # Switch para alternar entre fontes com e sem negrito.
        self.switch_bold_font = ctk.CTkSwitch(
            self.tab_appearance,
            text='With Bold',
            onvalue=True,
            offvalue=False,
            font=self.font,
            progress_color=self.color_theme,
            fg_color='#888888',
        )
        self.switch_bold_font.select()
        self.switch_bold_font.grid(row=4, column=0)

        # Botão para aplicar a mudança de fonte.
        self.btn_apply_font = ctk.CTkButton(
            self.tab_appearance,
            text='Change Font',
            font=self.font,
            fg_color=self.color_theme,
        )
        self.btn_apply_font.grid(row=4, column=1)

    def _make_btn_label_apply(self) -> None:
        """Cria o botão e o label para aplicar as mudanças."""

        # Criando o botão que informa o que será feito no apply.
        self.logger.debug('Criando o label do apply.')
        self.txt_steps_for_apply = 'Steps for apply:\n'
        self.label_steps_for_apply = ctk.CTkLabel(
            self.window,
            text=self.txt_steps_for_apply,
            font=self.font,
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
        except ValueError as e:
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

    def _handle_rename_user_error(self, e: ValueError) -> None:
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


if __name__ == '__main__':
    WindowSelectUser()
