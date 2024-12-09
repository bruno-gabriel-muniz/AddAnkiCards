import sqlite3 as sql
from random import shuffle

from add_anki_cards.Db import DbConnect


def embaralhe(combinacoes: list) -> list:
    """Func. q embaralha todas as comb. encontradas."""
    # embaralhando
    shuffle(combinacoes)
    # retornando
    return combinacoes


def distribua(
    combinacoes: list, quant_cards_por_d: int, num_max_cards: int
) -> tuple[list, int]:
    """Func. q distribui as comb. encontradas em listas."""
    # variavel que divide os valores da lista igualmente entre a
    # quantidade de cartoes por dia
    divisoria = len(combinacoes) / quant_cards_por_d
    # criando a lista que vai conter as listas separadas
    lista_separada = []
    count_cards = 0
    # verificando se possui um limite máximo para os cartoes
    if num_max_cards == 'n':
        # for loop que cria todas as listas
        for proximo in range(quant_cards_por_d):
            # adicionando a lista separada os cartoes da lista
            lista_separada.append(
                combinacoes[
                    round(proximo * divisoria) : round(
                        (proximo + 1) * divisoria
                    )
                ]
            )
            count_cards += len(lista_separada[-1])
    # verificando se o limite de cartoes ultrapaca a divisoria
    elif (num_max_cards / quant_cards_por_d) >= divisoria:
        # for loop que cria as listas
        for proximo in range(quant_cards_por_d):
            # adicionando a lista separada os cartoes da lista
            lista_separada.append(
                combinacoes[
                    round(proximo * divisoria) : round(
                        (proximo + 1) * divisoria
                    )
                ]
            )
            count_cards += len(lista_separada[-1])
    # caso tenha e nao ultrapase a divisoria
    else:
        count_cards = 0
        # for loop que cria as listas
        for proximo in range(quant_cards_por_d):
            # adicionando a lista separada os cartoes da lista
            # levando em consideracao o limite
            lista_separada.append(
                combinacoes[
                    round(proximo * divisoria) : round(
                        proximo * divisoria
                        + (num_max_cards / quant_cards_por_d)
                    )
                ]
            )
            count_cards += len(lista_separada[-1])
        if count_cards > num_max_cards:
            lista_separada[-1].pop()
    # retornando a lista e a quantidade de cartoes
    return lista_separada, count_cards


def calcula(combinacoes: list, operacao: str) -> str:
    """
    Func. q calcula os resultados das comb. sendo operadas por +, -, *, /.

    Como usar:
    ─ Argumentos: uma lista com todas as combinações encontradas e a
      operação a ser realizada; e
    ─ Retorno: o operador da operação realizada.
    """
    if operacao == 'sum':
        operator_auxi = '+'
        #
        # passamos por todos os cards
        for combinacoes_separadas in combinacoes:
            #
            # passamos por todos as combinacoes
            #
            for combinacao in combinacoes_separadas:
                # calculamos o valor de cada combinacao e
                # adcionamos os valores delas no ultimo indice da lista
                resultado = combinacao[0] + combinacao[1]
                combinacao.append(resultado)
    elif operacao == 'sub':
        operator_auxi = '-'
        for combinacoes_separadas in combinacoes:
            for combinacao in combinacoes_separadas:
                resultado = combinacao[0] - combinacao[1]
                combinacao.append(resultado)
    elif operacao == 'mul':
        operator_auxi = '*'
        for combinacoes_separadas in combinacoes:
            for combinacao in combinacoes_separadas:
                resultado = combinacao[0] * combinacao[1]
                combinacao.append(resultado)
    elif operacao == 'div':
        operator_auxi = '/'
        for combinacoes_separadas in combinacoes:
            for combinacao in combinacoes_separadas:
                resultado = (combinacao[0] * 100 // combinacao[1]) / 100
                combinacao.append(resultado)
    else:
        raise ValueError(
            'A operacao so pode ser "sum", "sub", "mul" ou '
            + '"div" com estes mesmos caracteres'
        )
    return operator_auxi


def formata(
    combinacoes: list,
    operator_auxi: str,
    operator: str,
    intervalo: list,
    cont_id: int,
    info_produto: dict,
) -> str:
    """
    Func. q formata as comb. encontradas para os cartoes.

    Como usar:
    ─ Argumentos: uma lista com todas as combinações encontradas, o operador
      a ser usado, o intervalo, o id do cartão e um dicionário com as
      informações do produto; e
    ─ Retorno: a string com o cartão formatado.
    """
    pulei_linha = True

    # criando a variavel que vai contar os numeros dos clozes
    cont_cloze = 0

    # Formatando o titulo do cartao e iniciando
    # a criacao da string do cartao
    card_title = (
        f'Treinamento_de_{operator}_entre_'
        + f'{intervalo[0]}-{intervalo[1]}_id_{cont_id}'
    )
    info_produto[cont_id] = {'Nome': card_title}
    card_final = f'<h2>{card_title}</h2>\n<p>'
    # passando por todos elementos cauculados da lista para aplicar a
    # formatacao que vai nos cartoes as combinacoes nos arquivos
    for combinado in combinacoes:
        # verificando se eu pulei uma linha no ciclo passado
        # caso nao tenha entrando na tomada de desicao
        # de pular uma linha
        if not pulei_linha:
            # adicionando a variavel do cloze
            cont_cloze += 1

            # escrevendo o valor do cálculo no arquivo já com a formatacao
            card_final += (
                f'{combinado[0]:_>2} {operator_auxi} '
                + f'{combinado[1]:_>2} = '
                + f'{{{{c{cont_cloze}::{combinado[2]:_^4}}}}}'
                + '<br>\n\n'
            )
            # informando o programa que ele pulou uma linha
            pulei_linha = True
        # caso o programa tenha pulado uma linha da ultima vez
        else:
            # adicionando a variavel do cloze
            cont_cloze += 1
            # escrevendo o valor do cálculo no arquivo já com a formatacao
            card_final += (
                f'{combinado[0]:_>2} {operator_auxi} '
                + f'{combinado[1]:_>2} = '
                + f'{{{{c{cont_cloze}::{combinado[2]:_^4}}}}}'
                + '|----------|'
            )
            # informando o programa que ele nao puluo uma linha
            pulei_linha = False
    # adicionando a quantidade de cartoes no dicionário
    # de informacoes do produto
    info_produto[cont_id]['Número de Perguntas'] = cont_cloze
    return card_final


def armazene(
    list_card_final: list,
    tipo_operacao: str,
    sao_dois_intervalos: bool,
    intervalo: list,
    count_cards: int,
    info_product: dict,
    db: sql.Connection | sql.Cursor = DbConnect.db_connect('GeneralDB.db'),
) -> dict:
    """Func. q armazena os valores dos cartoes no banco de dados."""

    # Criando os cursores da conexao
    cursor = db.cursor()
    cursor_consulta = db.cursor()

    # Verificando e criando as tabelas principais dos tipos e dos cartoes
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS TipoCardsCalculoMental'
        + ' (IdTipo INTEGER PRIMARY KEY AUTOINCREMENT,'
        + ' TipoOperacao TEXT KEY, DoisIntervalos INTEGER,'
        + ' Intervalo TEXT,'
        + ' NumNotes INTEGER, NumNotesFree INTEGER, NumCardsForNotes NUMBER)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS CardsCalculoMental'
        + ' (IdCard INTEGER NOT NULL,'
        + ' NomeCard TEXT NOT NULL, Card TEXT NOT NULL,'
        + ' NumCards INTEGER NOT NULL, DataPriRev TEXT NOT NULL,'
        + ' TipoCard INTEGER NOT NULL, FOREIGN KEY (TipoCard)'
        + ' REFERENCES TipoCardsCalculoMental(IdTipo))'
    )
    # verificando se sao dois intervalos para aplicar a formatacao correta
    # se este for o caso
    # criando a variável que vai contar o id dos arquivos
    cont_id = 1

    # inserino no DB de tipos as caracteristicas
    # dos cards que serao adicionados
    cursor.execute(
        'INSERT INTO TipoCardsCalculoMental'
        + ' (TipoOperacao, DoisIntervalos, '
        + 'Intervalo, NumNotes, NumNotesFree, NumCardsForNotes)'
        + f" VALUES ('{tipo_operacao}',"
        + f' {int(sao_dois_intervalos):.0f},'
        + f" '{intervalo[0]}-{intervalo[1]}',"
        + f' {len(list_card_final)}, {len(list_card_final)},'
        + f' {count_cards/len(list_card_final)})'
    )
    db.commit()
    for card_final in list_card_final:
        id_tipo_cards = cursor_consulta.execute(
            'SELECT IdTipo'
            + ' FROM TipoCardsCalculoMental'
            + ' ORDER BY IdTipo DESC LIMIT 2'
        ).fetchall()[0][0]
        # Adicionando o cartao no Banco de Dados
        cursor.execute(
            'INSERT INTO CardsCalculoMental'
            + ' (IdCard, NomeCard, Card, NumCards, DataPriRev, TipoCard)'
            + f' VALUES ({cont_id}, '
            + f"'{info_product[cont_id]['Nome']}', "
            + f"'{card_final}', "
            + f"{info_product[cont_id]['Número de Perguntas']},"
            + f" '-', {id_tipo_cards:.0f})"
        )
        cont_id += 1
        db.commit()
    # E encerrando a conexao
    cursor.close()
    cursor_consulta.close()
