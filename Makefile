.DEFAULT_GOAL := all
isort = isort flask_valid tests
black = black flask_valid tests

.PHONY: check
check:
	flake8 flask_valid/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: lint
lint:
	$(isort)
	$(black)

.PHONY: test
test:
	coverage run -m pytest tests/

.PHONY: coverage
coverage:
	coverage report --show-missing --skip-covered --fail-under=90
	coverage xml
	coverage html

.PHONY: publish
publish:
	poetry publish --build