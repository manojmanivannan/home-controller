SHELL := /bin/bash

PULL_POLICY?=always
GENERATOR_VERSION?=v7.7.0

.PHONY: generate run

all: clean generate run

generate: home_auto/generated

home_auto/generated:
	docker run --pull $(PULL_POLICY) --rm -v $(PWD):/local -u `id -u` openapitools/openapi-generator-cli:$(GENERATOR_VERSION) generate -i /local/openapi.yaml -g python-fastapi -c /local/config.yaml -o /local/src/client

run:
	docker compose up --build -d

stop:
	docker compose down --volumes --remove-orphans

clean:
	rm -Rf src/client