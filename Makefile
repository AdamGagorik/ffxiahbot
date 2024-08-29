.PHONY: install
install: ## Install the environment and the pre-commit hooks
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@uv lock
	@uv run pre-commit run -a
	@uv run deptry .

.PHONY: test
mypy: ## Run mypy
	@uv run mypy

.PHONY: test
test: ## Test the code with pytest
	@uv run pytest --cov --cov-config=pyproject.toml --cov-report=xml --junitxml=junit.xml

.PHONY: build
build: clean-build ## Build wheel file
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: publish
publish: ## publish a release to pypi.
	@uvx twine upload dist/*

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
