SHELL := /bin/bash

current_dir = $(shell pwd)

run-project:
	fastapi dev ./api/main.py

run-tests:
	pytest ./tests
