install: ## Install requirements
	pip install -r requirements.txt

fmt format: ## Run code formatters
	isort app tests
	black app tests

lint: ## Run code linters
	isort --check app tests
	black --check app tests
	flake8 app tests
	mypy app tests