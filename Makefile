install:
	poetry install

makemigrations:
	python manage.py makemigrations users

migrate:
	python manage.py migrate

start:
	python3 manage.py runserver

local:
	poetry run django-admin makemessages --ignore="static" --ignore=".env"  -l ru

translate:
	poetry run django-admin compilemessages
