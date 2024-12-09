import os
from os import path


def init_app():
    home_path = path.expanduser('~')
    data_path = path.join(home_path, '.AddAnkiCardsData', 'User_Default')
    if not path.exists(data_path):
        os.makedirs(data_path)
    if not path.exists(path.join(path.dirname(data_path), '.Test')):
        os.makedirs(path.join(path.dirname(data_path), '.Test'))
    from add_anki_cards.Interface.InterfaceMain import WindowSelectUser

    WindowSelectUser()


init_app()
