connect:
	source ./venv-dev/bin/activate
run:
	python main.py
install-dev:
	python -m venv venv-dev && source venv-dev/bin/activate && pip install -r requiriments-dev.txt
install:
	python -m venv venv && source venv/bin/activate && pip install -r requiriments.txt
format:
	@isort ./add_anki_cards/
	@isort ./tests/
	@isort main.py
	@blue ./add_anki_cards/
	@blue ./tests/
	@blue main.py
lint:
	prospector ./add_anki_cards/ --with-tool pydocstyle
lint-test:
	prospector ./tests/ --with-tool pydocstyle
testQuick:
	@pytest -v -s --cov=add_anki_cards.MathTraining --cov=add_anki_cards.PraticingEnglish --cov=add_anki_cards.ManagerUsers -m "not NotQuick"

testLessAnki:
	@pytest -v -s --cov=add_anki_cards.MathTraining --cov=add_anki_cards.PraticingEnglish --cov=add_anki_cards.ManagerUsers -m "not Anki"

test:
	@pytest -v -s --cov=add_anki_cards.MathTraining --cov=add_anki_cards.PraticingEnglish --cov=add_anki_cards.ManagerUsers
