TAG:=$(shell date +%y.%m.%d)
TIME:=$(shell date +%H%M%S)
PROJECT:=renameD
PROJECT_DOCKER_FILE:=$(PROJECT).Dockerfile
PROJECT_DOCKER_FILE_PRODUCTION:=$(PROJECT).prod.Dockerfile
COMMON=~/ws/common
SRC=$(pwd)../src
CACHE_ENABLED=
REPOSITORY=$(shell echo $(PROJECT):$(TAG) | tr '[:upper:]' '[:lower:]')

.PHONY: all image setup preliminary clean prod
all: setup


preliminary: $(COMMON)/entry.sh $(COMMON)/bashrc
	cp $(COMMON)/entry.sh entry.sh
	cp $(COMMON)/bashrc bashrc
	

image: $(PROJECT_DOCKER_FILE) preliminary
	docker build --tag local/$(REPOSITORY) --file $(PROJECT_DOCKER_FILE) .

setup: image
	echo "All Done"

renameD.py: $(SRC)/renameD.py
	cp  $(SRC)/renameD.py ./

prod: $(PROJECT_DOCKER_FILE_PRODUCTION) renameD.py
	docker build --tag prod/$(REPOSITORY)  --file $(PROJECT_DOCKER_FILE_PRODUCTION) .

clean:
	rm -rf entry.sh
	rm -rf bashrc
	rm -rf renameD.py
