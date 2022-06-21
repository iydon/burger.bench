PYTHON = pdm run python3
DOCKER = docker
VERSION = 0.1.3


.PHONY: help bench plot error docker shell collect uncache

help:     ## Print the usage
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

bench:    ## Run benchmark script in docker
	python3 script/$@.py

plot:     ## Plot benchmark results
	$(PYTHON) script/plot.py

error:    ## Run script that compares the results
	$(PYTHON) script/$@.py

docker:   ## Build image from Dockerfile
	$(DOCKER) build -t bench:$(VERSION) .
	$(DOCKER) run -dit bench:$(VERSION)

shell:    ## Activate docker environment
	docker exec -it `docker container ls --filter ancestor=bench:$(VERSION) --format "{{.ID}}"` bash

collect:  ## Collect benchmark data
	docker cp `docker container ls --filter ancestor=bench:$(VERSION) --format "{{.ID}}"`:/root/burger.bench/bench.json .

uncache:  ## Remove __pycache__ directories
	# https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
	find . -type d -name  "__pycache__" -exec rm -r {} +
