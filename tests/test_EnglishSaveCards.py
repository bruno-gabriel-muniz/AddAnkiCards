from add_anki_cards.Db.DbConnect import db_connect
from add_anki_cards.PraticingEnglish.EnglishSaveCards import (AddDBSaveCards,
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
    db_test = db_connect('DbTest.db', 'Test')
    AddDBSaveCards.armazena_sqlite(ReadSaveCards.reader(exemplo1), db_test)
    # reabrindo o banco de dados pois ele eh fechado na funcao a cima
    db_test = db_connect('DbTest.db', 'Test')
    assert (
        db_test.cursor().execute('SELECT * FROM FrasesNaoUsadas').fetchall()
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
    db_test.execute('DROP TABLE FrasesNaoUsadas')
    db_test.close()
    print()
