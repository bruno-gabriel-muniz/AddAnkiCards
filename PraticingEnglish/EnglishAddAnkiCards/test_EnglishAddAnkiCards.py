from unittest.mock import MagicMock
import unittest
import pytest
import requests
import MainAddAnkiCards
import json


def mockGeneralDB():
    """
    Funcao que faz os mocks do Db de todos os testes unitarios
    """
    mockGeneralDB = MagicMock()
    mockGeneralDB.cursor().execute(
        "SELECT FraseId, FraseOrig, FraseTrad, TagLingua FROM " +
        "FrasesNaoUsadas ORDER BY FraseId ASC LIMIT 3"
    ).fetchall.return_value = [
        (
            41,
            "Tom said that isn't true. (CK)",
            'Tom disse que não é verdade. (ajdavidl)',
            'Inglês'
        ),
        (
            42,
            'Tom said this was urgent. (CK)',
            'O Tom disse que isso era urgente. (MarlonX19)',
            'Inglês'
        ),
        (
            43,
            'Tom said you were hungry. (CK)',
            'Tom disse que você estava com fome. (bill)',
            'Inglês'
        )]
    mockGeneralDB.cursor.execute.return_value = None
    return mockGeneralDB


def deletaCardsTestById(idCardsTeste):
    """
    Funcao que deleta os cards feitos nos testes atraves do Id

    idCardsTeste: lista com os numeros dos Id's
    """
    requisisao = {
        'action': "deleteNotes",
        'params':
            {
                'notes': idCardsTeste
            },
        'version': 6
    }
    requisisao = json.dumps(requisisao)
    resultado = requests.post('http://127.0.0.1:8765', requisisao)


def test_simpleAddCloze():
    """
    Funcao que testa a conexao com o programa e a api do Anki-Connect
    """
    test = MainAddAnkiCards.AddAnkiCards(mockGeneralDB(), 3, "cloze")
    resultTest = test.addCloze()
    resultTestError = [resultTest[0]['error'],
                       resultTest[1]['error'], resultTest[2]['error']]
    resultTestId = [resultTest[0]['result'],
                    resultTest[1]['result'], resultTest[2]['result']]
    assert resultTestError == [None, None, None]
    deletaCardsTestById(resultTestId)


if __name__ == '__main__':
    unittest.main()
