.PHONY: build
build:
	poetry build

.PHONY: lint
lint:
	poetry run black src/

.PHONY: test
test:
	poetry run pytest
