import random
import sqlite3 as sql

from AddAnkiCards.Db import DbConnect
from AddAnkiCards.MathTraining.MakeCardsMath import (FindCombinations,
                                                     SaveCombinations)


def test_distribuaSimple():
    """
    Testa casos simples para a funcao que ditribui as combinacoes.
    """
    print('\n', end='')
    # Criamos combinacoes em que a ordem nao importa que no total
    # Dao 45 combinacoes diferentes

    # E distribuimos as possibilidades para 9 cartoes
    listTest, numCards = SaveCombinations.distribua(
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
    listTest, numCards = SaveCombinations.distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 9, 'n'
    )
    assert len(listTest) == 9
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert len(list) == 9
    assert countTerms == 81


def test_distribuaDivisoriaIsFloat():
    """
    Funcao que testa a distribuicao com o valor da divisoria sendo um float.
    Divisoria = len(lista)/numCardsPorDia
    """
    # para entender o teste consulte os comentarios do test_DistribuaSimple
    print('\n', end='')
    listTest, numCards = SaveCombinations.distribua(
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
    listTest, numCards = SaveCombinations.distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 8, 'n'
    )
    assert len(listTest) == 8
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert 10 <= len(list) <= 11
    assert countTerms == 81


def test_distribuaWithMaxCards():
    print('\n', end='')
    listTest, numCards = SaveCombinations.distribua(
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
    listTest, numCards = SaveCombinations.distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 8, 30
    )
    assert len(listTest) == 8
    countTerms = 0
    for list in listTest:
        print(list)
        countTerms += len(list)
        assert 3 <= len(list) <= 4
    assert countTerms == 30


def test_calcula1Intervalo():
    '''
    Testa a funcao calcula do armazene cards com combinacoes de um intervalo
    '''
    # preparamos o ambiente
    #
    # chamamos a funcao que encontra todas combinacoes
    resultSomTest1 = FindCombinations.FindCombSomMul([1, 9])
    #
    # a que distribui, mesmo sem chamar a que embaralha as combinacoes
    # pois isso nao influencia o teste
    resultSomTest1, numCards = SaveCombinations.distribua(
        resultSomTest1, 9, 'n')
    #
    # a mesma coisa para o teste de multiplicacao, devido a um bug no metodo
    # copy (ele esta passando o endereco de memoria da lista ao inves de
    # criar uma nova com os mesmos valores)
    resultMulTest1 = FindCombinations.FindCombSomMul([1, 9])
    resultMulTest1, numCards = SaveCombinations.distribua(
        resultMulTest1, 9, 'n')
    #
    # e enfim chamamos a funcao que esta sendo testada
    SaveCombinations.calcula(resultSomTest1, 'som')
    SaveCombinations.calcula(resultMulTest1, 'mul')
    #
    # as testamos com valores aleatorios delas.
    for test in range(5):
        combSomTest = random.choice(random.choice(resultSomTest1))
        combMulTest = random.choice(random.choice(resultMulTest1))
        #
        # Explicacao: cada combinacao fica em uma sub lista com os dois
        # valores da combinacao e o resultado da operacao no ultimo indice (2)
        assert combSomTest[0] + combSomTest[1] == combSomTest[2]
        assert combMulTest[0] * combMulTest[1] == combMulTest[2]
    #
    # Agora fazemos a mesma coisa para a subtracao e divisao.
    resultSubTest2 = FindCombinations.FindCombSubDiv([1, 9])
    resultSubTest2, numCards = SaveCombinations.distribua(
        resultSubTest2, 9, 'n')
    resultDivTest2 = FindCombinations.FindCombSubDiv([1, 9])
    resultDivTest2, numCards = SaveCombinations.distribua(
        resultDivTest2, 9, 'n')
    SaveCombinations.calcula(resultSubTest2, 'sub')
    SaveCombinations.calcula(resultDivTest2, 'div')
    for test in range(5):
        combSubTest = random.choice(random.choice(resultSubTest2))
        combDivTest = random.choice(random.choice(resultDivTest2))
        assert combSubTest[0] - combSubTest[1] == combSubTest[2]
        assert ((combDivTest[0]*100) // combDivTest[1])/100 == combDivTest[2]
    ...


def test_armazeneSimple():
    """
    Funcao que testa a integracao do programa com o banco de dados
    """
    print()
    #
    # Fazemos as combinacoes para teste
    combinacoesTest1, numCards = SaveCombinations.distribua(
        FindCombinations.FindCombSomMul([1, 9]), 5, 'n'
    )
    combinacoesTest2, numCards = SaveCombinations.distribua(
        FindCombinations.FindCombSubDiv([1, 9]), 9, 'n'
    )
    # Iniciamos a conexao com o banco de dados de teste
    conexaoDeTest = sql.connect('DbTest.db')
    cursorTest = conexaoDeTest.cursor()
    #
    # preparamos o ambiente para este teste
    operatorAuxi1 = SaveCombinations.calcula(combinacoesTest1, 'som')
    operatorAuxi2 = SaveCombinations.calcula(combinacoesTest2, 'som')
    listCardFinalTest1 = []
    listCardFinalTest2 = []
    infoProduct1 = {}
    infoProduct2 = {}
    cont_id = 0
    for cardTest in combinacoesTest1:
        cont_id += 1
        listCardFinalTest1.append(SaveCombinations.formata(
            cardTest, operatorAuxi1, 'som', [1, 9], cont_id, infoProduct1))
    cont_id = 0
    for cardTest in combinacoesTest2:
        cont_id += 1
        listCardFinalTest2.append(SaveCombinations.formata(
            cardTest, operatorAuxi2, 'som', [1, 9], cont_id, infoProduct2))
    #
    # Rodamos a funcao que esta sendo testado
    SaveCombinations.armazene(
        listCardFinalTest1, 'som', False, [1, 9], numCards, infoProduct1,
        DbConnect.DbConnect('DbTest.db'))
    SaveCombinations.armazene(
        listCardFinalTest2, 'som', False, [1, 9], numCards, infoProduct2,
        DbConnect.DbConnect('DbTest.db'))
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
