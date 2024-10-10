.PHONY: build
build:
	uv build

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: format
format:
	uv run ruff format

.PHONY: test
test:
	uv run pytest
