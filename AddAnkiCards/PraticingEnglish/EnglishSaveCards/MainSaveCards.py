import AddDBSaveCards
import ReadSaveCards


def mainSaveCards(newCards):
    """
    Funcao principal da leitura do arquivo com as frases.
    """
    # verificando se o usuário quer trocar o separador
    if (
        input(
            'Você deseja configurar um novo separador ou manter o padrao ─'
            + '🔊─? s─>configurar/n─>nao configurar: '
        )
        .lower()
        .startswith('s')
    ):
        # caso queira pedindo para ele digite o novo separador
        separador = input('Digite o separador: ')
    # caso ele nao queira
    else:
        # colocando como padrao
        separador = '🔊'
    # variável que contem as linhas da página
    # com as frases e as traducoes separadas
    lista_pag_entrada = ReadSaveCards.reader(newCards, separador)
    AddDBSaveCards.armazenaSQLite(lista_pag_entrada)
