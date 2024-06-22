import sqlite3 as sql


def DbConnect(nameDb: str = 'GeneralDB.db') -> sql.connect:
    return sql.connect(nameDb)
