import sqlite3 as sql

from add_anki_cards.Db import DbConnect


class DbResearcher:
    """Classe que realiza as pesquisas no banco de dados."""

    def __init__(
        self,
        db: sql.Connection | sql.Cursor = DbConnect.db_connect(),
    ) -> None:
        """Metodo construtor da classe."""
        # Primeiro, nos conectamos ao banco de dados.
        self.db = db
        self.db_cursor = self.db.cursor()
        #
        # Depois, iniciamos os bancos de dados caso
        # seja o primeiro acesso do usuario.
        self.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS FrasesNaoUsadas (FraseId INTEGER PRIM'
            + 'ARY KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, '
            + 'TagLingua TEXT);'
        )
        self.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS FrasesUsadas (FraseId INTEGER PRIMARY '
            + 'KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, '
            + 'TagLingua TEXT);'
        )
        self.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS TipoCardsCalculoMental'
            + ' (IdTipo INTEGER PRIMARY KEY AUTOINCREMENT,'
            + ' TipoOperacao TEXT KEY, DoisIntervalos INTEGER, Intervalo TEXT,'
            + ' NumNotes INTEGER, NumNotesFree INTEGER, '
            + 'NumCardsForNotes NUMBER)'
        )
        self.db_cursor.execute(
            'CREATE TABLE IF NOT EXISTS CardsCalculoMental'
            + ' (IdCard INTEGER NOT NULL,'
            + ' NomeCard TEXT NOT NULL, Card TEXT NOT NULL,'
            + ' NumCards INTEGER NOT NULL, DataPriRev TEXT NOT NULL,'
            + ' TipoCard INTEGER NOT NULL, FOREIGN KEY (TipoCard)'
            + ' REFERENCES TipoCardsCalculoMental(IdTipo))'
        )

    def count_notes_of_english(self) -> tuple:
        """Metodo que conta a quantidade de notas de ingles.

        Alem de dividir elas entre as que foram adicionadas,
        as que estao disponiveis (armazenadas) e o total delas.
        """
        #
        # Primeiramente, criamos uma variavel que possui e supoe que
        # o maior id das frases usadas corresponde a soma de todas
        num_notes_added = self.db_cursor.execute(
            'SELECT FraseId FROM FrasesUsadas ORDER BY FraseId DESC LIMIT 1'
        ).fetchall()
        #
        # Depois verificamos se a tabela das frases nao usadas estava vazia
        if len(num_notes_added) != 0:
            num_notes_added = num_notes_added[0][0]
        else:
            # E caso estivessse concluimos que nenhuma
            # nota/frase foi usada ainda
            num_notes_added = 0
        #
        # Fazemos a mesma coisa para as frases nao usadas,
        # supondo que o maior id represente o numero de todas as frases
        num_all_cards = self.db_cursor.execute(
            'SELECT FraseId FROM FrasesNaoUsadas ORDER BY FraseId DESC LIMIT 1'
        ).fetchall()
        if len(num_all_cards) != 0:
            num_all_cards = num_all_cards[0][0]
        else:
            num_all_cards = num_notes_added
        #
        # E caulamos os numeros de notas/frases armazenadas (ou nao usadas)
        # a partir da diferenca entre o total e as frases usadas. Ja que,
        # so se pode usar ou nao usar as frases e nao existe uma possibilidade
        # alem dessas duas.
        num_notes_stored = num_all_cards - num_notes_added
        return num_notes_added, num_notes_stored, num_all_cards

    def count_cards_of_math(self) -> tuple:
        """Metodo que descobre o total de cartoes de matematica."""
        #
        # Primeiramente, selecionamos as informacoes de todas as notas
        # dos diferentes tipos delas.
        data_cards_math = self.db_cursor.execute(
            'SELECT NumNotes, NumNotesFree, NumCardsForNotes '
            + 'FROM TipoCardsCalculoMental'
        ).fetchall()
        #
        # E passamos por cada tipo de nota somando
        # o numero de cards por notas * o total de notas e
        # fazendo a mesma coisa para as notas que ainda nao foram adicionadas
        # no Anki.
        all_cards_math = 0  # variavel que soma todos os cartoes
        stored_cards_math = 0  # variavel que soma todos cards nao usados
        for data in data_cards_math:
            all_cards_math += data[0] * data[2]
            stored_cards_math += data[1] * data[2]
        #
        # Finalmente, encontramos o numero de notas adcionadas
        # atraves da subtracao do total pela quantidade de notas livres.
        added_cards_math = all_cards_math - stored_cards_math
        #
        return added_cards_math, stored_cards_math, all_cards_math


def generic_search(
    query: str,
    db: sql.Connection | sql.Cursor = DbConnect.db_connect(),
) -> list[list]:
    """
    Func. que faz uma busca generica no DB e retorna o resultado numa lista.

    Entrada: qualquer busca na linquagem sql em string, o nome do DB em str
    Saida: resultado da pesquisa em uma lista
    """
    result = db.execute(query)
    db.commit()
    return list(map(list, result.fetchall()))
