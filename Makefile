.PHONY: install-dev lint test validate-dev deploy-dev deploy-test deploy-prod

install-dev:
	pip install -r requirements-dev.txt

lint:
	ruff check .
	black --check .
	yamllint .

test:
	pytest

validate-dev:
	databricks bundle validate -t dev

deploy-dev:
	databricks bundle deploy -t dev

deploy-test:
	databricks bundle deploy -t test

deploy-prod:
	databricks bundle deploy -t prod
