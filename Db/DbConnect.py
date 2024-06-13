import sqlite3 as sql


class DbConnect():
    def __init__(self, nameDb: str = "GeneralDB.db") -> None:
        self.DbConnect = sql.connect(nameDb)
