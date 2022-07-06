PYTHON = pdm run python3
DOCKER = docker
VERSION = 0.1.5


.PHONY: help bench plot error docker shell clean collect uncache

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
	@echo "cd ~/burger.bench && time make bench"
	ID=$$(docker container ls --filter ancestor=bench:$(VERSION) --format "{{.ID}}"); \
	docker exec -it $$ID bash

clean:    ## Remove container and image
	ID=$$(docker container ls --filter ancestor=bench:$(VERSION) --format "{{.ID}}"); \
	docker container stop $$ID
	docker container prune --force
	ID=$$(docker images bench:$(VERSION) --format "{{.ID}}"); \
	docker image rm $$ID

collect:  ## Collect benchmark data
	ID=$$(docker container ls --filter ancestor=bench:$(VERSION) --format "{{.ID}}"); \
	docker cp $$ID:/root/burger.bench/static/data/bench.json .

uncache:  ## Remove __pycache__ directories
	# https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files
	find . -type d -name  "__pycache__" -exec rm -r {} +
