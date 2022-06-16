# Small test container

The container itself hosts a simple Python Flask application, please visit the container's website on port 8910 to learn more, or, if running on minikube, check the service port and go through that.

# Building a docker image and kubernetes deployment

.env file first:
- project name is automatic, based on the directory name
- DOCKER_SRC is the base image for Dockerfile

Docker image by default is the project name, with :latest

This image will dynamically mount current dir as /workdir and use init.sh


## build

    make build

Builds docker image using Dockerfile

Does NOT copy any files over to the image

## run

    make run

Uses Docker Compose, mounts ./ as /workdir

## build_deploy

    make build_deploy

Test-builds a deployment image using Dockerfile.deployment, still local

Will pack all files in ./ into the image in /workdir

## deploy

    make deploy

Uses docker registry from minikube (if minikube container was detected)

Builds first docker image using Dockerfile  (cached, so you can even move the image manually if you want)

Builds second docker using Dockerfile.deployment, with --no-cache, copies all files from ./ into /workdir

Starts a kubectl deployment with deployment.yaml - but substitutes every shell variable inside using envsubst

## test

    make test

Checks what is the current state of the system (unfinished)