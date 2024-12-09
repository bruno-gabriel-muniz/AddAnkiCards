def reader(
    training_data: str,
    separetor_sentence: str = '|',
    separetor_translate: str = ';',
) -> list:
    """
    Funcao que le as frases e traducoes e devolve eles separado em uma lista.
    """
    sentences = training_data.split(separetor_sentence)
    for idx, sentence_and_translation in enumerate(sentences):
        sentences[idx] = sentence_and_translation.split(separetor_translate)
        sentences[idx][0] = removes_useless_white_space(sentences[idx][0])
        sentences[idx][1] = removes_useless_white_space(sentences[idx][1])
    return sentences


def removes_useless_white_space(sentence_and_translation: str) -> str:
    """Func. q remove os espaços em branco inuteis nas frases e traducoes."""
    if sentence_and_translation[0] == ' ':
        sentence_and_translation = sentence_and_translation[1:]
    if sentence_and_translation[-1] == ' ':
        sentence_and_translation = sentence_and_translation[:-1]
    return sentence_and_translation
