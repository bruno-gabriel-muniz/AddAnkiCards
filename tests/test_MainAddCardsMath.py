import json
from unittest.mock import MagicMock

import pytest
import requests

from add_anki_cards.MathTraining.AddCardsMath import MainAddCardsMath

casos_de_test = {
    'caso1Simple': [
        '''<h2>Treinamento_de_sub_entre_1-9_id_1</h2>
<p>_8 - _3 = {{c1::_5__}}|----------|_9 - _2 = {{c2::_7__}}<br>

_9 - _7 = {{c3::_2__}}|----------|_1 - _1 = {{c4::_0__}}<br>

_1 - _5 = {{c5::_-4_}}|----------|_9 - _1 = {{c6::_8__}}<br>

_6 - _3 = {{c7::_3__}}|----------|_9 - _6 = {{c8::_3__}}<br>

_4 - _7 = {{c9::_-3_}}|----------|
''', 1
    ],
    'caso2Simple': ['''<h2>Treinamento_de_sub_entre_1-9_id_2</h2>
<p>_8 - _9 = {{c1::_-1_}}|----------|_7 - _7 = {{c2::_0__}}<br>

_2 - _5 = {{c3::_-3_}}|----------|_7 - _6 = {{c4::_1__}}<br>

_4 - _1 = {{c5::_3__}}|----------|_5 - _6 = {{c6::_-1_}}<br>

_2 - _6 = {{c7::_-4_}}|----------|_7 - _2 = {{c8::_5__}}<br>

_5 - _5 = {{c9::_0__}}|----------|
''', 2
                    ]
}


def mock_db() -> MagicMock:
    global casos_de_test
    mock_db = MagicMock()
    mock_db.cursor().execute().fetchall.side_effect = [
        [
            casos_de_test['caso1Simple'],  casos_de_test['caso2Simple']
        ],
        [[4]],
    ]
    return mock_db


def delete_cards_test_by_id(id_cards_teste: list[int]):
    """
    Funcao que deleta os cards feitos nos testes atraves do Id

    idCardsTeste: lista com os numeros dos Id's
    """
    requisisao = {
        'action': 'deleteNotes',
        'params': {'notes': id_cards_teste},
        'version': 6,
    }
    requisisao = json.dumps(requisisao)
    requests.post('http://127.0.0.1:8765', requisisao)


@pytest.mark.Anki
def test_simple_add_cards():
    '''
    Funcao que testa a integracao entre o Anki-connect e o programa
    '''
    init_test = MainAddCardsMath.AddCardsMath(1, 2, db=mock_db())
    result_list = init_test.add_cards()
    assert result_list[0][0]['error'] == result_list[1][0]['error'] is None
    delete_cards_test_by_id([result_list[0][0]['result'],
                            result_list[1][0]['result']])
