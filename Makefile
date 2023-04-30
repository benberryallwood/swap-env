.PHONY: build
build:
	poetry build

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: format
format:
	poetry run black .

.PHONY: test
test:
	poetry run pytest
