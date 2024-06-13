from Db.DbConnect import DbConnect
from MathTraining.MakesCombinations import *
from PraticingEnglish.EnglishAddAnkiCards import MainAddAnkiCards

Test = MainAddAnkiCards.AddAnkiCards(DbConnect(), 3, "cloze")
Test.addCloze()
