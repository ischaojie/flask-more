.DEFAULT_GOAL := all
isort = hatch run isort flask_lan tests
black = hatch run black flask_lan tests

.PHONY: check
check:
	hatch run flake8 flask_lan/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: lint
lint:
	$(isort)
	$(black)

.PHONY: test
test:
	hatch run coverage run -m pytest tests/

.PHONY: coverage
coverage:
	hatch run coverage report --show-missing --skip-covered --fail-under=90
	hatch run coverage xml
	hatch run coverage html

.PHONY: docs
docs:
	hatch run mkdocs build

.PHONY: build
build:
	hatch build
	hatch run mkdocs build --clean

.PHONY: publish
publish:
	hatch publish
	hatch run mkdocs gh-deploy --force
