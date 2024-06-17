def FindCombSumMul(intervalo):
    """
    Funcao que acha todas as possibilidades da combinacao de dois números
    em determinado intervalo para operacoes de multiplicacpao e divisao.
    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no eltimo o máximo.
    """
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que cointa a quantidade de cartoes
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operacao
    for numero_grande in range(intervalo[0], intervalo[1] + 1):
        # passando por todas as possibilidades de números restantes
        for numero_pequeno in range(numero_grande, intervalo[1] + 1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinacao encontrada na lista
            combinacoes.append([numero_grande, numero_pequeno])
    # Contando para o usuário todas as possibilidades encontradas
    print('Foram encontradas %i possibilidades possíveis.' % cont)
    # returnando todas as possibiliades possíveis
    return combinacoes


def FindCombSubDiv(intervalo):
    """
    Funcao que acha todas as possibilidades da combinacao de dois números
    em determinado intervalo para as operacoes de subtracao e divisao.
    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no eltimo o máximo.
    """
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que cointa a quantidade de cartoes
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operacao
    for numero_grande in range(intervalo[0], intervalo[1] + 1):
        # passando por todas as possibilidades de números restantes
        for numero_pequeno in range(intervalo[0], intervalo[1] + 1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinacao encontrada na lista
            combinacoes.append([numero_grande, numero_pequeno])
    # Contando para o usuário todas as possibilidades encontradas
    print('Foram encontradas %i possibilidades possíveis.' % cont)
    # returnando todas as possibiliades possíveis
    return combinacoes


def Find2CombSumMul(intervalo1, intervalo2):
    """
    Funcao que encontra Todas possibilidades das combinacoes de
    números entre dois intervalos para o treino de soma e multiplicacao
    """
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que cointa a quantidade de combinacoes
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operacao
    for numero_intervalo1 in range(intervalo1[0], intervalo1[1] + 1):
        # passando por todas as possibilidades de números restantes
        for numero_intervalo2 in range(intervalo2[0], intervalo2[1] + 1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinacao encontrada na lista
            combinacoes.append([numero_intervalo1, numero_intervalo2])
    # Contando para o usuário todas as possibilidades encontradas
    print('Foram encontradas %i possibilidades possíveis.' % cont)
    # returnando todas as possibiliades possíveis
    return combinacoes


def Find2CombSubDiv(intervalo1, intervalo2):
    """
    Funcao que encontra Todas possibilidades das combinacoes de
    números entre dois intervalos para o treino de subtracao e divisao
    """
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que cointa a quantidade de combinacoes
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operacao
    for numero_intervalo1 in range(intervalo1[0], intervalo1[1] + 1):
        # passando por todas as possibilidades de números restantes
        for numero_intervalo2 in range(intervalo2[0], intervalo2[1] + 1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinacao encontrada na lista
            combinacoes.append([numero_intervalo1, numero_intervalo2])
            combinacoes.append([numero_intervalo2, numero_intervalo1])
    # Contando para o usuário todas as possibilidades encontradas
    print('Foram encontradas %i possibilidades possíveis.' % cont)
    # returnando todas as possibiliades possíveis
    return combinacoes
