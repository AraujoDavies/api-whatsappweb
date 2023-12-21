.PHONY: start
start: ## cria ambiente virtual com poetry e instala bibliotecas de dev
	git init 
	poetry init -n
	poetry add --group dev blue
	poetry add --group dev isort
	poetry add --group dev pytest
	poetry add --group dev pytest-cov
	poetry add --group dev ipython
	mkdir tests
	type NUL > tests/__init__.py
	echo __pycache__/ > .gitignore
	echo pass.env >> .gitignore
	echo htmlcov/ >> .gitignore
	echo .coverage >> .gitignore
	echo .pytest_cache/ >> .gitignore
	poetry add --group doc mkdocs-material
	poetry add --group doc mkdocstrings
	poetry add --group doc mkdocstrings-python
	poetry run mkdocs new .
	mkdir code
	type NUL > code/__init__.py

.PHONY: format
format: ## formata o script e ordena os imports
	poetry run blue .
	poetry run isort .

.PHONY: git
git: ## MSG - Sobe codigo pro GIT (Necessario usar variavel)
	@make format
	@make test
	git add -A
	git commit -m "${MSG}"
	git push -u origin main

.PHONY: test
test:
	poetry run pytest . -x -s --cov=code -vv --disable-warnings
	poetry run coverage html

.PHONY: docs
docs:
	poetry run mkdocs serve

.PHONY: build
build: # make build v=1 - remember to adjust image version in compose.yml
	poetry export -o requirements.txt
	docker build -t api-whatsweb:dev .

.PHONY: dev
dev: ## Start Container em modo iterativo
	poetry run ipython -i code/main.py

# .PHONY: dev
# dev: ## Start Container em modo iterativo
# 	docker run -ti -v ${PWD}/:/app api-whatsweb:dev /bin/bash
# # pip install -r requirements.txt
# # uvicorn --app-dir /app/code main:app --host 0.0.0.0 --port 80

.PHONY: up
up: # make run-docker v=123
	docker compose up -d