def Pergunte():
    """
    Funcao que pede informacoes necessárias para o usuário, como:
     - Quantidade de cartoes a serem adicionados por dia;
     - Intervalo dos algaritimos que serao adicionados; e
     - Se existira o número máximo de possibilidades criadas.
    E informa o usuário sobre:
     - O Funcionamento do programa;
     - Total das possibilidades; e
     - Número de dias que ele vai demorar para finalizar os cartoes,
       conforme a variacao do número de cards respondidos por dia.
    """
    # pedindo que o usuário informe o intervalo das combinacoes
    # crinado a lista que vai contar os valores do intervalo
    intervalo = []
    # perduntando se o usuário vai querer
    # treinar com dois intervalos diferentes
    while True:
        Quant_de_intervalo = input(
            """
Você Deseja escolher 1 ou 2 intervalos para as combinacoes?
1 Intervalo:
 Sem repeticoes e somente os números deste intervalo"""
            + """ serao combinados (1-para escolher)\n
2 Intervalos:
 Com repeticoes se um intervalo conter o outro e os números de um
intervalo serao combinados com os números do outro (2-para escolher)\n"""
        )
        # fazendo a verifivcacao de erros
        if Quant_de_intervalo == '1' or Quant_de_intervalo == '2':
            # Verificando se o usuário nao digitou errado
            if (
                input(
                    '\nVocê deseja confirmar a sua escolha? (s-sim/n-nao)'
                    + '\nEscolha = %s\n' % Quant_de_intervalo
                )
                .lower()
                .startswith('s')
            ):
                # caso tenha pulando uma linha e saindo da verificacao de erros
                print()
                break
            # caso nao tenha
            else:
                # o informando
                print('\nOk. Perguntando novamente.\n')
                # e voltando para o inicio do while loop para evitar a
                # mensagem de erro de quando o programa nao reconhece a entrada
                continue
        # mostrando que a entrada nao foi reconhecida
        print('Entrada nao Reconhecida\n')
    # caso o usuário tenha decidido trabalhar com um intervalo
    if Quant_de_intervalo == '1':
        # informando a funcao principal do program da escolha
        sao_dois_intervalos = False
        # redefinido o valor de intervalo já com os valor máximo
        # e mínimo
        intervalo = pede_valores_dos_intervalos()
    # caso o usuário tenha escolhido dois intervalos
    else:
        # informando a funcao principal
        sao_dois_intervalos = True
        # informando o usuário que estamos pedindo os valores
        # do primeiro intervlao
        print('\nPedindo os valores do intervalo 1\n')
        # pedindo os valores
        intervalo.append(pede_valores_dos_intervalos())
        # informando o usuário que estamos pedindo os valores
        # do segundo intervlao
        print('\nPedindo os valores do intervalo 2\n')
        # pedindo os valores
        intervalo.append(pede_valores_dos_intervalos())
        # pedindo a quantidade máxima de cartoes para o usuário
        # entrando na verificacao de erros
    while True:
        # perguntando se o usuário quer uma quantidade máxima de cartoes
        if (
            input(
                'Você deseja que os cartoes tenham uma quantidade máxima?'
                + ' s-sim/n-nao: '
            )
            .lower()
            .startswith('s')
        ):
            # entrando na verificacao de erros
            while True:
                # pedindo a quantidade máxima dos cartoes
                num_max_cards = input(
                    'Digite a quantidade máxima de cartoes: '
                )
                # verificando que o usuário digitou apenas digitos
                if num_max_cards.isdigit():
                    # se sim transformando a entrada em um inteiro e
                    num_max_cards = int(num_max_cards)
                    # saindo da verificacao de erros
                    break
                # caso o usuário nao tanhe digitados apenas números
                print('Digite apenas números.')
        # caso o usuário nao queira uma quantidade máxima
        else:
            # informando o programa sobre a escolha do usuário
            num_max_cards = 'n'
            # perguntando se a informacao está correta
            if (
                input(
                    'Você deseja prosseguir? Número máximo de cartoes = '
                    + '%s s-sim/n-nao: ' % num_max_cards
                )
                .lower()
                .startswith('s')
            ):
                # caso esteja, pulando uma linha e
                print()
                # saindo do programa
                break
            # caso nao esteja informando o usuário e
            print('OK, perguterei os dados novamente.\n')
            # perguntando os dados novamente
            continue
        # caso o usuário queira uma quantidade máxima de cartoes,
        # verificando se ele a informou corretamente
        if (
            input(
                'Você deseja prosseguir? Número máximo de cartoes= '
                + '%i s-sim/n-nao: ' % num_max_cards
            )
            .lower()
            .startswith('s')
        ):
            # pulando uma linha e
            print()
            # saindo da verificacao de erros
            break
        # caso o usuário tenha digitado uma informacao errada
        print('OK, perguterei os dados novamente.\n')

    # perguntando a quantidade de cartoes que serao respondido por dia
    # entrando na verificacao de erros
    while True:
        # pedindo a informacao para o usuário
        quant_cards_por_d = input(
            'Digite quantos cartoes você quer responder por dia: '
        )
        # verificando se ele digitou apenas digitos
        if quant_cards_por_d.isdigit():
            # caso tenha, transformando a entrada em um inteiro
            quant_cards_por_d = int(quant_cards_por_d)
            # perguntando se o usuário digitou as informacoes corretamente
            if (
                input(
                    'Você deseja prosseguir? Quantidade de cartoes por dia '
                    + '= %i s-sim/n-nao: ' % quant_cards_por_d
                )
                .lower()
                .startswith('s')
            ):
                # caso tenha, pulando uma linha e
                print()
                # saindo da verificacao de erros
                break
            # caso tenha digitado errado, perguntando novamente
            print('Ok, perguntando os dados novamente.\n')
    # pedindo a informacao sobre as operacoes que serao treinadas
    # entrando na verificacao de erros
    while True:
        # pedindo a informacao para o usuário
        operacao = input(
            'Digite qual operacao você quer treinar'
            + ' (som = +, sub = -, mul = * , div = /): '
        )
        # verificando se ela está dentro de uma das opicoes
        if operacao == 'som' or operacao == ('sub') or operacao == 'mul':
            # caso esteja saindo da verificacao
            break
        # verificando se a operacao é uma divisao separadamente
        # para verificar o caso o valor mínimo seja zero
        elif operacao == 'div':
            # caso ele seja
            if intervalo[0] == 0:
                # adicionando 1 para que futuros erros nao ocorram
                intervalo[0] += 1
            # saindo da verificacao de erros
            break
        # caso nao, informando o usuário e perguntando novamente
        print('Entrada nao reconhecida. Perguntando novamente.\n')
    # retornando os valores para a funacao principal
    return (
        quant_cards_por_d,
        sao_dois_intervalos,
        intervalo,
        num_max_cards,
        operacao,
    )


def pede_valores_dos_intervalos():
    """
    Funcao que pede os valores máximos e mínimos dos intervalos
    para as combinacoes
    """
    # criando a lista que vai conter o valor máximo e mínimo do intervalo
    intervalo = []
    # pedindo o valor mínimo do intervalo
    # entrando na verificacao de erros
    while True:
        # pedindo que o usuário de a entrada do valor mínimo
        num_min_intervalo = input(
            'Digite o valor mínimo do intervalo que você deseja treinar: '
        )
        # verificando se o usuário digitou apenas números
        if num_min_intervalo.isdigit():
            # caso tenha transformando ele em um inteiro
            num_min_intervalo = int(num_min_intervalo)
            # verificando se o usuário concorda com a entrada
            if (
                input(
                    'Você deseja que o valor mínimo do intervalo Seja '
                    + '%i? s-sim/n-nao: ' % num_min_intervalo
                )
                .lower()
                .startswith('s')
            ):
                # pulando uma linha para facilitar a visualizacao
                print()
                # caso concorde saindo da verificacao de erros
                break
        # caso o usuário nao tenha digitado apenas números
        else:
            # o informando do que aconteceu
            print('Digite somente números')
            # reiniciando o while loop
            continue
        # caso o usuário nao tenha concordado com a
        # entrada anterior dele
        print('Ok. Perguntando novamente.\n')
    # pedindo o valor máximo do intervalo
    # entrando na verificacao de erros
    while True:
        # pedindo para o usuário informar o número máximo do intervalo
        num_max_intervalo = input(
            'Digite o valor máximo do intervalo você deseja treinar: '
        )
        # verificando se ele digitou apenas números
        if num_max_intervalo.isdigit():
            # caso sim, transformando a entrada em um inteiro
            num_max_intervalo = int(num_max_intervalo)
            # verificando se o usuário digitou corretamente os valores
            if (
                input(
                    'Você deseja que o valor máximo do '
                    + 'intervalo Seja %i? s-sim/n-nao: ' % num_max_intervalo
                )
                .lower()
                .startswith('s')
            ):
                # caso tenha pulando uma linhe e
                print()
                # saindo da verificacao de erros
                break
        # caso o usuário nao tenha digitado apenas números
        else:
            # o informando e
            print('Digite somente números')
            # reiniciando a verificacao de erros
            continue
        # caso o usuário tenha digitado uma informacao errada
        print('Ok. Perguntando novamente.\n')
    # adicionando os valores na lista
    intervalo.append(num_min_intervalo)
    intervalo.append(num_max_intervalo)
    return intervalo


def informe(informacoes_do_produto):
    """
    Funcao que informa o usuário o nome dos arquivos dos cartoes
    e quantas perguntas tem em cada cartao
    """
    # Informando ao usuário os nomes dos cartoes
    print('\nMostrando Os Nomes dos Cartoes:\n')
    # passando por todos os nomes presentes no dicionário
    for mostra_nome in informacoes_do_produto:
        # mostrando cada um dos nomes
        print(informacoes_do_produto[mostra_nome]['Nome'])
    # informando o usuário que os números de perguntas em cada cartao
    print('\nMostrando O Número de Perguntas\n')
    # passando por todos os dados das perguntas do dicionário
    for mostra_perguntas in informacoes_do_produto:
        # mostrando a quantidade
        print(informacoes_do_produto[mostra_perguntas]['Número de Perguntas'])
    # informando o Fim do programa
    print('\nFim do Programa.')
