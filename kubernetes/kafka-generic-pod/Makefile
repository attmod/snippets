LOCAL_USER_ID := $(shell id -u)
export LOCAL_USER_ID

include ../expose_kafka.sh
include .env

DOCKER_IMAGE := ${PROJECT_NAME}:latest
export DOCKER_IMAGE

build:
	docker build -t ${DOCKER_IMAGE} \
			--build-arg DOCKER_SRC=${DOCKER_SRC} \
			--build-arg LOCAL_USER_ID=${LOCAL_USER_ID} .
	
run:
	docker-compose up -d --remove-orphans

stop:
	docker-compose down
	
test:
	@echo ""
	@echo "  $(shell whereis docker)":
	@echo "  $(shell whereis docker-compose)"
	@echo ""
	@echo "  Current directory is   ${PWD}"
	@echo "  Base docker image is   ${DOCKER_SRC}"
	@echo "  Project name will be   ${PROJECT_NAME}"
	@echo "  Docker image will be   ${DOCKER_IMAGE}"
	@echo ""
