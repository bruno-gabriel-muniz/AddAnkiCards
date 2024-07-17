def reader(
    trainingData: str,
    separetorSentence: str = '|',
    separetorTranslate: str = ';',
) -> list:
    """
    Funcao que le as frases e traducoes e devolve eles separado em uma lista.
    """
    sentences = trainingData.split(separetorSentence)
    for sentenceAndTranslation in range(len(sentences)):
        sentences[sentenceAndTranslation] = sentences[
            sentenceAndTranslation
        ].split(separetorTranslate)
        removes_useless_white_space(sentences[sentenceAndTranslation])
    return sentences


def removes_useless_white_space(sentenceAndTranslation):
    """
    Funcao que remove os espacos em branco inuteis nas frases e traducoes
    """
    for sentenceOrTranslation in range(len(sentenceAndTranslation)):
        if sentenceAndTranslation[sentenceOrTranslation][0] == ' ':
            sentenceAndTranslation[
                sentenceOrTranslation
            ] = sentenceAndTranslation[sentenceOrTranslation][1:]
        if sentenceAndTranslation[sentenceOrTranslation][-1] == ' ':
            sentenceAndTranslation[
                sentenceOrTranslation
            ] = sentenceAndTranslation[sentenceOrTranslation][:-1]


'''
# leitor usado para retirar as frases do site ManyThings
def reader(Novo_Treino, separador_tra, ):
    """
    Funcao que lê o arquivo de entrada e separa cada frase e traducao em listas
    """
    # colocando todas as linhas em uma só string para separar
    # primeiramente pela traducao
    Frases_juntas = Novo_Treino
    # separando pela traducao
    Frases_separadas_tra = Frases_juntas.split(separador_tra)
    # criando a lista que vai conter as frases e as traducoes
    # em índices separados
    Frases_prontas = []
    # passando por cada frase e traducao
    for frase in Frases_separadas_tra:
        # e verificando se nao está vazia
        if frase == '' or frase == 'MP3 ':
            # caso esteja, indo para o próximo
            continue
        # e separando as linhas delas
        frase_tra_separada_lin = frase.split('\n')
        # adicionando a a segunda e terceira linha, já que a primeira está
        # somente com o separador e depois da terceira só vai ter mais
        # formas de traduzir a mesma frase, na lista que será formatada
        Frases_prontas.append(
            [frase_tra_separada_lin[1], frase_tra_separada_lin[2]]
        )
    # retornando a lista para a funcao principal
    return Frases_prontas
'''
