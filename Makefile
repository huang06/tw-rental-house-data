SHELL=/bin/bash

.PHONY: all
all:

.PHONY: python
python:
	python3 -m pip install -U pipenv
	PIPENV_VENV_IN_PROJECT=1 python3 -m pipenv sync --dev -v

.PHONY: db
db:
	cd backend && docker compose up -d
	echo -e "See db status with 'docker compose logs -f'"

.PHONY: migrate
migrate:
	source .venv/bin/activate && cd backend && python3 manage.py migrate && python3 manage.py loaddata vendors

.PHONY: crawl
crawl:
	cd crawler && ./go.sh
