import random

from add_anki_cards.Db import DbConnect
from add_anki_cards.models.Math.MakeCardsMath import (
    FindCombinations,
    SaveCombinations,
)


def test_distribua_simple():
    """
    Testa casos simples para a funcao que ditribui as combinacoes.
    """
    print('\n', end='')
    # Criamos combinacoes em que a ordem nao importa que no total
    # Dao 45 combinacoes diferentes

    # E distribuimos as possibilidades para 9 cartoes
    list_test, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sum_mul([1, 9]), 9, 'n'
    )

    # verificamos se foram separadas as combinacoes para a
    # quantidade de cartoes
    assert len(list_test) == 9
    count_terms = 0
    for list in list_test:
        print(list)
        count_terms += len(list)
        # se foram separadas igualmente
        assert len(list) == 5  # 5 pois, 45/9 = 5
    # e se nao deixou nenhum cartao de fora
    assert count_terms == 45

    # A mesma coisa
    print('\n', end='')
    list_test, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sub_div([1, 9]), 9, 'n'
    )
    assert len(list_test) == 9
    count_terms = 0
    for list in list_test:
        print(list)
        count_terms += len(list)
        assert len(list) == 9
    assert count_terms == 81


def test_distribua_divisoria_is_float():
    """
    Funcao que testa a distribuicao com o valor da divisoria sendo um float.
    Divisoria = len(lista)/numCardsPorDia
    """
    # para entender o teste consulte os comentarios do test_DistribuaSimple
    print('\n', end='')
    list_test, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sum_mul([1, 9]), 8, 'n'
    )
    assert len(list_test) == 8
    count_terms = 0
    for list in list_test:
        print(list)
        count_terms += len(list)
        assert 5 <= len(list) <= 6
    assert count_terms == 45

    print('\n', end='')
    list_test, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sub_div([1, 9]), 8, 'n'
    )
    assert len(list_test) == 8
    count_terms = 0
    for list in list_test:
        print(list)
        count_terms += len(list)
        assert 10 <= len(list) <= 11
    assert count_terms == 81


def test_distribua_with_max_cards():
    print('\n', end='')
    list_test, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sum_mul([1, 9]), 8, 30
    )
    assert len(list_test) == 8
    count_terms = 0
    for list in list_test:
        print(list)
        count_terms += len(list)
        assert 3 <= len(list) <= 4
    assert count_terms == 30

    print('\n', end='')
    list_test, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sub_div([1, 9]), 8, 30
    )
    assert len(list_test) == 8
    count_terms = 0
    for list in list_test:
        print(list)
        count_terms += len(list)
        assert 3 <= len(list) <= 4
    assert count_terms == 30


def test_calcula_1_intervalo():
    """
    Testa a funcao calcula do armazene cards com combinacoes de um intervalo.
    """
    # preparamos o ambiente
    #
    # chamamos a funcao que encontra todas combinacoes
    result_sum_test_1 = FindCombinations.find_comb_sum_mul([1, 9])
    #
    # a que distribui, mesmo sem chamar a que embaralha as combinacoes
    # pois isso nao influencia o teste
    result_sum_test_1, num_cards = SaveCombinations.distribua(
        result_sum_test_1, 9, 'n'
    )
    #
    # a mesma coisa para o teste de multiplicacao, devido a um bug no metodo
    # copy (ele esta passando o endereco de memoria da lista ao inves de
    # criar uma nova com os mesmos valores)
    result_mul_test_1 = FindCombinations.find_comb_sum_mul([1, 9])
    result_mul_test_1, num_cards = SaveCombinations.distribua(
        result_mul_test_1, 9, 'n'
    )
    #
    # e enfim chamamos a funcao que esta sendo testada
    SaveCombinations.calcula(result_sum_test_1, 'sum')
    SaveCombinations.calcula(result_mul_test_1, 'mul')
    #
    # as testamos com valores aleatorios delas.
    for test in range(5):
        comb_sum_test = random.choice(random.choice(result_sum_test_1))
        comb_mul_test = random.choice(random.choice(result_mul_test_1))
        #
        # Explicacao: cada combinacao fica em uma sub lista com os dois
        # valores da combinacao e o resultado da operacao no ultimo indice (2)
        assert comb_sum_test[0] + comb_sum_test[1] == comb_sum_test[2]
        assert comb_mul_test[0] * comb_mul_test[1] == comb_mul_test[2]
    #
    # Agora fazemos a mesma coisa para a subtracao e divisao.
    result_sub_test_2 = FindCombinations.find_comb_sub_div([1, 9])
    result_sub_test_2, num_cards = SaveCombinations.distribua(
        result_sub_test_2, 9, 'n'
    )
    result_div_test_2 = FindCombinations.find_comb_sub_div([1, 9])
    result_div_test_2, num_cards = SaveCombinations.distribua(
        result_div_test_2, 9, 'n'
    )
    SaveCombinations.calcula(result_sub_test_2, 'sub')
    SaveCombinations.calcula(result_div_test_2, 'div')
    for test in range(5):
        comb_sub_test = random.choice(random.choice(result_sub_test_2))
        comb_div_test = random.choice(random.choice(result_div_test_2))
        assert comb_sub_test[0] - comb_sub_test[1] == comb_sub_test[2]
        assert (
            (comb_div_test[0] * 100) // comb_div_test[1]
        ) / 100 == comb_div_test[2]
    ...


def test_armazene_simple():
    """
    Funcao que testa a integracao do programa com o banco de dados
    """
    print()
    #
    # Fazemos as combinacoes para teste
    combinacoes_test_1, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sum_mul([1, 9]), 5, 'n'
    )
    combinacoes_test_2, num_cards = SaveCombinations.distribua(
        FindCombinations.find_comb_sub_div([1, 9]), 9, 'n'
    )
    # Iniciamos a conexao com o banco de dados de teste
    conexao_de_test = DbConnect.db_connect('DbTest.db', 'Test')
    cursor_test = conexao_de_test.cursor()
    #
    # preparamos o ambiente para este teste
    operator_auxi_1 = SaveCombinations.calcula(combinacoes_test_1, 'sum')
    operator_auxi_2 = SaveCombinations.calcula(combinacoes_test_2, 'sum')
    list_card_final_test_1 = []
    list_card_final_test_2 = []
    info_product_1 = {}
    info_product_2 = {}
    cont_id = 0
    for card_test in combinacoes_test_1:
        cont_id += 1
        list_card_final_test_1.append(
            SaveCombinations.formata(
                card_test,
                operator_auxi_1,
                'sum',
                [1, 9],
                cont_id,
                info_product_1,
            )
        )
    cont_id = 0
    for card_test in combinacoes_test_2:
        cont_id += 1
        list_card_final_test_2.append(
            SaveCombinations.formata(
                card_test,
                operator_auxi_2,
                'sum',
                [1, 9],
                cont_id,
                info_product_2,
            )
        )
    #
    # Rodamos a funcao que esta sendo testado
    SaveCombinations.armazene(
        list_card_final_test_1,
        'sum',
        False,
        [1, 9],
        num_cards,
        info_product_1,
        DbConnect.db_connect('DbTest.db', 'Test'),
    )
    SaveCombinations.armazene(
        list_card_final_test_2,
        'sum',
        False,
        [1, 9],
        num_cards,
        info_product_2,
        DbConnect.db_connect('DbTest.db', 'Test'),
    )
    #
    # Pesquisamos os valores que estao sendo testados no banco de dados de
    # teste e que nao dependem de outras funcoes
    result_test_1 = cursor_test.execute(
        'SELECT NumCards, TipoCard FROM CardsCalculoMental WHERE IdCard = 5'
    ).fetchall()
    result_test_2 = cursor_test.execute(
        'SELECT NumCards, TipoCard FROM CardsCalculoMental WHERE IdCard = 9'
    ).fetchall()

    # Fazemos as verificacoes
    print(result_test_1, result_test_2)
    assert result_test_1[0][0] == result_test_2[0][0] == 9
    assert result_test_1[0][1] == 1 and result_test_2[0][1] == 2

    # E limpamos o banco de dados de testes
    cursor_test.execute('DROP TABLE TipoCardsCalculoMental')
    cursor_test.execute('DROP TABLE CardsCalculoMental')
    cursor_test.close()
    conexao_de_test.commit()
    conexao_de_test.close()
