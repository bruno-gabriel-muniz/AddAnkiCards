from math import factorial

import pytest

from add_anki_cards.logging_main import get_logger
from add_anki_cards.models.Math.MakeCardsMath import FindCombinations

logger = get_logger('Test')

# Testes sobre encontrar todas as possibilidades ###


def sum_all_comb_sum_mul1(min_term: int, max_term: int) -> int:
    """
    Funcao que calcula a quantidades de combinacoes possiveis na soma
    e multiplicacao de termos do mesmo intervalo.

    Levando em consideracao que o total de possibilidades eh o valor, da
    combinacao (em que a ordem nao importa), da analise combinatoria, dos pares
    dos numeros do intervalo mais a diferenca entre o valor mais baixo e alto
    do intervalo. Ja que, cada valor do intervalo pode ser operado uma vez com
    ele e uma vez com cada um dos outros.

    ps.: Formula value = n!/(2!(n - 2)!)
         Formula Final:
            n = (MaiorValorIntervalo - MenorValorIntervalo + 1)
            Diferença Entre O Menor E Maior Num Do Intervalo = n
            =: **  (n!/(2!(n-2)!)) + n  **
    """
    n = max_term - min_term + 1
    return int((factorial(n) / (factorial(2) * factorial(n - 2))) + n)


def sum_all_comb_sub_div1(min_term: int, max_term: int) -> int:
    """
    Funcao que calcula a quantidades de arranjos possiveis na subtracao
    e divisao de termos do mesmo intervalo.

    Levando em consideracao que o total de possibilidades eh o valor, do
    arranjo (em que a ordem importa), da analise combinatoria, dos pares dos
    numeros do intervalo mais a diferenca entre o valor mais baixo e alto do
    intervalo mais 1. Ja que, cada valor do intervalo pode ser operado uma
    vez com ele e duas vezes com cada um dos outros. Ex.: 3-3 e 3-1 != 1-3.
    Logo o total eh tres operacao diferentes entre o 3 com 3 e 3 com 1.

    ps.: Formula value = n!/((n - 2)!)
         Formula Final:
            n = (MaiorValorIntervalo - MenorValorIntervalo + 1)
            Diferença Entre O Menor E Maior Num Do Intervalo = n
            =: (n!/((n-2)!)) + n, reduzindo =: ** n**2 **
    """
    n = max_term - min_term + 1
    return n**2


def sum_all_comb_sum_mul2(menor_inter: tuple, maior_inter: tuple) -> int:
    """
    Func. que calcula o maximo de combinacoes entre valores de dois intervalos.
    Levando em concideracao que isso eh a combinacao dos valores dos dois
    grupos na qual a ordem nao importa. Sendo assim, para cada termo de um
    intervalo, todas as combinacoes possiveis em que ele aparece sera
    exatemente o tamanho do outro intervalo. Logo:
    =: TamanhoInter1 * TamanhoInter2
    """
    tamanho_inter_menor = menor_inter[1] - menor_inter[0] + 1
    tamanho_inter_maior = maior_inter[1] - maior_inter[0] + 1
    return tamanho_inter_maior * tamanho_inter_menor


def sum_all_comb_sub_div2(menor_inter: tuple, maior_inter: tuple) -> int:
    """
    Func. que calcula o maximo de combinacoes entre valores de dois intervalos.
    Levando em concideracao que isso eh a combinacao dos valores dos dois
    grupos na qual a ordem importa. Sendo assim, para cada termo de um
    intervalo, todas as combinacoes possiveis em que ele aparece sera
    exatemente o tamanho do outro intervalo vezes dois. Pois, para cada
    combinacao existem duas ordenacoes diferentes ([1, 2] e [2, 1]) Logo:
    =: TamanhoInter1 * TamanhoInter2 * 2.
    """
    tamanho_inter_menor = menor_inter[1] - menor_inter[0] + 1
    tamanho_inter_maior = maior_inter[1] - maior_inter[0] + 1
    return tamanho_inter_maior * tamanho_inter_menor * 2


def test_find_comb_sum_mul__all_combinations(benchmark):
    """
    Funcao que testa se todas as possibilidades foram encontradas.
    Levando em consideracao os calculas da funcao 'sumAllCombinationsSomMul1'.
    """
    print('\nCombinacao 1-9: ', end='')

    assert len(
        FindCombinations.find_comb_sum_mul([1, 9])
    ) == sum_all_comb_sum_mul1(1, 9)
    print('Combinacao 10-99: ', end='')
    assert len(
        FindCombinations.find_comb_sum_mul([10, 99])
    ) == sum_all_comb_sum_mul1(10, 99)
    print('Combinacao 100-999: ', end='')
    testb = benchmark(FindCombinations.find_comb_sum_mul, [100, 999])
    assert len(testb) == sum_all_comb_sum_mul1(100, 999)


def test_find_comb_sub_div__all_combinations(benchmark):
    """
    Funcao que testa se todas as possibilidades foram encontradas.
    Levando em consideracao os calculas da funcao 'sumAllCombinationsSubDiv1'.
    """
    print('\nCombinacao 1-9: ', end='')
    assert len(
        FindCombinations.find_comb_sub_div([1, 9])
    ) == sum_all_comb_sub_div1(1, 9)
    print('Combinacao 10-99: ', end='')
    assert len(
        FindCombinations.find_comb_sub_div([10, 99])
    ) == sum_all_comb_sub_div1(10, 99)
    print('Combinacao 100-999: ', end='')
    testb = benchmark(FindCombinations.find_comb_sub_div, [100, 999])
    assert len(testb) == sum_all_comb_sub_div1(100, 999)


def test_find_comb_sum_mul__all_combinations2(benchmark):
    """
    Funcao que testa se todas as possibilidades foram encontradas.
    Levando em consideracao os calculas da funcao 'sumAllCombinationsSomMul2'.
    """
    print('\nCombinacao (1-9)-(10-99): ', end='')
    assert len(
        FindCombinations.find_2_comb_som_mul([1, 9], [10, 99])
    ) == sum_all_comb_sum_mul2([1, 9], [10, 99])

    print('Combinacao (1-9)-(100-999): ', end='')
    assert len(
        FindCombinations.find_2_comb_som_mul([1, 9], [100, 999])
    ) == sum_all_comb_sum_mul2([1, 9], [100, 999])

    print('Combinacao (10-99)-(100-999): ', end='')
    testb = benchmark(
        FindCombinations.find_2_comb_som_mul, [10, 99], [100, 999]
    )
    assert len(testb) == sum_all_comb_sum_mul2([10, 99], [100, 999])


def test_find_comb_sub_div__all_combinations2(benchmark):
    """
    Funcao que testa se todas as possibilidades foram encontradas.
    Levando em consideracao os calculas da funcao 'sumAllCombinationsSubDiv2'.
    """
    print('\nCombinacao (1-9)-(10-99): ', end='')
    assert len(
        FindCombinations.find_2_comb_sub_div([1, 9], [10, 99])
    ) == sum_all_comb_sub_div2([1, 9], [10, 99])

    print('Combinacao (1-9)-(100-990): ', end='')
    assert len(
        FindCombinations.find_2_comb_sub_div([1, 9], [100, 999])
    ) == sum_all_comb_sub_div2([1, 9], [100, 999])

    print('Combinacao (10-99)-(100-990): ', end='')
    testb = benchmark(
        FindCombinations.find_2_comb_sub_div, [10, 99], [100, 999]
    )
    assert len(testb) == sum_all_comb_sub_div2([10, 99], [100, 999])


#
# Testes sobre repeticoes ###
#


def not_repeat_data(data: list) -> bool:
    dnr = {}
    for comb in data:
        scomb = str(comb)
        if scomb not in dnr:
            dnr[scomb] = True
        else:
            return False, f'O ele. {comb} estah repetido'
    return True, 'Deu Bom'


def test_not_repeat_data():
    assert not_repeat_data([1, 2, 3]) == (True, 'Deu Bom')
    assert not_repeat_data([9, 2, 800, 50]) == (True, 'Deu Bom')
    assert not_repeat_data([2, 7, 11, 2]) == (False, 'O ele. 2 estah repetido')


def test_find_comb_sum_mul_not_repeat(caplog):
    """
    Funcao que testa se nao ha repeticao nas combinacoes encontradas
    """
    print('\nCombinacao 1-9: ', end='')
    combinations = FindCombinations.find_comb_sum_mul([1, 9])
    result = not_repeat_data(combinations)
    assert result[0], result[1]

    print('Combinacao 10-99: ', end='')
    combinations = FindCombinations.find_comb_sum_mul([10, 99])
    result = not_repeat_data(combinations)
    assert result[0], result[1]


def test_find_comb_sub_div_not_repeat(caplog):
    """
    Funcao que testa se nao ha repeticao nas combinacoes encontradas
    """
    print('\nCombinacao 1-9: ', end='')
    combinations = FindCombinations.find_comb_sub_div([1, 9])
    result = not_repeat_data(combinations)
    assert result[0], result[1]

    print('Combinacao 10-99: ', end='')
    combinations = FindCombinations.find_comb_sub_div([10, 99])
    result = not_repeat_data(combinations)
    assert result[0], result[1]


@pytest.mark.NotQuick
def test_find_comb_sum_mul_not_repeat2(caplog):
    """
    Funcao que testa se nao ha repeticao nas combinacoes encontradas
    """
    print('\nCombinacao (1-9)-(10-99): ', end='')
    combinations = FindCombinations.find_2_comb_som_mul([1, 9], [10, 99])
    result = not_repeat_data(combinations)
    assert result[0], result[1]

    print('Combinacao (1-9)-(100-999): ', end='')
    combinations = FindCombinations.find_2_comb_som_mul([1, 9], [100, 999])
    result = not_repeat_data(combinations)
    assert result[0], result[1]


@pytest.mark.NotQuick
def test_find_comb_sub_div_not_repeat2(caplog):
    """
    Funcao que testa se nao ha repeticao nas combinacoes encontradas
    """
    print('\nCombinacao (1-9)-(10-99): ', end='')
    combinations = FindCombinations.find_2_comb_sub_div([1, 9], [10, 99])
    result = not_repeat_data(combinations)
    assert result[0], result[1]

    print('Combinacao (1-9)-(100-999): ', end='')
    combinations = FindCombinations.find_2_comb_sub_div([1, 9], [100, 999])
    result = not_repeat_data(combinations)
    assert result[0], result[1]


#
# Testes sobre entradas erradas ###
#


def test_find_combinations_range_empty():
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_comb_sum_mul([1, 1])
    assert test_error.value.args[0] == (
        'O intervalo tem que ter o menor '
        + 'valor primeiro e o maior depois '
        + '[menor, maior]'
    )
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_comb_sub_div([9, 1])
    assert test_error.value.args[0] == (
        'O intervalo tem que ter o menor '
        + 'valor primeiro e o maior depois '
        + '[menor, maior]'
    )


def test_find_combinations_range_invalid():
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_comb_sum_mul([1, 3, 10])
    print('\n', test_error)
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_comb_sub_div([10, 50, 99])
    print(test_error)


def test_find_2_combinations_range_empty():
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_2_comb_som_mul([1, 1], [10, 99])
    assert test_error.value.args[0] == (
        'Os intervalos tem que ter o menor '
        + 'valor primeiro e o maior depois '
        + '[menor, maior]'
    )
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_2_comb_sub_div([1, 9], [10, 1])
    assert test_error.value.args[0] == (
        'Os intervalos tem que ter o menor '
        + 'valor primeiro e o maior depois '
        + '[menor, maior]'
    )


def test_find_2_combinations_range_intersect():
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_2_comb_som_mul([1, 10], [5, 20])
    assert test_error.value.args[0] == (
        'Os intervalos, (' + f'{[1, 10]}-{[5, 20]}' + '), se interssectam.'
    )
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_2_comb_sub_div([10, 99], [50, 200])
    assert test_error.value.args[0] == (
        'Os intervalos, (' + f'{[10, 99]}-{[50, 200]}' + '), se interssectam.'
    )


def test_find_2_combinations_range_invalid():
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_2_comb_som_mul([1, 3, 10], [10, 99])
    print('\n', test_error)
    with pytest.raises(ValueError) as test_error:
        FindCombinations.find_2_comb_sub_div([10, 50, 99], [50, 200])
    print(test_error)
