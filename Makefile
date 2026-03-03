.PHONY: download-models build up down logs test lint dev

download-models:
	bash scripts/download_models.sh

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test:
	docker compose --profile test run --rm test

lint:
	docker compose --profile test run --rm test python -m ruff check app/ tests/
