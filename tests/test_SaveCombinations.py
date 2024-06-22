import sqlite3 as sql

from AddAnkiCards.Db import DbConnect
from AddAnkiCards.MathTraining.MakesCombinations import (
    FindCombinations,
    SaveCombinations,
)


def test_DistribuaSimple():
    """
    Testa casos simples para a funcao que ditribui as combinacoes.
    """
    print('\n', end='')
    # Criamos combinacoes em que a ordem nao importa que no total
    # Dao 45 combinacoes diferentes

    # E distribuimos as possibilidades para 9 cartoes
    listTest = SaveCombinations.Distribua(
        FindCombinations.FindCombSomMul([1, 9]), 9, 'n'
    )

    # verificamos se foram separadas as combinacoes para a
    # quantidade de cartoes
    assert len(listTest) == 9
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        # se foram separadas igualmente
        assert len(list) == 5  # 5 pois, 45/9 = 5
    # e se nao deixou nenhum cartao de fora
    assert countTerms == 45

    # A mesma coisa
    print('\n', end='')
    listTest = SaveCombinations.Distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 9, 'n'
    )
    assert len(listTest) == 9
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert len(list) == 9
    assert countTerms == 81


def test_DistribuaDivisoriaIsFloat():
    """
    Funcao que testa a distribuicao com o valor da divisoria sendo um float.
    Divisoria = len(lista)/numCardsPorDia
    """
    # para entender o teste consulte os comentarios do test_DistribuaSimple
    print('\n', end='')
    listTest = SaveCombinations.Distribua(
        FindCombinations.FindCombSomMul([1, 9]), 8, 'n'
    )
    assert len(listTest) == 8
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert 5 <= len(list) <= 6
    assert countTerms == 45

    print('\n', end='')
    listTest = SaveCombinations.Distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 8, 'n'
    )
    assert len(listTest) == 8
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert 10 <= len(list) <= 11
    assert countTerms == 81


def test_DistribuaWithMaxCards():
    print('\n', end='')
    listTest = SaveCombinations.Distribua(
        FindCombinations.FindCombSomMul([1, 9]), 8, 30
    )
    assert len(listTest) == 8
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert 3 <= len(list) <= 4
    assert countTerms == 30

    print('\n', end='')
    listTest = SaveCombinations.Distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 8, 30
    )
    assert len(listTest) == 8
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert 3 <= len(list) <= 4
    assert countTerms == 30


def test_ArmazeneSimple():
    """
    Funcao que testa a integracao do programa com o banco de dados
    """
    #
    # Fazemos as combinacoes para teste
    combinacaoTest1 = SaveCombinations.Distribua(
        FindCombinations.FindCombSomMul([1, 9]), 5, 'n'
    )
    combinacaoTest2 = SaveCombinations.Distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 9, 'n'
    )
    # Iniciamos a conexao com o banco de dados de teste
    conexaoDeTest = sql.connect('DbTest.db')
    cursorTest = conexaoDeTest.cursor()
    #
    # Rodamos a funcao que esta sendo testado
    SaveCombinations.Armazene(
        combinacaoTest1, 'som', False, [1, 9], DbConnect.DbConnect('DbTest.db')
    )
    SaveCombinations.Armazene(
        combinacaoTest2, 'som', False, [1, 9], DbConnect.DbConnect('DbTest.db')
    )
    #
    # Pesquisamos os valores que estao sendo testados no banco de dados de
    # teste e que nao dependem de outras funcoes
    resultTest1 = cursorTest.execute(
        'SELECT NumCards, TipoCard FROM CardsCalculoMental WHERE IdCard = 5'
    ).fetchall()
    resultTest2 = cursorTest.execute(
        'SELECT NumCards, TipoCard FROM CardsCalculoMental WHERE IdCard = 9'
    ).fetchall()

    # Fazemos as verificacoes
    assert resultTest1[0][0] == resultTest2[0][0] == 9
    assert resultTest1[0][1] == 1 and resultTest2[0][1] == 2

    # E limpamos o banco de dados de testes
    cursorTest.execute('DROP TABLE TipoCardsCalculoMental')
    cursorTest.execute('DROP TABLE CardsCalculoMental')
    cursorTest.close()
    conexaoDeTest.commit()
    conexaoDeTest.close()
