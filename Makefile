all: pull migrate site server

pull:
	git pull

server:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

site:
	firefox http://127.0.0.1:8000/

static:
	python3 manage.py collectstatic

app:
	python3 manage.py startapp $(name)

# Use it like make deploy msg=Made some changes
deploy:
	git pull
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py collectstatic
	git commit -m "$(msg)"
	git push

upgrade:
	pip-upgrade

update:
	pip freeze > requirements.txt