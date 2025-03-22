.PHONY: start, build, build-, build-base stop
compose:
	python ./build_helpers/generate_compose.py
build:
	BUILDKIT_COLORS="run=light-cyan" docker compose build

build-%:
	BUILDKIT_COLORS="run=light-cyan" docker compose build $*

build-base:
	BUILDKIT_COLORS="run=light-cyan" docker build -f base/Dockerfile -t python_base:latest .

start:
	docker compose up -d

stop:
	docker compose down

restart: stop start
