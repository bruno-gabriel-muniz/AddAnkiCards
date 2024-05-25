from random import shuffle
import sqlite3 as sql


def Embaralhe(combinações):
    """
    Função que embaralha todas as possibilidades encontradas
    pelo programa
    """
    # embaralhando
    shuffle(combinações)
    # retornando
    return combinações


def Distribua(combinações, quant_cards_por_d, num_max_cards):
    """
    Função que distribui em listas ─ uma para cada cartão adicionado por dia ─
    as possibilidades encontradas.
    """
    # variavel que divide os valores da lista igualmente entre a
    # quantidade de cartões por dia
    divisória = len(combinações)/quant_cards_por_d
    # criando a lista que vai conter as listas separadas
    lista_separada = []
    # verificando se possui um limite máximo para os cartões
    if num_max_cards == "n":
        # for loop que cria todas as listas
        for próximo in range(quant_cards_por_d):
            # adicionando a lista separada os cartões da lista
            lista_separada.append(
                combinações[round(próximo*divisória):
                            round((próximo+1)*divisória)])
    # verificando se o limite de cartões ultrapaça a divisória
    elif (num_max_cards//quant_cards_por_d) >= divisória:
        # for loop que cria as listas
        for próximo in range(quant_cards_por_d):
            # adicionando a lista separada os cartões da lista
            lista_separada.append(
                combinações[round(próximo*divisória):
                            round((próximo+1)*divisória)])
    # caso tenha e não ultrapase a divisória
    else:
        # for loop que cria as listas
        for próximo in range(quant_cards_por_d):
            # adicionando a lista separada os cartões da lista
            # levando em consideração o limite
            lista_separada.append(
                combinações[round(próximo*divisória):
                            round(próximo*divisória +
                            (num_max_cards/quant_cards_por_d))])
    # retornando a lista
    return lista_separada


def Armazene(combinações, operações, são_dois_intervalos, intervalo):
    """
    Função que armazena os valores dos cartões em um banco de dados
    e realiza as operçãoes que eles foram feitos para treinar
    """

    # Criando a conexão com o Banco de Dados
    ConexaoDB = sql.connect("GeneralDB.db")

    # Criando os cursores da conexão
    Cursor = ConexaoDB.cursor()
    CursorConsulta = ConexaoDB.cursor()

    # Verificando e criando as tabelas principais dos tipos e dos cartões
    Cursor.execute("CREATE TABLE IF NOT EXISTS TipoCardsCalculoMental" +
                   " (IdTipo INTEGER PRIMARY KEY AUTOINCREMENT," +
                   " TipoOperacao TEXT KEY, DoisIntervalos INTEGER," +
                   " Intervalo TEXT)")
    Cursor.execute("CREATE TABLE IF NOT EXISTS CardsCalculoMental" +
                   " (IdCard INTEGER NOT NULL," +
                   " NomeCard TEXT NOT NULL, Card TEXT NOT NULL," +
                   " DataPriRev TEXT NOT NULL," +
                   " TipoCard INTEGER NOT NULL, FOREIGN KEY (TipoCard)" +
                   " REFERENCES TipoCardsCalculoMental(IdTipo))")
    # verificando se são dois intervalos para aplicar a formatação correta
    # se este for o caso
    if são_dois_intervalos:
        # caso seja aplicando as formatações
        intervalo[0] = "(%02i-%02i)" % (intervalo[0][0], intervalo[0][1])
        intervalo[1] = "(%02i-%02i)" % (intervalo[1][0], intervalo[1][1])
    # criando a lista com as informações dos resultados
    informações_do_produto = {}
    # criando a variável que vai contar o id dos arquivos
    cont_id = 0

    # inserino no DB de tipos as caracteristicas
    # dos cards que serão adicionados
    Cursor.execute("INSERT INTO TipoCardsCalculoMental" +
                   " (TipoOperacao, DoisIntervalos, Intervalo)" +
                   f" VALUES ('{operações}'," +
                   f" {int(são_dois_intervalos):.0f}," +
                   f" '{intervalo[0]}-{intervalo[1]}')")
    ConexaoDB.commit()

    # passando por todas as listas de combinação
    for lista_operações in combinações:
        # adicionando a variavel contadora de id
        cont_id += 1
        # Adicionando o nome no dicionário de informações do produto
        informações_do_produto[cont_id] = {
            "Nome": "Treinamento_de_%s_entre_%s-%s_id_%03i" % (
                operações, intervalo[0], intervalo[1], cont_id)}
        # verificando se a operação é uma soma
        if operações == "som":
            # passando por todos valores das listas
            for conta in lista_operações:
                # calculando o resultado da conta
                resultado = conta[0]+conta[1]
                # adicionando o resultado na lista
                conta.append(resultado)
            # informando o sinal da operação
            operações_auxi = "+"
        # verificando se a operação é uma subtração
        elif operações == "sub":
            # passando por todos os valores da lista
            # para caucular os resultados
            for conta in lista_operações:
                # calculando o resultado da subtração
                resultado = conta[0]-conta[1]
                # adicionando o resultado na lista do cálculo
                conta.append(resultado)
            # informando o sinal da operação
            operações_auxi = "-"
        # verificando se a operação é uma multiplicação
        elif operações == "mul":
            # passando por todos os valores da lista para
            # calcular os resultados
            for conta in lista_operações:
                # cauculando o resultado da conta
                resultado = conta[0]*conta[1]
                # adicionando o resultado da conta na lista
                conta.append(resultado)
            # informando o sinal da operação
            operações_auxi = "*"
        # descobrindo que a operação é uma divisão
        else:
            # passnado por todos valores da lista para caucular os resultados
            for conta in lista_operações:
                # cauculando o resultado com duas casas decimais
                resultado = (conta[0]*100//conta[1])/100
                # adicionando o resultado na lista
                conta.append(resultado)
            # informando o sinal da operação
            operações_auxi = "/"
        # criando a variavel pulei linha como true para o programa
        # começar sem pular uma linha
        pulei_linha = True

        # criando a variavel que vai contar os numeros dos clozes
        cont_cloze = 0

        # Formatando o titulo do cartão e iniciando
        # a criação da string do cartão
        CardTitle = (f"Treinamento_de_{operações}_entre_" +
                     f"{intervalo[0]}-{intervalo[1]}_id_{cont_id}")
        CardFinal = (f"<h2>{CardTitle}</h2>\n<p>")
        # passando por todos elementos cauculados da lista para aplicar a
        # formatação que vai nos cartões as combinações nos arquivos
        for combinado in lista_operações:
            # verificando se eu pulei uma linha no ciclo passado
            # caso não tenha entrando na tomada de desição
            # de pular uma linha
            if not pulei_linha:
                # adicionando a variavel do cloze
                cont_cloze += 1

                # escrevendo o valor do cálculo no arquivo já com a formatação
                CardFinal += (f"{combinado[0]:>2} {operações_auxi} " +
                              f"{combinado[1]:>2} = " +
                              f"{{{{c{cont_cloze}::{combinado[2]:^4}}}}}<br>\n\n")
                # informando o programa que ele pulou uma linha
                pulei_linha = True
            # caso o programa tenha pulado uma linha da ultima vez
            else:
                # adicionando a variavel do cloze
                cont_cloze += 1
                # escrevendo o valor do cálculo no arquivo já com a formatação
                CardFinal += (f"{combinado[0]:>2} {operações_auxi} " +
                              f"{combinado[1]:>2} = " +
                              f"{{{{c{cont_cloze}::{combinado[2]:^4}}}}} |   | ")
                # informando o programa que ele não puluo uma linha
                pulei_linha = False
        # adicionando a quantidade de cartões no dicionário
        #  de informações do produto
        informações_do_produto[cont_id]["Número de Perguntas"] = cont_cloze

        # Adicionando o cartão no Banco de Dados
        Cursor.execute("INSERT INTO CardsCalculoMental" +
                       " (IdCard, NomeCard, Card, DataPriRev, TipoCard) VALUES" +
                       f" ({cont_id}, '{CardTitle}', " +
                       f"'{CardFinal}', '-', {CursorConsulta.execute(
                           "SELECT IdTipo" +
                           " FROM TipoCardsCalculoMental" +
                           " ORDER BY IdTipo DESC LIMIT 2").fetchall()[0][0]:.0f})")
        ConexaoDB.commit()
    # E encerrando a conexão
    Cursor.close()
    CursorConsulta.close()
    ConexaoDB.close()
    return informações_do_produto
