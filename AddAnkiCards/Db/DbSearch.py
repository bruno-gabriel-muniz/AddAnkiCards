from AddAnkiCards.Db import DbConnect


class DbResearcher(object):
    """
    Classe que realiza as pesquisas no banco de dados
    """

    def __init__(self, DbConnect=DbConnect.DbConnect()) -> None:
        self.DbConnect = DbConnect
        self.DbCursor = self.DbConnect.cursor()

    def countNotesOfEnglish(self) -> tuple:
        """
        Metodo que conta a quantidade de notas de ingles.

        Alem de dividir elas entre as que foram adicionadas,
        as que estao disponiveis (armazenadas) e o total delas.
        """
        numNotesAdded = self.DbCursor.execute(
            'SELECT FraseId FROM FrasesUsadas ORDER BY FraseId DESC LIMIT 1'
        ).fetchall()[0][0]
        numAllCards = self.DbCursor.execute(
            'SELECT FraseId FROM FrasesNaoUsadas ORDER BY FraseId DESC LIMIT 1'
        ).fetchall()[0][0]
        numNotesStored = numAllCards - numNotesAdded
        return numNotesAdded, numNotesStored, numAllCards

    def countCardsOfMath(self) -> tuple:
        # descobrindo o total de cartoes
        dataCardsMath = self.DbCursor.execute(
            'SELECT NumNotes, NumNotesFree, NumCardsForNotes '
            + 'FROM TipoCardsCalculoMental'
        ).fetchall()
        AllCardsMath = 0
        StoredCardsMath = 0
        for data in dataCardsMath:
            AllCardsMath += data[0] * data[2]
            StoredCardsMath += data[1] * data[2]
        AddedCardsMath = AllCardsMath - StoredCardsMath
        return AddedCardsMath, StoredCardsMath, AllCardsMath
