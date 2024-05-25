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


mainSaveCards('''MP3 🔊  TTS  English
Tom sent Mary a postcard. (CK)
Tom enviou um cartão postal a Mary. (ajdavidl)
MP3 🔊  TTS  English
Tom sent Mary some money. (CK)
Tom enviou dinheiro para Mary. (Ricardo14)
MP3 🔊  TTS  English
Tom sent a video to Mary. (CK)
Tom enviou um vídeo para Mary. (carlosalberto)
Tom enviou um vídeo a Mary. (carlosalberto)
MP3 🔊  TTS  English
Tom sharpened the knives. (CK)
Tom amolou as facas. (bill)
MP3 🔊  TTS  English
Tom should be in the lab. (Eccles17)
Tom deveria estar no laboratório. (Mecamute)
MP3 🔊  TTS  English
Tom should blame himself. (CK)
Tom deveria se envergonhar. (ToinhoAlam)
MP3 🔊  TTS  English
Tom should do that today. (CK)
O Tom não deveria fazer isso hoje. (Wagner1994)
MP3 🔊  TTS  English
Tom should eat breakfast. (CK)
Tom deveria tomar café da manhã. (bill)
MP3 🔊  TTS  English
Tom should eat something. (CK)
Tom deveria comer alguma coisa. (bill)
MP3 🔊  TTS  English
Tom should go to the gym. (CK)
Tom deveria ir à academia. (alexmarcelo)
MP3 🔊  TTS  English
Tom should help us today. (CK)
Tom deveria nos ajudar hoje. (Ricardo14)
MP3 🔊  TTS  English
Tom should've been first. (CK)
Tom deveria ter sido o primeiro. (Ricardo14)
MP3 🔊  TTS  English
Tom should've bought one. (CK)
Tom deveria ter comprado um. (bill)
Tom deveria ter comprado uma. (bill)
MP3 🔊  TTS  English
Tom should've trusted me. (CK)
Tom deveria ter confiado em mim. (bill)
MP3 🔊  TTS  English
Tom showed me the letter. (CK)
Tom me mostrou a carta. (bill)
MP3 🔊  TTS  English
Tom signed the documents. (CK)
Tom assinou os documentos. (bill)
MP3 🔊  TTS  English
Tom sings better than me. (supercoolbeas30)
Tom canta melhor que eu. (Ricardo14)
MP3 🔊  TTS  English
Tom slept during the day. (CK)
Tom dormiu durante o dia. (bill)
MP3 🔊  TTS  English
Tom slept for three days. (CK)
Tom dormiu por três dias. (bill)
MP3 🔊  TTS  English
Tom smiled halfheartedly. (CM)
Tom sorriu desentusiasmado. (Ricardo14)
MP3 🔊  TTS  English
Tom snuck into the party. (Hybrid)
Tom entrou sorrateiramente na festa. (Ricardo14)
MP3 🔊  TTS  English
Tom sold his car to Mary. (CK)
Tom vendeu o seu carro à Maria. (bill)
MP3 🔊  TTS  English
Tom spent time with Mary. (CK)
Tom passou um tempo com Maria. (bufo)
MP3 🔊  TTS  English
Tom spoiled all my plans. (sharptoothed)
Tom estragou todos os meus planos. (bill)
MP3 🔊  TTS  English
Tom spoiled his children. (CK)
Tom mimava os filhos. (bill)
MP3 🔊  TTS  English
Tom spoke highly of Mary. (CK)
Tom falou muito bem de Maria. (bill)
MP3 🔊  TTS  English
Tom squeezed Mary's hand. (CK)
Tom apertou a mão de Maria. (bill)
MP3 🔊  TTS  English
Tom squeezed the oranges. (CK)
Tom espremeu as laranjas. (bill)
MP3 🔊  TTS  English
Tom started to get angry. (CK)
Tom começou a ficar bravo. (alexmarcelo)
MP3 🔊  TTS  English
Tom started to walk away. (CK)
Tom começou a ir embora. (Ricardo14)
MP3 🔊  TTS  English
Tom stayed at his aunt's. (CK)
Tom ficou na casa da tia. (bill)
MP3 🔊  TTS  English
Tom stepped on the brake. (CK)
Tom pisou no freio. (bill)
MP3 🔊  TTS  English
Tom stepped on the scale. (Hybrid)
O Tom pisou na balança. (Ricardo14)
MP3 🔊  TTS  English
Tom still has to do that. (CK)
Tom continua tendo que fazer isso. (Wagner1994)
MP3 🔊  TTS  English
Tom still hasn't arrived. (CK)
Tom ainda não chegou. (bill)
MP3 🔊  TTS  English
Tom still studies French. (CK)
Tom ainda estuda francês. (bill)
MP3 🔊  TTS  English
Tom still teaches French. (CK)
Tom ainda ensina francês. (bill)
MP3 🔊  TTS  English
Tom stood up and clapped. (CM)
Tom levantou-se e aplaudiu. (bill)
''')
