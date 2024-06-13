import ReadSaveCards
import AddDBSaveCards


def mainSaveCards(newCards):
    """
    Função principal da leitura do arquivo com as frases.
    """
    # verificando se o usuário quer trocar o separador
    if input("Você deseja configurar um novo separador ou manter o padrão ─" +
             "🔊─? s─>configurar/n─>não configurar: ").lower().startswith("s"):
        # caso queira pedindo para ele digite o novo separador
        separador = input("Digite o separador: ")
    # caso ele não queira
    else:
        # colocando como padrão
        separador = "🔊"
    # variável que contem as linhas da página
    # com as frases e as traduções separadas
    lista_pag_entrada = ReadSaveCards.reader(newCards, separador)
    AddDBSaveCards.armazenaSQLite(lista_pag_entrada)
