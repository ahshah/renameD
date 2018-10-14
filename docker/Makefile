TAG:=$(shell date +%y.%m.%d)
PROJECT:=renamed
PROJECT_DOCKER_FILE:=$(PROJECT).Dockerfile
COMMON=~/ws/common
CACHE_ENABLED=

.PHONY: all image setup preliminary clean
all: setup


preliminary: $(COMMON)/entry.sh $(COMMON)/bashrc
	cp $(COMMON)/entry.sh entry.sh
	cp $(COMMON)/bashrc bashrc
	

image: $(PROJECT_DOCKER_FILE) preliminary
	docker build --tag local/$(PROJECT):$(TAG) --file $(PROJECT_DOCKER_FILE) .

setup: image
	echo "All Done"

clean:
	rm -rf entry.sh
	rm -rf bashrc

