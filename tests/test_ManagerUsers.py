import os
from os import path
from unittest.mock import mock_open, patch

import pytest

from add_anki_cards.models.ManagerUsers.ManagerUsers import (
    ManagerUsers,
    ReadConfig,
    make_config_default,
)


@pytest.fixture
def manager():
    """Fixture para inicializar o ManagerUsers com dados de teste."""
    return ManagerUsers(data_path='/fake/path')


@pytest.fixture
def default_users():
    """Fixture para usuários padrão."""
    return ['User_Default', '.Test']


def test_init_manager_users():
    """
    Testa a iniciacao da classe manager.

    - Garante que a classe eh iniciado corretamente.
    - Verifica se o caminho para os dados eh correto.
    """
    with patch('os.path.expanduser', return_value='/mock/home'):
        test = ManagerUsers()
        expected = path.join(os.sep, 'mock', 'home', '.AddAnkiCardsData')
        assert isinstance(test, ManagerUsers)
        assert test.data_path == expected
    test = ManagerUsers('Algum/path/')
    expected = 'Algum/path/'
    assert isinstance(test, ManagerUsers)
    assert test.data_path == expected


@patch(
    'os.listdir',
    return_value=['User_Default', '.Test', 'User1', '.HiddenUser'],
)
def test_new_name_user_is_valid(mock_listdir, manager, default_users):
    """
    Testa a validação de nomes para novos usuários.

    - Garante que nomes válidos sejam aceitos.
    - Verifica mensagens de erro para nomes inválidos:
        - Nome vazio.
        - Nome igual aos padrões ou já existentes.
        - Nome com caracteres inválidos.
        - Nome antigo não definido no app.
    """
    # Nome válido
    valid, error = manager.new_name_user_is_valid('NewUser')
    assert valid
    assert error is None

    # Antigo nome inexistente
    valid, error = manager.new_name_user_is_valid('pass', 'NotDefinid')
    assert not valid
    assert isinstance(error, ValueError)
    assert 'O nome antigo ainda não foi definido no app.' in str(error)

    # Nome vazio
    valid, error = manager.new_name_user_is_valid('')
    assert not valid
    assert isinstance(error, ValueError)
    assert str(error) == 'O novo nome não pode estar em branco.'

    # Nome igual ao padrão
    for user in default_users:
        valid, error = manager.new_name_user_is_valid(user, 'User1')
        assert not valid
        assert isinstance(error, ValueError)
        assert str(error) in (
            'Outro usuário já possui este nome.',
            'O novo nome não pode ser igual ao do usuário padrão.',
        )

    # Alterando para o mesmo nome
    valid, error = manager.new_name_user_is_valid('User1', 'User1')
    assert not valid
    assert isinstance(error, ValueError)
    assert 'O novo nome não pode ser igual ao antigo.' in str(error)

    # Nome existente
    valid, error = manager.new_name_user_is_valid('User1')
    assert not valid
    assert isinstance(error, ValueError)
    assert 'Outro usuário já possui este nome.' in str(error)

    # Nome com carcteres inválidos
    valid, error = manager.new_name_user_is_valid(
        'OI/OutraPasta\\eTalvezOutra'
    )
    assert not valid
    assert isinstance(error, ValueError)
    assert "O nome não pode conter os char's: / ou \\" in str(error)


@patch(
    'os.listdir',
    return_value=['User_Default', '.Test', 'User1', '.HiddenUser'],
)
def test_load_users(mock_listdir, manager):
    """
    Testa o carregamento e categorização de usuários.

    - Garante que a função separa corretamente:
        - Todos os usuários.
        - Usuários visíveis.
        - Usuários ocultos.
    """
    all_users, visible_users, hidden_users = manager.load_users()
    assert set(all_users) == {'User_Default', '.Test', 'User1', '.HiddenUser'}
    assert set(visible_users) == {'User_Default', 'User1'}
    assert set(hidden_users) == {'.Test', '.HiddenUser'}


@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
def test_make_user(mock_open, mock_makedirs, manager):
    """
    Testa a criação de novos usuários.

    - Verifica:
        - Diretórios criados corretamente.
        - Arquivo de configuração gerado.
    - Simula erros de nome inválido.
    """
    # Nome válido
    with patch.object(
        manager, 'new_name_user_is_valid', return_value=(False, None)
    ):
        manager.make_user('NewUser')
        mock_makedirs.assert_called_with(
            path.join(os.sep, 'fake', 'path', 'NewUser')
        )
        mock_open.assert_called_with(
            path.join(os.sep, 'fake', 'path', 'NewUser', 'config.json'), 'w'
        )

    # Nome inválido
    with patch.object(
        manager,
        'new_name_user_is_valid',
        return_value=(True, ValueError('Erro ao criar')),
    ):
        with pytest.raises(ValueError, match='Erro ao criar'):
            manager.make_user('InvalidUser')


@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
def test_rename_common_user(mock_open, mock_rename, manager):
    """
    Testa a renomeação de um usuário comum.

    - Verifica se o nome antigo é corretamente alterado para o novo.
    - Garante que a validação de nome seja chamada e aceita nomes válidos.
    - Simula erros ao validar ou renomear, garantindo que sejam levantadas as
      exceções esperadas.
    """
    with patch.object(
        manager, 'new_name_user_is_valid', return_value=(True, None)
    ):
        manager.rename_user('NomeAntigo', 'NomeNovo')
        mock_rename.assert_called_with(
            path.join(manager.data_path, 'NomeAntigo'),
            path.join(manager.data_path, 'NomeNovo'),
        )
        mock_open.assert_not_called()

    with patch.object(
        manager,
        'new_name_user_is_valid',
        return_value=(False, ValueError('Erro ao criar')),
    ):
        with pytest.raises(ValueError, match='Erro ao criar'):
            manager.rename_user('InvalidUser', 'InvalidUser')


@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
def test_rename_default_user(mock_open, mock_rename, manager):
    """
    Testa a renomeação de um usuário padrão.

    - Verifica se o nome do usuário padrão pode ser alterado para um novo nome.
    - Garante que o arquivo de configuração do novo usuário seja criado
      corretamente.
    """
    # Renomeando o User_Default
    with patch.object(
        manager, 'new_name_user_is_valid', return_value=(True, None)
    ):
        manager.rename_user('User_Default', 'NomeNovo')
        mock_rename.assert_called_with(
            path.join(manager.data_path, 'User_Default'),
            path.join(manager.data_path, 'NomeNovo'),
        )
        mock_open.assert_called_with(
            path.join(os.sep, manager.data_path, 'NomeNovo', 'config.json'),
            'w',
        )


@patch('builtins.open', new_callable=mock_open)
def test_make_config_default(mock_open):
    """
    Testa a função que cria configurações padrão.

    - Verifica retorno do dicionário de configurações padrão.
    - Garante que o arquivo de configuração seja salvo corretamente.
    """
    # Testando apenas retorno do dicionário
    result = make_config_default(None, None, only_dict=True)
    assert result['font'] == ('Poppins', 'bold', 12)
    assert result['color_theme'] == '#008800'

    # Testando escrita do arquivo
    make_config_default(
        path.join(os.sep, 'fake', 'path'),
        'NewUser',
    )
    mock_open.assert_called_with(
        path.join(os.sep, 'fake', 'path', 'NewUser', 'config.json'), 'w'
    )


@patch(
    'builtins.open',
    new_callable=mock_open,
    read_data=('{"font": ["Arial", "bold", 14], "color_theme": "#FF0000"}'),
)
def test_read_config(mock_open):
    """
    Testa a leitura de configurações de usuários.

    - Garante que:
        - Configurações padrão sejam carregadas para usuários padrão.
        - Configurações de arquivo sejam corretamente interpretadas.
    """
    # Configuração padrão
    config = ReadConfig('User_Default', path.join(os.sep, 'fake', 'path'))
    assert config.font == ('Poppins', 'bold', 12)
    assert config.color_theme == '#008800'

    # Configuração do arquivo
    config = ReadConfig('TestUser', path.join(os.sep, 'fake', 'path'))
    assert config.color_theme == '#FF0000'
    assert config.font == ['Arial', 'bold', 14]
