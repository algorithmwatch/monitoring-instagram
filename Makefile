BACKEND_URL_ENV=https://monitoring-ig.herokuapp.com
BACKEND_MANAGE=cd backend && pipenv run ./manage.py
BACKEND_DOCKERCOMPOSE=cd backend && docker-compose
WEB_EXT_YARN=cd web-ext && yarn


installbackend:
	cd backend && pipenv sync

runbackend: startdockerservices
	$(BACKEND_MANAGE) runserver

startdockerservices:
	$(BACKEND_DOCKERCOMPOSE) up -d

stopdockerservices:
	$(BACKEND_DOCKERCOMPOSE) down

migrate:
	$(BACKEND_MANAGE) migrate

makemigrations:
	$(BACKEND_MANAGE) makemigrations

createsuperuser:
	$(BACKEND_MANAGE) createsuperuser

shell:
	$(BACKEND_MANAGE) shell

installwebext:
	$(WEB_EXT_YARN) install

runwebext: export TARGET=firefox-desktop
runwebext:
	$(WEB_EXT_YARN) start

runwebextchrome: export TARGET=chromium
runwebextchrome:
	$(WEB_EXT_YARN) start

build_webext: export BACKEND_URL=$(BACKEND_URL_ENV)
build_webext:
	$(WEB_EXT_YARN) build

format:
	$(WEB_EXT_YARN) format
	cd backend && pipenv run yapf -rip --verbose ./
	$(WEB_EXT_YARN) eslint ./src

load_db:
	cd backend/ && curl `heroku pg:backups:url -r heroku` --output - |  docker-compose exec -T db pg_restore -U postgres -d postgres --no-owner --no-privileges --clean
	$(BACKEND_MANAGE) migrate
