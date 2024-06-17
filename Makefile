format:
	@isort ./AddAnkiCards/
	@isort ./tests/
	@blue ./AddAnkiCards/
	@blue ./tests/
lint:
	@blue ./AddAnkiCards/ --check
	@blue ./tests/ --check
test:
	@pytest -v
