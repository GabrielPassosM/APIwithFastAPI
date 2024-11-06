SHELL := /bin/bash

current_dir = $(shell pwd)

services-up:
	docker compose -f infra/compose.yaml up -d

services-down:
	docker compose -f infra/compose.yaml down

services-stop:
	docker compose -f infra/compose.yaml stop

services-logs:
	docker compose -f infra/compose.yaml logs -f

run-project: services-up
	fastapi dev ./api/main.py

run-tests:
	pytest ./tests
