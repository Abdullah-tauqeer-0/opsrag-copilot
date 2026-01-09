SHELL := /bin/bash

.PHONY: demo up down logs migrate eval

demo:
	docker compose -f infra/docker-compose.yml up -d --build
	python scripts/bootstrap_demo.py

up:
	docker compose -f infra/docker-compose.yml up -d --build

down:
	docker compose -f infra/docker-compose.yml down -v

logs:
	docker compose -f infra/docker-compose.yml logs -f

migrate:
	docker compose -f infra/docker-compose.yml exec backend alembic upgrade head

eval:
	python scripts/run_eval.py
