from AddAnkiCards.Db import DbConnect


class DbResearcher(object):
    """
    Classe que realiza as pesquisas no banco de dados
    """

    def __init__(self, DbConnect=DbConnect.DbConnect()) -> None:
        # Primeiro, nos conectamos ao banco de dados.
        self.DbConnect = DbConnect
        self.DbCursor = self.DbConnect.cursor()
        #
        # Depois, iniciamos os bancos de dados caso
        # seja o primeiro acesso do usuario.
        self.DbCursor.execute(
            'CREATE TABLE IF NOT EXISTS FrasesNaoUsadas (FraseId INTEGER PRIM'
            + 'ARY KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, '
            + 'TagLingua TEXT);'
        )
        self.DbCursor.execute(
            'CREATE TABLE IF NOT EXISTS FrasesUsadas (FraseId INTEGER PRIMARY '
            + 'KEY AUTOINCREMENT, FraseOrig TEXT, FraseTrad TEXT, '
            + 'TagLingua TEXT);'
        )
        self.DbCursor.execute(
            'CREATE TABLE IF NOT EXISTS TipoCardsCalculoMental'
            + ' (IdTipo INTEGER PRIMARY KEY AUTOINCREMENT,'
            + ' TipoOperacao TEXT KEY, DoisIntervalos INTEGER, Intervalo TEXT,'
            + ' NumNotes INTEGER, NumNotesFree INTEGER, '
            + 'NumCardsForNotes NUMBER)'
        )
        self.DbCursor.execute(
            'CREATE TABLE IF NOT EXISTS CardsCalculoMental'
            + ' (IdCard INTEGER NOT NULL,'
            + ' NomeCard TEXT NOT NULL, Card TEXT NOT NULL,'
            + ' NumCards INTEGER NOT NULL, DataPriRev TEXT NOT NULL,'
            + ' TipoCard INTEGER NOT NULL, FOREIGN KEY (TipoCard)'
            + ' REFERENCES TipoCardsCalculoMental(IdTipo))'
        )

    def countNotesOfEnglish(self) -> tuple:
        """
        Metodo que conta a quantidade de notas de ingles.

        Alem de dividir elas entre as que foram adicionadas,
        as que estao disponiveis (armazenadas) e o total delas.
        """
        #
        # Primeiramente, criamos uma variavel que possui e supoe que
        # o maior id das frases usadas corresponde a soma de todas
        numNotesAdded = self.DbCursor.execute(
            'SELECT FraseId FROM FrasesUsadas ORDER BY FraseId DESC LIMIT 1'
        ).fetchall()
        #
        # Depois verificamos se a tabela das frases nao usadas estava vazia
        if len(numNotesAdded) != 0:
            numNotesAdded = numNotesAdded[0][0]
        else:
            # E caso estivessse concluimos que nenhuma
            # nota/frase foi usada ainda
            numNotesAdded = 0
        #
        # Fazemos a mesma coisa para as frases nao usadas,
        # supondo que o maior id represente o numero de todas as frases
        numAllCards = self.DbCursor.execute(
            'SELECT FraseId FROM FrasesNaoUsadas ORDER BY FraseId DESC LIMIT 1'
        ).fetchall()
        if len(numAllCards) != 0:
            numAllCards = numAllCards[0][0]
        else:
            numAllCards = numNotesAdded
        #
        # E caulamos os numeros de notas/frases armazenadas (ou nao usadas)
        # a partir da diferenca entre o total e as frases usadas. Ja que,
        # so se pode usar ou nao usar as frases e nao existe uma possibilidade
        # alem dessas duas.
        numNotesStored = numAllCards - numNotesAdded
        return numNotesAdded, numNotesStored, numAllCards

    def countCardsOfMath(self) -> tuple:
        """
        Metodo que descobre o total de cartoes de matematica.
        """
        #
        # Primeiramente, selecionamos as informacoes de todas as notas
        # dos diferentes tipos delas.
        dataCardsMath = self.DbCursor.execute(
            'SELECT NumNotes, NumNotesFree, NumCardsForNotes '
            + 'FROM TipoCardsCalculoMental'
        ).fetchall()
        #
        # E passamos por cada tipo de nota somando
        # o numero de cards por notas * o total de notas e
        # fazendo a mesma coisa para as notas que ainda nao foram adicionadas
        # no Anki.
        AllCardsMath = 0  # variavel que soma todos os cartoes
        StoredCardsMath = 0  # variavel que soma todos cards nao usados
        for data in dataCardsMath:
            AllCardsMath += data[0] * data[2]
            StoredCardsMath += data[1] * data[2]
        #
        # Finalmente, encontramos o numero de notas adcionadas
        # atraves da subtracao do total pela quantidade de notas livres.
        AddedCardsMath = AllCardsMath - StoredCardsMath
        #
        return AddedCardsMath, StoredCardsMath, AllCardsMath
