import sqlite3 as sql
from random import shuffle

from AddAnkiCards.Db import DbConnect


def Embaralhe(combinacoes):
    """
    Funcao que embaralha todas as possibilidades encontradas
    pelo programa
    """
    # embaralhando
    shuffle(combinacoes)
    # retornando
    return combinacoes


def Distribua(
    combinacoes: list, quant_cards_por_d: int, num_max_cards: int
) -> list:
    """
    Funcao que distribui em listas ─ uma para cada cartao adicionado por dia ─
    as possibilidades encontradas.
    """
    # variavel que divide os valores da lista igualmente entre a
    # quantidade de cartoes por dia
    divisoria = len(combinacoes) / quant_cards_por_d
    # criando a lista que vai conter as listas separadas
    lista_separada = []
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
    # retornando a lista
    return lista_separada


def Armazene(
    combinacoes: list,
    operacoes: str,
    sao_dois_intervalos: bool,
    intervalo: list,
    conexaoDb: sql.connect = DbConnect.DbConnect('GeneralDb.db'),
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
        + ' Intervalo TEXT)'
    )
    Cursor.execute(
        'CREATE TABLE IF NOT EXISTS CardsCalculoMental'
        + ' (IdCard INTEGER NOT NULL,'
        + ' NomeCard TEXT NOT NULL, Card TEXT NOT NULL,'
        + ' NumCards INTEGER, DataPriRev TEXT NOT NULL,'
        + ' TipoCard INTEGER NOT NULL, FOREIGN KEY (TipoCard)'
        + ' REFERENCES TipoCardsCalculoMental(IdTipo))'
    )
    # verificando se sao dois intervalos para aplicar a formatacao correta
    # se este for o caso
    if sao_dois_intervalos:
        # caso seja aplicando as formatacoes
        intervalo[0] = '(%02i-%02i)' % (intervalo[0][0], intervalo[0][1])
        intervalo[1] = '(%02i-%02i)' % (intervalo[1][0], intervalo[1][1])
    # criando a lista com as informacoes dos resultados
    informacoes_do_produto = {}
    # criando a variável que vai contar o id dos arquivos
    cont_id = 0

    # inserino no DB de tipos as caracteristicas
    # dos cards que serao adicionados
    Cursor.execute(
        'INSERT INTO TipoCardsCalculoMental'
        + ' (TipoOperacao, DoisIntervalos, Intervalo)'
        + f" VALUES ('{operacoes}',"
        + f' {int(sao_dois_intervalos):.0f},'
        + f" '{intervalo[0]}-{intervalo[1]}')"
    )
    ConexaoDB.commit()

    # passando por todas as listas de combinacao
    for lista_operacoes in combinacoes:
        # adicionando a variavel contadora de id
        cont_id += 1
        # Adicionando o nome no dicionário de informacoes do produto
        informacoes_do_produto[cont_id] = {
            'Nome': 'Treinamento_de_%s_entre_%s-%s_id_%03i'
            % (operacoes, intervalo[0], intervalo[1], cont_id)
        }
        # verificando se a operacao é uma soma
        if operacoes == 'som':
            # passando por todos valores das listas
            for conta in lista_operacoes:
                # calculando o resultado da conta
                resultado = conta[0] + conta[1]
                # adicionando o resultado na lista
                conta.append(resultado)
            # informando o sinal da operacao
            operacoes_auxi = '+'
        # verificando se a operacao é uma subtracao
        elif operacoes == 'sub':
            # passando por todos os valores da lista
            # para caucular os resultados
            for conta in lista_operacoes:
                # calculando o resultado da subtracao
                resultado = conta[0] - conta[1]
                # adicionando o resultado na lista do cálculo
                conta.append(resultado)
            # informando o sinal da operacao
            operacoes_auxi = '-'
        # verificando se a operacao é uma multiplicacao
        elif operacoes == 'mul':
            # passando por todos os valores da lista para
            # calcular os resultados
            for conta in lista_operacoes:
                # cauculando o resultado da conta
                resultado = conta[0] * conta[1]
                # adicionando o resultado da conta na lista
                conta.append(resultado)
            # informando o sinal da operacao
            operacoes_auxi = '*'
        # descobrindo que a operacao é uma divisao
        else:
            # passnado por todos valores da lista para caucular os resultados
            for conta in lista_operacoes:
                # cauculando o resultado com duas casas decimais
                resultado = (conta[0] * 100 // conta[1]) / 100
                # adicionando o resultado na lista
                conta.append(resultado)
            # informando o sinal da operacao
            operacoes_auxi = '/'
        # criando a variavel pulei linha como true para o programa
        # comecar sem pular uma linha
        pulei_linha = True

        # criando a variavel que vai contar os numeros dos clozes
        cont_cloze = 0

        # Formatando o titulo do cartao e iniciando
        # a criacao da string do cartao
        CardTitle = (
            f'Treinamento_de_{operacoes}_entre_'
            + f'{intervalo[0]}-{intervalo[1]}_id_{cont_id}'
        )
        CardFinal = f'<h2>{CardTitle}</h2>\n<p>'
        # passando por todos elementos cauculados da lista para aplicar a
        # formatacao que vai nos cartoes as combinacoes nos arquivos
        for combinado in lista_operacoes:
            # verificando se eu pulei uma linha no ciclo passado
            # caso nao tenha entrando na tomada de desicao
            # de pular uma linha
            if not pulei_linha:
                # adicionando a variavel do cloze
                cont_cloze += 1

                # escrevendo o valor do cálculo no arquivo já com a formatacao
                CardFinal += (
                    f'{combinado[0]:>2} {operacoes_auxi} '
                    + f'{combinado[1]:>2} = '
                    + f'{{{{c{cont_cloze}::{combinado[2]:^4}}}}}'
                    + '<br>\n\n'
                )
                # informando o programa que ele pulou uma linha
                pulei_linha = True
            # caso o programa tenha pulado uma linha da ultima vez
            else:
                # adicionando a variavel do cloze
                cont_cloze += 1
                # escrevendo o valor do cálculo no arquivo já com a formatacao
                CardFinal += (
                    f'{combinado[0]:>2} {operacoes_auxi} '
                    + f'{combinado[1]:>2} = '
                    + f'{{{{c{cont_cloze}::{combinado[2]:^4}}}}}'
                    + ' |   | '
                )
                # informando o programa que ele nao puluo uma linha
                pulei_linha = False
        # adicionando a quantidade de cartoes no dicionário
        # de informacoes do produto
        informacoes_do_produto[cont_id]['Número de Perguntas'] = cont_cloze

        idTipoCards = CursorConsulta.execute(
            'SELECT IdTipo'
            + ' FROM TipoCardsCalculoMental'
            + ' ORDER BY IdTipo DESC LIMIT 2'
        ).fetchall()[0][0]
        # Adicionando o cartao no Banco de Dados
        Cursor.execute(
            'INSERT INTO CardsCalculoMental'
            + ' (IdCard, NomeCard, Card, NumCards, DataPriRev, TipoCard)'
            + f" VALUES ({cont_id}, '{CardTitle}', "
            + f"'{CardFinal}',{cont_cloze}, '-', {idTipoCards:.0f})"
        )
        ConexaoDB.commit()
    # E encerrando a conexao
    Cursor.close()
    CursorConsulta.close()
    ConexaoDB.close()
    return informacoes_do_produto
