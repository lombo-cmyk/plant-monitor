.PHONY: start, build
start:
	docker compose up -d

build:
	docker compose build