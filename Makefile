SHELL := /bin/bash


.PHONY: stop run

all: stop run


run:
	docker compose up --build -d

stop:
	docker compose down --volumes --remove-orphans

clean:
	rm -Rf src/client