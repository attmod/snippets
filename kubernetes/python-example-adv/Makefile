#
#
#
#

# added in case the docker image needs to match uid
# also usage in docker-compose
LOCAL_USER_ID := $(shell id -u)
export LOCAL_USER_ID

# Kafka detection should only be used if kubernetes is found running
# and kubectl get pods -A shows kafka
#include ../expose_kafka.sh

# project name, source image, all user-editable options:
include .env

DOCKER_IMAGE := ${PROJECT_NAME}:latest
export DOCKER_IMAGE

DOCKER_DEPLOYMENT_IMAGE := ${PROJECT_NAME}-deployment:latest
export DOCKER_DEPLOYMENT_IMAGE

MINIKUBE_ENV := $(shell docker container ls | grep -c k8s-minikube)

CONTAINER_NAME := ${PROJECT_NAME}
export CONTAINER_NAME

build:
	docker build -t ${DOCKER_IMAGE} \
			--build-arg DOCKER_SRC=${DOCKER_SRC} \
			--build-arg LOCAL_USER_ID=${LOCAL_USER_ID} .
	
run:
	docker-compose up --remove-orphans

detach:
	docker-compose up -d --remove-orphans

stop:
	docker-compose down


build_deploy:
	docker build -t ${DOCKER_DEPLOYMENT_IMAGE} \
	        --no-cache \
			--build-arg DOCKER_IMAGE=${DOCKER_IMAGE} \
			--build-arg LOCAL_USER_ID=${LOCAL_USER_ID} \
			-f Dockerfile.deployment .


deploy:
ifeq ($(MINIKUBE_ENV),0)
	@echo no minikube, proceeding with default registry
	docker build -t ${DOCKER_DEPLOYMENT_IMAGE} \
	        --no-cache \
			--build-arg DOCKER_IMAGE=${DOCKER_IMAGE} \
			--build-arg LOCAL_USER_ID=${LOCAL_USER_ID} \
			-f Dockerfile.deployment .
else
	@echo outside minikube, launching eval to get inside container

	@eval $$(minikube docker-env) ;\
	docker build -t ${DOCKER_IMAGE} \
			--build-arg DOCKER_SRC=${DOCKER_SRC} \
			--build-arg LOCAL_USER_ID=${LOCAL_USER_ID} .

	@eval $$(minikube docker-env) ;\
	docker build -t ${DOCKER_DEPLOYMENT_IMAGE} \
	        --no-cache \
			--build-arg DOCKER_IMAGE=${DOCKER_IMAGE} \
			--build-arg LOCAL_USER_ID=${LOCAL_USER_ID} \
			-f Dockerfile.deployment .
endif
	envsubst < deployment.yaml | kubectl apply -f -

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
	@echo "  Kafka IP:     ${KAFKA_IP}"
	@echo "  Kafka port:   ${KAFKA_PORT}"
	@echo ""
