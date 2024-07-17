import sqlite3 as sql


def DbConnect(nameDb: str = 'GeneralDB.db') -> sql.Connection:
    return sql.connect(nameDb)
