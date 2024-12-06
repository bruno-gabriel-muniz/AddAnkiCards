import json
import os
from typing import Literal, Union

from customtkinter import CTkFont


def make_config_default(
    data_path: str | None,
    name_user: str | None,
    only_dict: bool = False,
) -> None | dict[str, Union[str, tuple]]:
    """Func. q. inicializa as config's padrões."""
    config_default = {
        'font': ('Poppins', 'bold', 12),
        'color_theme': '#00AA00',
        'theme_dark_or_ligth': 'dark',
    }
    if only_dict:
        return config_default
    path_to_config = os.path.join(data_path, name_user, 'config.json')
    with open(path_to_config, 'w') as config:
        json.dump(config_default, config, indent=4)


class ManagerUsers:
    """Gerencia operações relacionadas aos usuários."""

    def __init__(self, data_path: str | None = None):
        """
        Inicializa a classe ManagerUsers.

        Args:
            data_path (str): Caminho para o diretório de dados.
        """
        if data_path is None:
            home = os.path.expanduser('~')
            self.data_path = os.path.join(home, '.AddAnkiCardsData')
        else:
            self.data_path = data_path
        self.all_users_list = []
        self.users_list = []
        self.hidden_users_list = []

    def new_name_user_is_valid(
        self,
        new_name: str,
        old_name: str = 'User_Default',
    ) -> tuple[bool, Exception | None]:
        self.load_users(have_return=False)
        if old_name not in self.all_users_list:
            return (
                False,
                ValueError('O nome antigo ainda não foi definido no app.'),
            )
        if new_name == '' or new_name.isspace():
            return (
                False,
                ValueError('O novo nome não pode estar em branco.'),
            )
        if new_name == old_name:
            return (
                False,
                ValueError('O novo nome não pode ser igual ao antigo.'),
            )
        if new_name == 'User_Default':
            return (
                False,
                ValueError(
                    'O novo nome não pode ser igual ao do usuário padrão.'
                ),
            )
        if '/' in new_name or '\\' in new_name:
            return (
                False,
                ValueError(
                    "O nome não pode conter os char's: / ou \\",
                ),
            )
        if new_name in self.all_users_list:
            return (
                False,
                ValueError('Outro usuário já possui este nome.'),
            )
        return (True, None)

    def load_users(
        self,
        have_return: bool = True,
    ) -> (tuple[list[str], list[str], list[str]]) | None:
        """
        Carrega e categoriza os usuários em listas.

        Returns:
            tuple: Contém listas de todos, visíveis e ocultos.
        """
        self.all_users_list = os.listdir(self.data_path)
        self.users_list = [
            user for user in self.all_users_list if not user.startswith('.')
        ]
        self.hidden_users_list = [
            user for user in self.all_users_list if user.startswith('.')
        ]
        if have_return:
            return self.all_users_list, self.users_list, self.hidden_users_list
        return None

    def make_user(self, name_new_user: str) -> None:
        """
        Cria um novo usuário se o nome não estiver em uso.

        Args:
            name_new_user (str): Nome do novo usuário.

        Raises:
            UserCreationError: Se o nome já estiver em uso.
        """
        name_is_valid, error = self.new_name_user_is_valid(name_new_user, '')
        if not name_is_valid:
            raise error
        os.makedirs(os.path.join(self.data_path, name_new_user))
        make_config_default(self.data_path, name_new_user)

    def rename_user(
        self,
        old_user_name: str,
        new_user_name: str,
    ) -> None:
        """
        Renomeia um usuário existente.

        Args:
            old_user_name (str): Nome atual do usuário.
            new_user_name (str): Novo nome desejado.

        Raises:
            ValueError: Se o novo nome já estiver em uso.
        """
        name_is_valid, error_msg = self.new_name_user_is_valid(
            new_user_name,
            old_user_name,
        )
        if not name_is_valid:
            raise error_msg
        os.rename(
            os.path.join(self.data_path, old_user_name),
            os.path.join(self.data_path, new_user_name),
        )
        if old_user_name == 'User_Default':
            make_config_default(self.data_path, new_user_name)


class ReadConfig:
    def __init__(self, name_user: str, data_path: str) -> None:
        self.user = name_user
        if self.user in ('User_Default', 'Test', '.Test'):
            config_default = make_config_default(
                None,
                None,
                True,
            )
            self.font = config_default['font']
            self.color_theme = config_default['color_theme']
            self.theme_dark_or_ligth: Literal[
                'light', 'dark'
            ] = config_default['theme_dark_or_ligth']
        else:
            path_to_config = os.path.join(
                data_path,
                name_user,
                'config.json',
            )
            with open(path_to_config, 'r') as config:
                data_config = json.load(config)
            self.font = data_config['font']
            self.color_theme = data_config['color_theme']
            self.theme_dark_or_ligth: Literal['light', 'dark'] = data_config[
                'theme_dark_or_ligth'
            ]
        self.dict_data = {}
        self.dict_data['font'] = self.font
        self.dict_data['color_theme'] = self.color_theme
        self.dict_data['theme_dark_or_ligth'] = self.theme_dark_or_ligth
        self.dict_data['user'] = self.user

    def get(self) -> dict[str, Union[CTkFont, tuple, str]]:
        return self.dict_data
