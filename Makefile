connect:
	source ./venv-dev/bin/activate
run:
	python main.py
install-dev:
	python -m venv venv-dev && source venv-dev/bin/activate && pip install -r requiriments-dev.txt
install:
	python -m venv venv && source venv/bin/activate && pip install -r requiriments.txt
format:
	@isort main.py
	@isort ./add_anki_cards/
	@blue main.py
	@blue ./add_anki_cards/
formatT:
	@isort ./tests/
	@blue ./tests/
lint:
	prospector ./add_anki_cards/ --with-tool pydocstyle
lint-test:
	prospector ./tests/ --with-tool pydocstyle
testQuick:
	@pytest -v -s --cov=add_anki_cards.models --benchmark-columns=mean -m "not NotQuick"

testLessAnki:
	@pytest -v -s --cov=add_anki_cards.models --benchmark-columns=mean -m "not Anki"

test:
	@pytest -v -s --cov=add_anki_cards.models --benchmark-columns=mean

testb:
	@pytest -v -s --cov=add_anki_cards.models --benchmark-columns=mean --benchmark-only
