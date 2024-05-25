def Pergunte():
    """
    Função que pede informações necessárias para o usuário, como:
     - Quantidade de cartões a serem adicionados por dia;
     - Intervalo dos algaritimos que serão adicionados; e
     - Se existira o número máximo de possibilidades criadas.
    E informa o usuário sobre:
     - O Funcionamento do programa;
     - Total das possibilidades; e
     - Número de dias que ele vai demorar para finalizar os cartões,
       conforme a variação do número de cards respondidos por dia.
    """
    # pedindo que o usuário informe o intervalo das combinações
    # crinado a lista que vai contar os valores do intervalo
    intervalo = []
    # perduntando se o usuário vai querer
    # treinar com dois intervalos diferentes
    while True:
        Quant_de_intervalo = input('''
Você Deseja escolher 1 ou 2 intervalos para as combinações?
1 Intervalo:
 Sem repetições e somente os números deste intervalo''' +
                                   ''' serão combinados (1-para escolher)\n
2 Intervalos:
 Com repetições se um intervalo conter o outro e os números de um
intervalo serão combinados com os números do outro (2-para escolher)\n''')
        # fazendo a verifivcação de erros
        if Quant_de_intervalo == "1" or Quant_de_intervalo == "2":
            # Verificando se o usuário não digitou errado
            if input("\nVocê deseja confirmar a sua escolha? (s-sim/n-não)" +
                     "\nEscolha = %s\n" % Quant_de_intervalo
                     ).lower().startswith("s"):
                # caso tenha pulando uma linha e saindo da verificação de erros
                print()
                break
            # caso não tenha
            else:
                # o informando
                print("\nOk. Perguntando novamente.\n")
                # e voltando para o inicio do while loop para evitar a
                # mensagem de erro de quando o programa não reconhece a entrada
                continue
        # mostrando que a entrada não foi reconhecida
        print("Entrada não Reconhecida\n")
    # caso o usuário tenha decidido trabalhar com um intervalo
    if Quant_de_intervalo == "1":
        # informando a função principal do program da escolha
        são_dois_intervalos = False
        # redefinido o valor de intervalo já com os valor máximo
        # e mínimo
        intervalo = pede_valores_dos_intervalos()
    # caso o usuário tenha escolhido dois intervalos
    else:
        # informando a função principal
        são_dois_intervalos = True
        # informando o usuário que estamos pedindo os valores
        # do primeiro intervlao
        print("\nPedindo os valores do intervalo 1\n")
        # pedindo os valores
        intervalo.append(pede_valores_dos_intervalos())
        # informando o usuário que estamos pedindo os valores
        # do segundo intervlao
        print("\nPedindo os valores do intervalo 2\n")
        # pedindo os valores
        intervalo.append(pede_valores_dos_intervalos())
        # pedindo a quantidade máxima de cartões para o usuário
        # entrando na verificação de erros
    while True:
        # perguntando se o usuário quer uma quantidade máxima de cartões
        if input("Você deseja que os cartões tenham uma quantidade máxima?" +
                 " s-sim/n-não: ").lower().startswith("s"):
            # entrando na verificação de erros
            while True:
                # pedindo a quantidade máxima dos cartões
                num_max_cards = input(
                    "Digite a quantidade máxima de cartões: ")
                # verificando que o usuário digitou apenas digitos
                if num_max_cards.isdigit():
                    # se sim transformando a entrada em um inteiro e
                    num_max_cards = int(num_max_cards)
                    # saindo da verificação de erros
                    break
                # caso o usuário não tanhe digitados apenas números
                print("Digite apenas números.")
        # caso o usuário não queira uma quantidade máxima
        else:
            # informando o programa sobre a escolha do usuário
            num_max_cards = "n"
            # perguntando se a informação está correta
            if input("Você deseja prosseguir? Número máximo de cartões = " +
                     "%s s-sim/n-não: " % num_max_cards).lower(
            ).startswith("s"):
                # caso esteja, pulando uma linha e
                print()
                # saindo do programa
                break
            # caso não esteja informando o usuário e
            print("OK, perguterei os dados novamente.\n")
            # perguntando os dados novamente
            continue
        # caso o usuário queira uma quantidade máxima de cartões,
        # verificando se ele a informou corretamente
        if input("Você deseja prosseguir? Número máximo de cartões= " +
                 "%i s-sim/n-não: " % num_max_cards).lower().startswith("s"):
            # pulando uma linha e
            print()
            # saindo da verificação de erros
            break
        # caso o usuário tenha digitado uma informação errada
        print("OK, perguterei os dados novamente.\n")

    # perguntando a quantidade de cartões que serão respondido por dia
    # entrando na verificação de erros
    while True:
        # pedindo a informação para o usuário
        quant_cards_por_d = input(
            "Digite quantos cartões você quer responder por dia: ")
        # verificando se ele digitou apenas digitos
        if quant_cards_por_d.isdigit():
            # caso tenha, transformando a entrada em um inteiro
            quant_cards_por_d = int(quant_cards_por_d)
            # perguntando se o usuário digitou as informações corretamente
            if input("Você deseja prosseguir? Quantidade de cartões por dia " +
                     "= %i s-sim/n-não: " %
                     quant_cards_por_d).lower().startswith("s"):
                # caso tenha, pulando uma linha e
                print()
                # saindo da verificação de erros
                break
            # caso tenha digitado errado, perguntando novamente
            print("Ok, perguntando os dados novamente.\n")
    # pedindo a informação sobre as operações que serão treinadas
    # entrando na verificação de erros
    while True:
        # pedindo a informação para o usuário
        operação = input("Digite qual operação você quer treinar" +
                         " (som = +, sub = -, mul = * , div = /): ")
        # verificando se ela está dentro de uma das opições
        if operação == "som" or operação == (
                "sub") or operação == "mul":
            # caso esteja saindo da verificação
            break
        # verificando se a operação é uma divisão separadamente
        # para verificar o caso o valor mínimo seja zero
        elif operação == "div":
            # caso ele seja
            if intervalo[0] == 0:
                # adicionando 1 para que futuros erros não ocorram
                intervalo[0] += 1
            # saindo da verificação de erros
            break
        # caso não, informando o usuário e perguntando novamente
        print("Entrada não reconhecida. Perguntando novamente.\n")
    # retornando os valores para a funação principal
    return (quant_cards_por_d, são_dois_intervalos,
            intervalo, num_max_cards, operação)


def pede_valores_dos_intervalos():
    '''
    Função que pede os valores máximos e mínimos dos intervalos
    para as combinações
    '''
    # criando a lista que vai conter o valor máximo e mínimo do intervalo
    intervalo = []
    # pedindo o valor mínimo do intervalo
    # entrando na verificação de erros
    while True:
        # pedindo que o usuário de a entrada do valor mínimo
        num_min_intervalo = input(
            "Digite o valor mínimo do intervalo que você deseja treinar: ")
        # verificando se o usuário digitou apenas números
        if num_min_intervalo.isdigit():
            # caso tenha transformando ele em um inteiro
            num_min_intervalo = int(num_min_intervalo)
            # verificando se o usuário concorda com a entrada
            if input("Você deseja que o valor mínimo do intervalo Seja " +
                     "%i? s-sim/n-não: " % num_min_intervalo).lower(
            ).startswith("s"):
                # pulando uma linha para facilitar a visualização
                print()
                # caso concorde saindo da verificação de erros
                break
        # caso o usuário não tenha digitado apenas números
        else:
            # o informando do que aconteceu
            print("Digite somente números")
            # reiniciando o while loop
            continue
        # caso o usuário não tenha concordado com a
        # entrada anterior dele
        print("Ok. Perguntando novamente.\n")
    # pedindo o valor máximo do intervalo
    # entrando na verificação de erros
    while True:
        # pedindo para o usuário informar o número máximo do intervalo
        num_max_intervalo = input(
            "Digite o valor máximo do intervalo você deseja treinar: ")
        # verificando se ele digitou apenas números
        if num_max_intervalo.isdigit():
            # caso sim, transformando a entrada em um inteiro
            num_max_intervalo = int(num_max_intervalo)
            # verificando se o usuário digitou corretamente os valores
            if input("Você deseja que o valor máximo do " +
                     "intervalo Seja %i? s-sim/n-não: " % num_max_intervalo
                     ).lower().startswith("s"):
                # caso tenha pulando uma linhe e
                print()
                # saindo da verificação de erros
                break
        # caso o usuário não tenha digitado apenas números
        else:
            # o informando e
            print("Digite somente números")
            # reiniciando a verificação de erros
            continue
        # caso o usuário tenha digitado uma informação errada
        print("Ok. Perguntando novamente.\n")
    # adicionando os valores na lista
    intervalo.append(num_min_intervalo)
    intervalo.append(num_max_intervalo)
    return intervalo


def informe(informações_do_produto):
    """
    Função que informa o usuário o nome dos arquivos dos cartões
    e quantas perguntas tem em cada cartão
    """
    # Informando ao usuário os nomes dos cartões
    print("\nMostrando Os Nomes dos Cartões:\n")
    # passando por todos os nomes presentes no dicionário
    for mostra_nome in informações_do_produto:
        # mostrando cada um dos nomes
        print(informações_do_produto[mostra_nome]["Nome"])
    # informando o usuário que os números de perguntas em cada cartão
    print("\nMostrando O Número de Perguntas\n")
    # passando por todos os dados das perguntas do dicionário
    for mostra_perguntas in informações_do_produto:
        # mostrando a quantidade
        print(informações_do_produto[mostra_perguntas]["Número de Perguntas"])
    # informando o Fim do programa
    print("\nFim do Programa.")
