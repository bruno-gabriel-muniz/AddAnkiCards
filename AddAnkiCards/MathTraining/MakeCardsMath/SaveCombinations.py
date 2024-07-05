import sqlite3 as sql
from random import shuffle

from AddAnkiCards.Db import DbConnect


def embaralhe(combinacoes):
    """
    Funcao que embaralha todas as possibilidades encontradas
    pelo programa
    """
    # embaralhando
    shuffle(combinacoes)
    # retornando
    return combinacoes


def distribua(
    combinacoes: list, quant_cards_por_d: int, num_max_cards: int
) -> tuple[list, int]:
    """
    Funcao que distribui em listas ─ uma para cada cartao adicionado por dia ─
    as possibilidades encontradas.
    """
    # variavel que divide os valores da lista igualmente entre a
    # quantidade de cartoes por dia
    divisoria = len(combinacoes) / quant_cards_por_d
    # criando a lista que vai conter as listas separadas
    lista_separada = []
    countCards = 0
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
            countCards += len(lista_separada[-1])
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
            countCards += len(lista_separada[-1])
    # caso tenha e nao ultrapase a divisoria
    else:
        countCards = 0
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
            countCards += len(lista_separada[-1])
        if countCards > num_max_cards:
            lista_separada[-1].pop()
    # retornando a lista e a quantidade de cartoes
    return lista_separada, countCards


def calcula(combinacoes: list, operacao: str) -> str:
    """
    Funcao que calcula os resultados das combinacoes sendo
    operadas pelos operadores (+, -, *, /).
    """
    if operacao == 'som':
        operatorAuxi = '+'
        #
        # passamos por todos os cards
        for combinacoesSeparadas in combinacoes:
            #
            # passamos por todos as combinacoes
            #
            for combinacao in combinacoesSeparadas:
                # calculamos o valor de cada combinacao e
                # adcionamos os valores delas no ultimo indice da lista
                resultado = combinacao[0] + combinacao[1]
                combinacao.append(resultado)
    elif operacao == 'sub':
        operatorAuxi = '-'
        for combinacoesSeparadas in combinacoes:
            for combinacao in combinacoesSeparadas:
                resultado = combinacao[0] - combinacao[1]
                combinacao.append(resultado)
    elif operacao == 'mul':
        operatorAuxi = '*'
        for combinacoesSeparadas in combinacoes:
            for combinacao in combinacoesSeparadas:
                resultado = combinacao[0] * combinacao[1]
                combinacao.append(resultado)
    elif operacao == 'div':
        operatorAuxi = '/'
        for combinacoesSeparadas in combinacoes:
            for combinacao in combinacoesSeparadas:
                resultado = (combinacao[0] * 100 // combinacao[1]) / 100
                combinacao.append(resultado)
    else:
        raise ValueError(
            'A operacao so pode ser "som", "sub", "mul" ou '
            + '"div" com estes mesmos caracteres'
        )
    return operatorAuxi


def formata(
    combinacoes: list,
    operatorAuxi: str,
    operator: str,
    intervalo: list,
    contId: int,
    infoProduto: dict,
) -> str:
    """ """
    pulei_linha = True

    # criando a variavel que vai contar os numeros dos clozes
    cont_cloze = 0

    # Formatando o titulo do cartao e iniciando
    # a criacao da string do cartao
    CardTitle = (
        f'Treinamento_de_{operator}_entre_'
        + f'{intervalo[0]}-{intervalo[1]}_id_{contId}'
    )
    infoProduto[contId] = {'Nome': CardTitle}
    cardFinal = f'<h2>{CardTitle}</h2>\n<p>'
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
            cardFinal += (
                f'{combinado[0]:_>2} {operatorAuxi} '
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
            cardFinal += (
                f'{combinado[0]:_>2} {operatorAuxi} '
                + f'{combinado[1]:_>2} = '
                + f'{{{{c{cont_cloze}::{combinado[2]:_^4}}}}}'
                + '|----------|'
            )
            # informando o programa que ele nao puluo uma linha
            pulei_linha = False
    # adicionando a quantidade de cartoes no dicionário
    # de informacoes do produto
    infoProduto[contId]['Número de Perguntas'] = cont_cloze
    return cardFinal


def armazene(
    listCardFinal: list,
    tipoOperacao: str,
    saoDoisIntervalos: bool,
    intervalo: list,
    countCards: int,
    infoProduct: dict,
    conexaoDb: sql.connect = DbConnect.DbConnect('GeneralDB.db'),
) -> dict:
    """
    Funcao que armazena os valores dos cartoes em um banco de dados
    e realiza as opercaoes que eles foram feitos para treinar
    """

    # Criando a conexao com o Banco de Dados
    ConexaoDB = conexaoDb

    # Criando os cursores da conexao
    Cursor = ConexaoDB.cursor()
    CursorConsulta = ConexaoDB.cursor()

    # Verificando e criando as tabelas principais dos tipos e dos cartoes
    Cursor.execute(
        'CREATE TABLE IF NOT EXISTS TipoCardsCalculoMental'
        + ' (IdTipo INTEGER PRIMARY KEY AUTOINCREMENT,'
        + ' TipoOperacao TEXT KEY, DoisIntervalos INTEGER,'
        + ' Intervalo TEXT,'
        + ' NumNotes INTEGER, NumNotesFree INTEGER, NumCardsForNotes NUMBER)'
    )
    Cursor.execute(
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
    Cursor.execute(
        'INSERT INTO TipoCardsCalculoMental'
        + ' (TipoOperacao, DoisIntervalos, '
        + 'Intervalo, NumNotes, NumNotesFree, NumCardsForNotes)'
        + f" VALUES ('{tipoOperacao}',"
        + f' {int(saoDoisIntervalos):.0f},'
        + f" '{intervalo[0]}-{intervalo[1]}',"
        + f' {len(listCardFinal)}, {len(listCardFinal)},'
        + f' {countCards/len(listCardFinal)})'
    )
    ConexaoDB.commit()
    for cardFinal in listCardFinal:
        idTipoCards = CursorConsulta.execute(
            'SELECT IdTipo'
            + ' FROM TipoCardsCalculoMental'
            + ' ORDER BY IdTipo DESC LIMIT 2'
        ).fetchall()[0][0]
        # Adicionando o cartao no Banco de Dados
        Cursor.execute(
            'INSERT INTO CardsCalculoMental'
            + ' (IdCard, NomeCard, Card, NumCards, DataPriRev, TipoCard)'
            + f' VALUES ({cont_id}, '
            + f"'{infoProduct[cont_id]['Nome']}', "
            + f"'{cardFinal}', "
            + f"{infoProduct[cont_id]['Número de Perguntas']},"
            + f" '-', {idTipoCards:.0f})"
        )
        cont_id += 1
        ConexaoDB.commit()
    # E encerrando a conexao
    Cursor.close()
    CursorConsulta.close()
    ConexaoDB.close()
