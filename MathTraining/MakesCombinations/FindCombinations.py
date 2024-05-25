def FindCombSumMul(intervalo):
    """
    Função que acha todas as possibilidades da combinação de dois números
    em determinado intervalo para operações de multiplicaçpão e divisão.
    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no eltimo o máximo.
    """
    # criando a lista que vai conter as possibilidades
    combinações = []
    # criando a variavel que cointa a quantidade de cartões
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operação
    for numero_grande in range(intervalo[0], intervalo[1]+1):
        # passando por todas as possibilidades de números restantes
        for numero_pequeno in range(numero_grande, intervalo[1]+1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinação encontrada na lista
            combinações.append([numero_grande, numero_pequeno])
    # Contando para o usuário todas as possibilidades encontradas
    print("Foram encontradas %i possibilidades possíveis." % cont)
    # returnando todas as possibiliades possíveis
    return combinações


def FindCombSubDiv(intervalo):
    """
    Função que acha todas as possibilidades da combinação de dois números
    em determinado intervalo para as operações de subtração e divisão.
    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no eltimo o máximo.
    """
    # criando a lista que vai conter as possibilidades
    combinações = []
    # criando a variavel que cointa a quantidade de cartões
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operação
    for numero_grande in range(intervalo[0], intervalo[1]+1):
        # passando por todas as possibilidades de números restantes
        for numero_pequeno in range(intervalo[0], intervalo[1]+1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinação encontrada na lista
            combinações.append([numero_grande, numero_pequeno])
    # Contando para o usuário todas as possibilidades encontradas
    print("Foram encontradas %i possibilidades possíveis." % cont)
    # returnando todas as possibiliades possíveis
    return combinações


def Find2CombSumMul(intervalo1, intervalo2):
    '''
    Função que encontra Todas possibilidades das combinações de
    números entre dois intervalos para o treino de soma e multiplicação
    '''
    # criando a lista que vai conter as possibilidades
    combinações = []
    # criando a variavel que cointa a quantidade de combinações
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operação
    for numero_intervalo1 in range(intervalo1[0], intervalo1[1]+1):
        # passando por todas as possibilidades de números restantes
        for numero_intervalo2 in range(intervalo2[0], intervalo2[1]+1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinação encontrada na lista
            combinações.append([numero_intervalo1, numero_intervalo2])
    # Contando para o usuário todas as possibilidades encontradas
    print("Foram encontradas %i possibilidades possíveis." % cont)
    # returnando todas as possibiliades possíveis
    return combinações


def Find2CombSubDiv(intervalo1, intervalo2):
    '''
    Função que encontra Todas possibilidades das combinações de
    números entre dois intervalos para o treino de subtração e divisão
    '''
    # criando a lista que vai conter as possibilidades
    combinações = []
    # criando a variavel que cointa a quantidade de combinações
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operação
    for numero_intervalo1 in range(intervalo1[0], intervalo1[1]+1):
        # passando por todas as possibilidades de números restantes
        for numero_intervalo2 in range(intervalo2[0], intervalo2[1]+1):
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinação encontrada na lista
            combinações.append([numero_intervalo1, numero_intervalo2])
            combinações.append([numero_intervalo2, numero_intervalo1])
    # Contando para o usuário todas as possibilidades encontradas
    print("Foram encontradas %i possibilidades possíveis." % cont)
    # returnando todas as possibiliades possíveis
    return combinações
