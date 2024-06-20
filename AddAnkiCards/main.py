import os
import sys


def resolveBug():
    sys.path.append(os.getcwd())
    from AddAnkiCards.Db.DbConnect import DbConnect
    from AddAnkiCards.PraticingEnglish.EnglishAddAnkiCards import (
        MainAddAnkiCards,
    )

    return MainAddAnkiCards, DbConnect


MainAddAnkiCards, DbConnect = resolveBug()
MainAddAnkiCards.AddAnkiCards(DbConnect(), 3, 'cloze').addCloze()
