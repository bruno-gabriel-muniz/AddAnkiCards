import sqlite3 as sql
import ReadSaveCards as ReadSaveCards
import os
import os.path as path


def armazenaSQLite(lista_pag_entrada):
    """
    Função Que armazenas as frases em um banco de
    dados SQLite e cria as tabelas dele.
    """
    # Conectando No Banco de Dados
    FrasesDB = sql.connect("GeneralDB.db")
    # Criando as tabelas de frases usadas e não usadas, caso  não existam
    FrasesDB.execute(
        "CREATE TABLE IF NOT EXISTS FrasesNaoUsadas (FraseId INTEGER PRIM" +
        "ARY KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, TagLingua" +
        " TEXT);")
    FrasesDB.execute(
        "CREATE TABLE IF NOT EXISTS FrasesUsadas (FraseId INTEGER PRIMARY " +
        "KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, TagLingua TEXT);")
    # inserindo as frases e as traduções no banco de dados
    # das frases não usadas
    for frase_e_tradução in lista_pag_entrada:
        FrasesDB.execute(
            "INSERT INTO FrasesNaoUsadas (FraseOrig, FraseTrad, TagLingua)" +
            " VALUES (\"{}\", \"{}\", \"Inglês\");".format(
                frase_e_tradução[0],
                frase_e_tradução[1]))
    FrasesDB.commit()
    FrasesDB.close()
