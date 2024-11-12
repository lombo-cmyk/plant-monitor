.PHONY: start, build, stop
build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down

restart: stop start

build-base:
	docker build -f base/Dockerfile -t python_base:latest .
