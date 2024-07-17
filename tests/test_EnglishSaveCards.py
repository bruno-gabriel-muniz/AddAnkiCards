from AddAnkiCards.Db.DbConnect import DbConnect
from AddAnkiCards.PraticingEnglish.EnglishSaveCards import (AddDBSaveCards,
                                                            ReadSaveCards)

exemplo1 = (
    'While her poetic talent shines, she overlooks the joy and hope ' +
    'baking can bring.;Embora seu talento poético brilhe, ela ignora a ' +
    'alegria e a esperança que o ato de assar pode trazer.|Baking a ' +
    'birthday cake can evoke childhood memories and raise spirits.;' +
    'Assar um bolo de aniversário pode evocar memórias de infância e ' +
    'elevar os ânimos.|The act of baking can create unexpected ' +
    'delights from simple ingredients.;O ato de assar pode criar ' +
    'delícias inesperadas a partir de ingredientes simples.'
)
exemplo2 = (
    'While her poetic talent shines, she overlooks the joy and hope ' +
    'baking can bring. ; Embora seu talento poético brilhe, ela ignora a ' +
    'alegria e a esperança que o ato de assar pode trazer. | Baking a ' +
    'birthday cake can evoke childhood memories and raise spirits. ; ' +
    'Assar um bolo de aniversário pode evocar memórias de infância e ' +
    'elevar os ânimos. | The act of baking can create unexpected ' +
    'delights from simple ingredients. ; O ato de assar pode criar ' +
    'delícias inesperadas a partir de ingredientes simples.'
)


def test_basic_read_cards():
    global exemplo1
    print()
    result_espec = [['While her poetic talent shines, she overlooks the ' +
                     'joy and hope baking can bring.',
                     'Embora seu talento poético brilhe, ela ignora a ' +
                     'alegria e a esperança que o ato de assar pode trazer.'],
                    ['Baking a birthday cake can evoke childhood memories' +
                     ' and raise spirits.',
                     'Assar um bolo de aniversário pode evocar memórias de' +
                     ' infância e elevar os ânimos.'],
                    ['The act of baking can create unexpected delights' +
                     ' from simple ingredients.',
                     'O ato de assar pode criar delícias inesperadas a ' +
                     'partir de ingredientes simples.']]

    assert ReadSaveCards.reader(exemplo1) == result_espec
    print()


def test_read_cards_whit_whitespace():
    global exemplo2
    print()
    result_espec = [['While her poetic talent shines, she overlooks the ' +
                     'joy and hope baking can bring.',
                     'Embora seu talento poético brilhe, ela ignora a ' +
                     'alegria e a esperança que o ato de assar pode trazer.'],
                    ['Baking a birthday cake can evoke childhood memories' +
                     ' and raise spirits.',
                     'Assar um bolo de aniversário pode evocar memórias de' +
                     ' infância e elevar os ânimos.'],
                    ['The act of baking can create unexpected delights' +
                     ' from simple ingredients.',
                     'O ato de assar pode criar delícias inesperadas a ' +
                     'partir de ingredientes simples.']]
    assert ReadSaveCards.reader(exemplo2) == result_espec
    print()


def test_simple_save_cards():
    global exemplo1
    print()
    DbTest = DbConnect('DbTest.db')
    AddDBSaveCards.armazenaSQLite(ReadSaveCards.reader(exemplo1), DbTest)
    # reabrindo o banco de dados pois ele eh fechado na funcao a cima
    DbTest = DbConnect('DbTest.db')
    assert (
        DbTest.cursor().execute('SELECT * FROM FrasesNaoUsadas').fetchall()
    ) == [
        (
            1,
            'While her poetic talent shines, she overlooks the joy and ' +
            'hope baking can bring.',
            'Embora seu talento poético brilhe, ela ignora a alegria e a ' +
            'esperança que o ato de assar pode trazer.', 'english'
        ),
        (
            2,
            'Baking a birthday cake can evoke childhood memories and raise ' +
            'spirits.',
            'Assar um bolo de aniversário pode evocar memórias de infância ' +
            'e elevar os ânimos.',
            'english'
        ),
        (
            3,
            'The act of baking can create unexpected delights from simple ' +
            'ingredients.',
            'O ato de assar pode criar delícias inesperadas a partir de ' +
            'ingredientes simples.',
            'english'
        )
    ]
    DbTest.execute('DROP TABLE FrasesNaoUsadas')
    DbTest.close()
    print()
