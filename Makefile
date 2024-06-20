format:
	@isort ./AddAnkiCards/
	@isort ./tests/
	@blue ./AddAnkiCards/
	@blue ./tests/
lint:
	@blue ./AddAnkiCards/ --check
	@blue ./tests/ --check
testQuick:
	@pytest -v -s -m "not NotQuick"

testLessAnki:
	@pytest -v -s -m "not Anki"

testAll:
	@pytest -v -s