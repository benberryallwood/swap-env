.PHONY: build
build:
	poetry build

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: format
format:
	poetry run ruff format

.PHONY: test
test:
	poetry run pytest
