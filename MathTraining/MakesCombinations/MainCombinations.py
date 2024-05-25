# importando a função que pede as informações para o usuário
from InfoCombinations import Pergunte, informe
# importando a parte do programa que encontra as possibilidades
from FindCombinations import (
    Find2CombSumMul, Find2CombSubDiv,
    FindCombSumMul, FindCombSubDiv)
# importando a parte do programa que formata, o que foi
# encontrado, para treinar no Anki
from SaveCombinations import Embaralhe, Distribua, Armazene


def main_combinador():
    """
    Função Principal do Algorito:
    - Pede as informações sobre as combinações;
    - Encontra todas possibilidades; e
    - Armazena elas em quantos arquivos a pessoa quiser
      de maneira alteatória ou não
    """
    # pedindo as informações sobre a combinação
    (quant_cards_por_d, são_dois_intervalos,
     intervalo, num_max_cards, operação) = Pergunte()
    # verificando se o usuário escolheu dois intervalos ou somente 1
    if são_dois_intervalos:
        # caso tenha escolhido 2 verificando se escolheu
        # subtração ou divisão
        if operação == "sub" or operação == "div":
            # realizando a função deste caso
            combinações = Find2CombSubDiv(
                intervalo[0], intervalo[1])
        # caso não tenha escolhido sabemos que foi soma ou multiplicação
        else:
            # portanto aplicamos a função correta para este caso
            combinações = Find2CombSumMul(
                intervalo[0], intervalo[1])
    # caso ele só tenha escolhido 1
    else:
        # verificando se o usuário escolheu subtração ou divisão
        if operação == "sub" or operação == "div":
            # criando todas as combinações possíveis
            combinações = FindCombSubDiv(intervalo)
        # caso não tenha escolhidoi rodando o programa
        # de adição e multiplicação
        else:
            # criando todas as combinações possíveis
            combinações = FindCombSumMul(intervalo)
    # embaralhando elas
    combinações_embaralhada = Embaralhe(combinações)
    # distriubuindo nas listas
    combinações_distribuidas = Distribua(
        combinações_embaralhada, quant_cards_por_d, num_max_cards)
    # armazenando elas no arquivo
    informações_do_resultado = Armazene(
        combinações_distribuidas, operação, são_dois_intervalos, intervalo)
    # informando a condição final do produto
    informe(informações_do_resultado)


main_combinador()
