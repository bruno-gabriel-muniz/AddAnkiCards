import sqlite3 as sql


def DbConnect(nameDb: str = 'GeneralDB.db') -> None:
    return sql.connect(nameDb)
