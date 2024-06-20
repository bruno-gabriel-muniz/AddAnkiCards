import json
import logging
from unittest.mock import MagicMock

import pytest
import requests

from AddAnkiCards.logginMain import get_logger
from AddAnkiCards.PraticingEnglish.EnglishAddAnkiCards import MainAddAnkiCards

logger = get_logger()


exemplos = {
    'exemplo1': (
        41,
        "Tom said that isn't true. (CK)",
        'Tom disse que nao é verdade. (ajdavidl)',
        'Inglês',
    ),
    'exemplo2': (
        42,
        'Tom said this was urgent. (CK)',
        'O Tom disse que isso era urgente. (MarlonX19)',
        'Inglês',
    ),
    'exemplo3': (
        43,
        'Tom said you were hungry. (CK)',
        'Tom disse que você estava com fome. (bill)',
        'Inglês',
    ),
}


def mockGeneralDB():
    """
    Funcao que faz os mocks do Db de todos os testes unitarios
    """
    global exemplos
    mockGeneralDB = MagicMock()
    mockGeneralDB.cursor().execute(
        'SELECT FraseId, FraseOrig, FraseTrad, TagLingua FROM '
        + 'FrasesNaoUsadas ORDER BY FraseId ASC LIMIT 3'
    ).fetchall.return_value = [
        exemplos['exemplo1'],
        exemplos['exemplo2'],
        exemplos['exemplo3'],
    ]
    mockGeneralDB.cursor.execute.return_value = None
    return mockGeneralDB


def deletaCardsTestById(idCardsTeste):
    """
    Funcao que deleta os cards feitos nos testes atraves do Id

    idCardsTeste: lista com os numeros dos Id's
    """
    requisisao = {
        'action': 'deleteNotes',
        'params': {'notes': idCardsTeste},
        'version': 6,
    }
    requisisao = json.dumps(requisisao)
    requests.post('http://127.0.0.1:8765', requisisao)


@pytest.mark.NotQuick
@pytest.mark.Anki
def test_simple_AddCloze_Integrate_Anki_Connect(caplog):
    """
    Funcao que testa a conexao com o programa e a api do Anki-Connect
    """
    caplog.set_level(logging.DEBUG)
    test = MainAddAnkiCards.AddAnkiCards(mockGeneralDB(), 3, 'cloze')
    resultTest = test.addCloze()
    resultTestError = [
        resultTest[0]['error'],
        resultTest[1]['error'],
        resultTest[2]['error'],
    ]
    resultTestId = [
        resultTest[0]['result'],
        resultTest[1]['result'],
        resultTest[2]['result'],
    ]
    assert resultTestError == [None, None, None]
    deletaCardsTestById(resultTestId)


def test_format_Cards_AddCloze(caplog):
    """
    Funcao que testa a formatacao dos cartoes
    """
    # imporatando os exemplos
    global exemplos, logger
    #
    # Capitura os logs
    caplog.set_level(logging.DEBUG)
    #
    # rodando o teste
    test = MainAddAnkiCards.AddAnkiCards(mockGeneralDB(), 3, 'cloze')
    results = []
    for fraseTest in range(3):
        results.append(test.formatTextCardCloze(fraseTest))
    #
    # verificando a formatacao
    formatEspec = [
        f"""id: {exemplos['exemplo1'][0]}<br>
{{{{c1::{exemplos['exemplo1'][1]}}}}} -> {{{{c1::[sound:AddCardsAudio{exemplos[
            'exemplo1'][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c2::{exemplos['exemplo1'][2]}}}}}
    </ul>
""",
        f"""id: {exemplos['exemplo2'][0]}<br>
{{{{c1::{exemplos['exemplo2'][1]}}}}} -> {{{{c1::[sound:AddCardsAudio{exemplos[
            'exemplo2'][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c2::{exemplos['exemplo2'][2]}}}}}
    </ul>
""",
        f"""id: {exemplos['exemplo3'][0]}<br>
{{{{c1::{exemplos['exemplo3'][1]}}}}} -> {{{{c1::[sound:AddCardsAudio{exemplos[
            'exemplo3'][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c2::{exemplos['exemplo3'][2]}}}}}
    </ul>
""",
    ]
    assert results == formatEspec
