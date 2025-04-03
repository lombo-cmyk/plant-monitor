.PHONY: compose, build, build-, build-base, start, stop, restart, logs-
compose:
	python ./build_helpers/generate_compose.py
build:
	BUILDKIT_COLORS="run=light-cyan" docker compose build

build-%:
	BUILDKIT_COLORS="run=light-cyan" docker compose build $*

build-base:
	BUILDKIT_COLORS="run=light-cyan" docker build -f base/Dockerfile -t python_base:latest .

start:
	docker compose up -d --remove-orphans

stop:
	docker compose down

restart: stop start

logs-%:
	docker logs $* -f

dev:
	./build_helpers/make-dev.sh

tests:
	./build_helpers/make-tests.sh
