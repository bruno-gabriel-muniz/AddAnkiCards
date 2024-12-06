import sqlite3 as sql
from os import path


def db_connect(
    name_db: str = 'GeneralDB.db', user: str = 'User_Default'
) -> sql.Connection:
    home_path = path.expanduser('~')
    return sql.connect(
        path.join(home_path, '.AddAnkiCardsData', user, name_db)
    )
