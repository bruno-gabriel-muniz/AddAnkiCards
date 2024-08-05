"""Modulo proncipal da criacao dos cards de matematica."""
import sqlite3

from AddAnkiCards.Db import DbConnect

# importando a funcao que pede as informacoes para o usuario.
# importando a parte do programa que encontra as possibilidades
from AddAnkiCards.MathTraining.MakeCardsMath.FindCombinations import (
    Find2CombSomMul,
    Find2CombSubDiv,
    FindCombSomMul,
    FindCombSubDiv,
)

# importando a parte do programa que formata, o que foi
# encontrado, para treinar no Anki
from AddAnkiCards.MathTraining.MakeCardsMath.SaveCombinations import (
    armazene,
    calcula,
    distribua,
    embaralhe,
    formata,
)


def main_make_cards(
    quant_of_notes: int,
    sao_dois_intervalos: bool,
    intervalo: list,
    num_max_cards_per_note: int,
    operacao: str,
    Db: sqlite3.Connection = DbConnect.DbConnect(),
):
    """
    Funcao que faz as combinacoes.
    - Encontra todas possibilidades; e
    - Armazena elas no banco de dados
    """
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
    combinacoes_distribuidas, countCards = distribua(
        combinacoes_embaralhada, quant_of_notes, num_max_cards_per_note
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
        listCardFinal,
        operacao,
        sao_dois_intervalos,
        intervalo,
        countCards,
        infoProduct,
    )


if __name__ == '__main__':
    main_make_cards()
