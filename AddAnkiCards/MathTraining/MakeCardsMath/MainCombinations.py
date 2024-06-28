"""Modulo proncipal da criacao dos cards de matematica."""
# importando a funcao que pede as informacoes para o usuario.
# importando a parte do programa que encontra as possibilidades
from FindCombinations import (
    Find2CombSomMul,
    Find2CombSubDiv,
    FindCombSomMul,
    FindCombSubDiv,
)
from InfoCombinations import informe, pergunte

# importando a parte do programa que formata, o que foi
# encontrado, para treinar no Anki
from SaveCombinations import armazene, calcula, distribua, embaralhe, formata


def main_combinador():
    """
    Funcao Principal do Algorito.
    - Pede as informacoes sobre as combinacoes;
    - Encontra todas possibilidades; e
    - Armazena elas em quantos arquivos a pessoa quiser
      de maneira alteatória ou nao
    """
    # pedindo as informacoes sobre a combinacao
    (
        quant_cards_por_d,
        sao_dois_intervalos,
        intervalo,
        num_max_cards,
        operacao,
    ) = pergunte()
    # verificamos se o usuário escolheu dois intervalos ou somente 1
    if sao_dois_intervalos:
        # caso tenha escolhido 2, verificamos se escolheu
        # subtracao ou divisao
        if operacao == 'sub' or operacao == 'div':
            # realizamos a funcao deste caso
            combinacoes = Find2CombSubDiv(intervalo[0], intervalo[1])
        # caso nao tenha escolhido sabemos que foi soma ou multiplicacao
        else:
            # portanto aplicamos a funcao correta para este caso
            combinacoes = Find2CombSomMul(intervalo[0], intervalo[1])
    # caso ele só tenha escolhido 1
    else:
        # verificamos se o usuário escolheu subtracao ou divisao
        if operacao == 'sub' or operacao == 'div':
            # criamos todas as combinacoes possíveis
            combinacoes = FindCombSubDiv(intervalo)
        # caso nao tenha escolhido, rodamos o programa
        # de adicao e multiplicacao
        else:
            # criamos todas as combinacoes possíveis
            combinacoes = FindCombSomMul(intervalo)
    # embaralhamos elas
    combinacoes_embaralhada = embaralhe(combinacoes)
    # distriuimos nas listas
    combinacoes_distribuidas = distribua(
        combinacoes_embaralhada, quant_cards_por_d, num_max_cards
    )
    # calculamos os valores das combinacoes:
    operatorAuxi = calcula(combinacoes_distribuidas, operacao)
    infoProduct = {}
    listCardFinal = []
    # verificamos se sao dois intervalos
    cont_id = 0
    if sao_dois_intervalos:
        intervalo[0] = '(%02i-%02i)' % (intervalo[0][0], intervalo[0][1])
        intervalo[1] = '(%02i-%02i)' % (intervalo[1][0], intervalo[1][1])
    for combinacoesSeparadas in combinacoes_distribuidas:
        cont_id += 1
        listCardFinal.append(
            formata(
                combinacoesSeparadas,
                operatorAuxi,
                operacao,
                intervalo,
                cont_id,
                infoProduct,
            )
        )
    # armazenando elas no arquivo
    armazene(
        listCardFinal, operacao, sao_dois_intervalos, intervalo, infoProduct
    )
    # informando a condicao final do produto
    informe(infoProduct)


main_combinador()
