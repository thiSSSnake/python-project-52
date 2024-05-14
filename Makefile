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

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

selfcheck:
	poetry check

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

check: selfcheck test-coverage lint