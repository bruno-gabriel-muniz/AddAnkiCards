"""Modulo proncipal da criacao dos cards de matematica."""
# importando a funcao que pede as informacoes para o usuario.
# importando a parte do programa que encontra as possibilidades
from FindCombinations import (Find2CombSubDiv, Find2CombSumMul, FindCombSubDiv,
                              FindCombSumMul)
from InfoCombinations import Pergunte, informe
# importando a parte do programa que formata, o que foi
# encontrado, para treinar no Anki
from SaveCombinations import Armazene, Distribua, Embaralhe


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
    ) = Pergunte()
    # verificando se o usuário escolheu dois intervalos ou somente 1
    if sao_dois_intervalos:
        # caso tenha escolhido 2 verificando se escolheu
        # subtracao ou divisao
        if operacao == 'sub' or operacao == 'div':
            # realizando a funcao deste caso
            combinacoes = Find2CombSubDiv(intervalo[0], intervalo[1])
        # caso nao tenha escolhido sabemos que foi soma ou multiplicacao
        else:
            # portanto aplicamos a funcao correta para este caso
            combinacoes = Find2CombSumMul(intervalo[0], intervalo[1])
    # caso ele só tenha escolhido 1
    else:
        # verificando se o usuário escolheu subtracao ou divisao
        if operacao == 'sub' or operacao == 'div':
            # criando todas as combinacoes possíveis
            combinacoes = FindCombSubDiv(intervalo)
        # caso nao tenha escolhidoi rodando o programa
        # de adicao e multiplicacao
        else:
            # criando todas as combinacoes possíveis
            combinacoes = FindCombSumMul(intervalo)
    # embaralhando elas
    combinacoes_embaralhada = Embaralhe(combinacoes)
    # distriubuindo nas listas
    combinacoes_distribuidas = Distribua(
        combinacoes_embaralhada, quant_cards_por_d, num_max_cards
    )
    # armazenando elas no arquivo
    informacoes_do_resultado = Armazene(
        combinacoes_distribuidas, operacao, sao_dois_intervalos, intervalo
    )
    # informando a condicao final do produto
    informe(informacoes_do_resultado)


main_combinador()
