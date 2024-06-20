def FindCombSomMul(intervalo: list) -> list:
    """
    Funcao que acha todas as possibilidades da combinacao de dois números
    em determinado intervalo para operacoes de multiplicacpao e divisao.
    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no eltimo o máximo.
    """
    rangeIsValid(intervalo)
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


def FindCombSubDiv(intervalo: list) -> list:
    """
    Funcao que acha todas as possibilidades da combinacao de dois números
    em determinado intervalo para as operacoes de subtracao e divisao.
    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no eltimo o máximo.
    """
    rangeIsValid(intervalo)
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que conta a quantidade de cartoes
    cont = 0
    #
    # Passando por cada um dos numeros grandes fazendo todas as
    # combinacoes possiveis com eles diretamente. Assim, reduzindo
    # o loop pela metade
    for numero_grande in range(intervalo[0], intervalo[1] + 1):
        for numero_pequeno in range(numero_grande, intervalo[1] + 1):
            # Verificando se os numeros sao iguais para nao duplica-los
            if numero_grande == numero_pequeno:
                combinacoes.append([numero_pequeno, numero_grande])
                cont += 1
                continue
            cont += 2
            # adicionando a combinacao encontrada das duas forma possiveis
            combinacoes.append([numero_grande, numero_pequeno])
            combinacoes.append([numero_pequeno, numero_grande])
    # Contando para o usuário todas as possibilidades encontradas
    print('Foram encontradas %i possibilidades possíveis.' % cont)
    # returnando todas as possibiliades possíveis
    return combinacoes


def Find2CombSomMul(intervalo1: list, intervalo2: list) -> list:
    """
    Funcao que encontra Todas possibilidades das combinacoes de
    números entre dois intervalos para o treino de soma e multiplicacao
    """
    rangeIsValid2(intervalo1, intervalo2)
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


def Find2CombSubDiv(intervalo1: list, intervalo2: list) -> list:
    """
    Funcao que encontra Todas possibilidades das combinacoes de
    números entre dois intervalos para o treino de subtracao e divisao
    """
    rangeIsValid2(intervalo1, intervalo2)
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
            cont += 2
            # adicionando a combinacao encontrada na lista
            combinacoes.append([numero_intervalo1, numero_intervalo2])
            combinacoes.append([numero_intervalo2, numero_intervalo1])
    # Contando para o usuário todas as possibilidades encontradas
    print('Foram encontradas %i possibilidades possíveis.' % cont)
    # returnando todas as possibiliades possíveis
    return combinacoes


def rangesIntersect(intervalo1: list, intervalo2: list) -> bool:
    """
    Funcao que verifica se os intervalos se intersectao.
    """
    if intervalo1[0] <= intervalo2[0] and intervalo1[1] >= intervalo2[0]:
        return True
    if intervalo2[0] <= intervalo1[0] and intervalo2[1] >= intervalo1[0]:
        return True


def rangeIsNotEmpyt(intervalo: list) -> bool:
    """
    Funcao que verifica se o intervalo esta vazio.
    """
    if intervalo[0] >= intervalo[1]:
        return False
    return True


def rangeIsValid2(intervalo1: list, intervalo2: list) -> bool:
    """
    Verifica se os ranges das combinacoes de dois intervalos estao errados.
    """
    # Verificamos se os valores das entradas sao do tipo certo
    if not isinstance(intervalo1, (list, tuple)) or not isinstance(
        intervalo2, (list, tuple)
    ):
        raise TypeError('Os intervalos so podem ser listas ou tuplas')
    #
    # Verificamos se estao apenas com as estremidades dos intervalos
    if len(intervalo1) == len(intervalo2) == 2:
        #
        # Se os intervalos nao estao vazios
        if rangeIsNotEmpyt(intervalo1) and rangeIsNotEmpyt(intervalo2):
            #
            # e se eles nao estao dentro um do outro
            if not rangesIntersect(intervalo1, intervalo2):
                return True
            else:
                raise ValueError(
                    'Os intervalos, ('
                    f'{intervalo1}-{intervalo2}), se interssectam.'
                )
        raise ValueError(
            'Os intervalos tem que ter o menor valor primeiro'
            + ' e o maior depois [menor, maior]'
        )
    raise ValueError(
        'As listas que representam os intervalos so podem ter'
        + ' dois valores: o menor e o maior valor do intervalo'
    )


def rangeIsValid(intervalo):
    """
    Verifica se os ranges das combinacoes de um intervalo estao errados.
    """
    # Verificamos se o valores da entrada eh do tipo certo
    if not isinstance(intervalo, (list, tuple)):
        raise TypeError('O intervalo so pode ser listas ou tuplas')
    #
    # Se contem apenas as extramidades dos intervalos
    if len(intervalo) == 2:
        #
        # E se nao eh um intervalo vazio
        if rangeIsNotEmpyt(intervalo):
            return True
        raise ValueError(
            'O intervalo tem que ter o menor valor primeiro'
            + ' e o maior depois [menor, maior]'
        )
    raise ValueError(
        'A lista que representa o intervalo so pode ter'
        + ' dois valores: o menor e o maior valor do intervalo'
    )
