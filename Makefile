all: pull upgrade migrate site server

.PHONY: help

help: ## Provides all functions with a help string
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pull: ## Pull from github
	git pull

server: ## Runserver
	python3 manage.py runserver

migrate: ## Make model migrations
	python3 manage.py makemigrations
	python3 manage.py migrate

site: ## Opens development site on firefox
	firefox http://127.0.0.1:8000/

static: ## Put all staticfiles in staticfiles folder
	python3 manage.py collectstatic

app: ## Create new app
	python3 manage.py startapp $(name)

deploy: ## Use it as {make deploy msg="Made some changes"} to deploy to github
	git pull
	pip-upgrade
	pip freeze > requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py collectstatic
	git add .
	git commit -m "$(msg)"
	git push

upgrade: ## Upgrade all pip modules from requirements.txt
	pip-upgrade

requirements: ## Write requirements.txt
	pip freeze > requirements.txt

install: ## Install all modules from requirements.txt
	pip install pip-upgrader
	pip-upgrade

rand: ## Returns a random number
	@python -c "import random; print(random.randint(1, 100))"

time: ## Returns the current time
	@python -c "from datetime import datetime; print(datetime.now())"