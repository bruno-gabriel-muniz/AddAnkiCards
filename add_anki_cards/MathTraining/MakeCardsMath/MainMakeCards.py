"""Modulo proncipal da criacao dos cards de matematica."""
from sqlite3 import Connection, Cursor
from typing import Any

from add_anki_cards.logging_main import get_logger

# importando a funcao que pede as informacoes para o usuario.
# importando a parte do programa que encontra as possibilidades
from add_anki_cards.MathTraining.MakeCardsMath.FindCombinations import (
    find_2_comb_som_mul,
    find_2_comb_sub_div,
    find_comb_sub_div,
    find_comb_sum_mul,
)

# importando a parte do programa que formata, o que foi
# encontrado, para treinar no Anki
from add_anki_cards.MathTraining.MakeCardsMath.SaveCombinations import (
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
    db: Connection | Cursor,
    logger: Any = get_logger(),
):
    """Func. q faz, encontra e armazena as combinações."""
    # verificamos se o usuário escolheu dois intervalos ou somente 1
    logger.info(
        'Verificando se o usuário escolheu dois intervalos ou somente 1'
    )
    if sao_dois_intervalos:
        # caso tenha escolhido 2, verificamos se escolheu
        # subtracao ou divisao
        if operacao in ('sub', 'div'):
            # realizamos a funcao deste caso
            combinacoes = find_2_comb_sub_div(intervalo[0], intervalo[1])
        # caso nao tenha escolhido sabemos que foi soma ou multiplicacao
        else:
            # portanto aplicamos a funcao correta para este caso
            combinacoes = find_2_comb_som_mul(intervalo[0], intervalo[1])
    # caso ele só tenha escolhido 1
    else:
        # verificamos se o usuário escolheu subtracao ou divisao
        if operacao in ('sub', 'div'):
            # criamos todas as combinacoes possíveis
            combinacoes = find_comb_sub_div(intervalo)
        # caso nao tenha escolhido, rodamos o programa
        # de adicao e multiplicacao
        else:
            # criamos todas as combinacoes possíveis
            combinacoes = find_comb_sum_mul(intervalo)
    # embaralhamos elas
    logger.info('Embaralhando as combinações')
    combinacoes_embaralhada = embaralhe(combinacoes)
    # distriuimos nas listas
    logger.info('Distribuindo as combinações')
    combinacoes_distribuidas, count_cards = distribua(
        combinacoes_embaralhada, quant_of_notes, num_max_cards_per_note
    )
    # calculamos os valores das combinacoes:
    logger.info('Calculando os valores das combinações')
    operator_auxi = calcula(combinacoes_distribuidas, operacao)
    info_product = {}
    list_card_final = []
    # Fazendo a formatação dos intervalos caso sejam dois
    cont_id = 0
    logger.info('Fazendo a formatação dos intervalos caso sejam dois')
    if sao_dois_intervalos:
        intervalo[0] = f'({intervalo[0][0]:02.0f}-{intervalo[0][1]:02.0f})'
        intervalo[1] = f'({intervalo[1][0]:02.0f}-{intervalo[1][1]:02.0f})'
    # Formatação das combinações
    logger.info('Formatação das combinações')
    for combinacoes_separadas in combinacoes_distribuidas:
        cont_id += 1
        list_card_final.append(
            formata(
                combinacoes_separadas,
                operator_auxi,
                operacao,
                intervalo,
                cont_id,
                info_product,
            )
        )
    # Armazenando as combinações no banco de dados
    logger.info('Armazenando as combinações no banco de dados')
    armazene(
        list_card_final=list_card_final,
        tipo_operacao=operacao,
        sao_dois_intervalos=sao_dois_intervalos,
        intervalo=intervalo,
        count_cards=count_cards,
        info_product=info_product,
        db=db,
    )


if __name__ == '__main__':
    main_make_cards()
