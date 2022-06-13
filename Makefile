PYTHON = python3
DOCKER = docker
VERSION = 0.1.3


.PHONY: help bench docker shell uncache

help:     ## Print the usage
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

bench:    ## Run benchmark scripts
	$(PYTHON) main.py

docker:   ## Build image from Dockerfile
	$(DOCKER) build -t bench:$(VERSION) .
	$(DOCKER) run -dit bench:$(VERSION)

shell:    ## Activate docker environment
	docker exec -it `docker container ls --filter ancestor=bench:$(VERSION) --format "{{.ID}}"` bash

uncache:  ## Remove __pycache__ directories
	# https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
	find . -type d -name  "__pycache__" -exec rm -r {} +
