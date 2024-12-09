import json
import logging
from unittest.mock import MagicMock

import pytest
import requests

from add_anki_cards.logging_main import get_logger
from add_anki_cards.models.Lang.AddCardsLang import MainAddCardsLang

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


def mock_db():
    """
    Funcao que faz os mocks do Db de todos os testes unitarios
    """
    global exemplos
    mock_db = MagicMock()
    mock_db.cursor().execute().fetchall.return_value = [
        exemplos['exemplo1'],
        exemplos['exemplo2'],
        exemplos['exemplo3'],
    ]
    return mock_db


def delete_cards_test_by_id(id_cards_teste: list[int]):
    """
    Funcao que deleta os cards feitos nos testes atraves do Id

    id_cards_teste: lista com os numeros dos Id's
    """
    requisisao = {
        'action': 'deleteNotes',
        'params': {'notes': id_cards_teste},
        'version': 6,
    }
    requisisao = json.dumps(requisisao)
    requests.post('http://127.0.0.1:8765', requisisao)


@pytest.mark.NotQuick
@pytest.mark.Anki
def test_simple_add_cloze_integrate_anki_connect(caplog):
    """
    Funcao que testa a conexao com o programa e a api do Anki-Connect
    """
    caplog.set_level(logging.DEBUG)
    test = MainAddCardsLang.AddCardsLang(3, db=mock_db())
    result_test = test.add_cards()
    result_test_error = [
        result_test[0]['error'],
        result_test[1]['error'],
        result_test[2]['error'],
    ]
    result_test_id = [
        result_test[0]['result'],
        result_test[1]['result'],
        result_test[2]['result'],
    ]
    assert result_test_error == [None, None, None]
    delete_cards_test_by_id(result_test_id)


def test_format_cards_add_cloze(caplog):
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
    test = MainAddCardsLang.AddCardsLang(3, db=mock_db())
    results = []
    for frase_test in range(3):
        results.append(test.format_text_card_cloze(frase_test))
    #
    # verificando a formatacao
    format_espec = [
        f"""id: {exemplos['exemplo1'][0]}<br>
{{{{c2::{exemplos['exemplo1'][1]}}}}} -> {{{{c2::[sound:AddCardsAudio{exemplos[
            'exemplo1'][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c1::{exemplos['exemplo1'][2]}}}}}
    </ul>
""",
        f"""id: {exemplos['exemplo2'][0]}<br>
{{{{c2::{exemplos['exemplo2'][1]}}}}} -> {{{{c2::[sound:AddCardsAudio{exemplos[
            'exemplo2'][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c1::{exemplos['exemplo2'][2]}}}}}
    </ul>
""",
        f"""id: {exemplos['exemplo3'][0]}<br>
{{{{c2::{exemplos['exemplo3'][1]}}}}} -> {{{{c2::[sound:AddCardsAudio{exemplos[
            'exemplo3'][0]:0>6}.mp3]}}}}
    <ul>
    {{{{c1::{exemplos['exemplo3'][2]}}}}}
    </ul>
""",
    ]
    print(*results, *format_espec)
    assert results == format_espec
