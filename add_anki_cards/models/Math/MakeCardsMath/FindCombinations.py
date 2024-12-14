def find_comb_sum_mul(intervalo: list) -> list:
    """
    Func. q acha todas as comb. de 2 nums em um intervalo para soma e mul.

    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no segundo, e ultimo, o máximo.
    """
    range_is_valid(intervalo)
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que cointa a quantidade de cartoes
    cont = 0
    # passando por todas as possibilidades de números do lado
    # esquerdo da operacao
    begin, end = intervalo
    for num_big in range(begin, end+1):
        # passando por todas as possibilidades de números restantes
        num_lower = num_big
        while num_lower <= end:
            # adicionando a variável que conta as possibilidades
            cont += 1
            # adicionando a combinacao encontrada na lista
            combinacoes.append([num_lower, num_big])
            num_lower += 1
    # Contando para o usuário todas as possibilidades encontradas
    print(f'Foram encontradas {cont} possibilidades possíveis.')
    # returnando todas as possibiliades possíveis
    return combinacoes


def find_comb_sub_div(intervalo: list) -> list:
    """
    Func. q acha todas as comb. de 2 nums em um intervalo para sub e div.

    Como usar:
    ─ Argumentos: uma lista com no primerio índice o número mínimo
      do intervalo e no segundo, e ultimo, o máximo.
    """
    range_is_valid(intervalo)
    # criando a lista que vai conter as possibilidades
    combinacoes = []
    # criando a variavel que conta a quantidade de cartoes
    cont = 0
    #
    # Passando por cada um dos numeros grandes fazendo todas as
    # combinacoes possiveis com eles diretamente. Assim, reduzindo
    # o loop pela metade
    begin, end = intervalo
    for num_big in range(begin, end+1):
        combinacoes.append([num_big, num_big])
        num_lower = num_big+1
        cont += 1
        while num_lower <= end:
            cont += 2
            # adicionando a combinacao encontrada das duas forma possiveis
            combinacoes.append([num_big, num_lower])
            combinacoes.append([num_lower, num_big])
            num_lower += 1
    # Contando para o usuário todas as possibilidades encontradas
    print(f'Foram encontradas {cont} possibilidades possíveis.')
    # returnando todas as possibiliades possíveis
    return combinacoes


def find_2_comb_som_mul(intervalo1: list, intervalo2: list) -> list:
    """
    Func. q acha todas as comb. de 2 nums em dois intervalos para soma e mul.

    Como usar:
    ─ Argumentos: duas listas com no primerio índice o número mínimo
      do intervalo e no segundo, e ultimo, o máximo.
    ─ Retorno: uma lista com todas as possibilidades encontradas.
    """
    range_is_valid_2(intervalo1, intervalo2)
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
    print(f'Foram encontradas {cont} possibilidades possíveis.')
    # returnando todas as possibiliades possíveis
    return combinacoes


def find_2_comb_sub_div(intervalo1: list, intervalo2: list) -> list:
    """
    Func. q acha todas as comb. de 2 nums em dois intervalos para sub e div.

    Como usar:
    ─ Argumentos: duas listas com no primerio índice o número mínimo
      do intervalo e no segundo, e ultimo, o máximo.
    ─ Retorno: uma lista com todas as possibilidades encontradas.
    """
    range_is_valid_2(intervalo1, intervalo2)
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
    print(f'Foram encontradas {cont} possibilidades possíveis.')
    # returnando todas as possibiliades possíveis
    return combinacoes


def ranges_intersect(intervalo1: list, intervalo2: list) -> bool:
    """Func. q verifica se os intervalos se intersectam."""
    if intervalo1[0] <= intervalo2[0] and intervalo1[1] >= intervalo2[0]:
        return True
    if intervalo2[0] <= intervalo1[0] and intervalo2[1] >= intervalo1[0]:
        return True
    return False


def range_is_not_empty(intervalo: list) -> bool:
    """Func. q verifica se o intervalo esta vazio."""
    if intervalo[0] >= intervalo[1]:
        return False
    return True


def range_is_valid_2(intervalo1: list, intervalo2: list) -> bool:
    """Func. q verif. se os ranges das comb. de 2 intervalos estao errados."""
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
        if range_is_not_empty(intervalo1) and range_is_not_empty(intervalo2):
            #
            # e se eles nao estao dentro um do outro
            if not ranges_intersect(intervalo1, intervalo2):
                return True
            raise ValueError(
                'Os intervalos, ('
                + f'{intervalo1}-{intervalo2}), se interssectam.'
            )
        raise ValueError(
            'Os intervalos tem que ter o menor valor primeiro'
            + ' e o maior depois [menor, maior]'
        )
    raise ValueError(
        'As listas que representam os intervalos so podem ter'
        + ' dois valores: o menor e o maior valor do intervalo'
    )


def range_is_valid(intervalo):
    """Func. q verif. se os ranges das comb. de um intervalo estao errados."""
    # Verificamos se o valores da entrada eh do tipo certo
    if not isinstance(intervalo, (list, tuple)):
        raise TypeError('O intervalo so pode ser listas ou tuplas')
    #
    # Se contem apenas as extramidades dos intervalos
    if len(intervalo) == 2:
        #
        # E se nao eh um intervalo vazio
        if range_is_not_empty(intervalo):
            return True
        raise ValueError(
            'O intervalo tem que ter o menor valor primeiro'
            + ' e o maior depois [menor, maior]'
        )
    raise ValueError(
        'A lista que representa o intervalo so pode ter'
        + ' dois valores: o menor e o maior valor do intervalo'
    )
