.DEFAULT_GOAL := all
isort = poetry run isort flask_valid tests
black = poetry run black flask_valid tests

.PHONY: check
check:
	poetry run flake8 flask_valid/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: lint
lint:
	$(isort)
	$(black)

.PHONY: test
test:
	poetry run coverage run -m pytest tests/

.PHONY: coverage
coverage:
	poetry run coverage report --show-missing --skip-covered --fail-under=90
	poetry run coverage xml
	poetry run coverage html

.PHONY: docs
docs:
	poetry run mkdocs build

.PHONY: build
build:
	poetry build
	poetry run mkdocs build --clean

.PHONY: publish
publish:
	poetry publish
	poetry run mkdocs gh-deploy --force