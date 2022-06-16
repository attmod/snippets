#!/bin/bash
KAFKA_IP=$(shell minikube ip)
export KAFKA_IP
KAFKA_PORT=$(shell kubectl get service my-cluster-kafka-external-bootstrap -n kafka -o=jsonpath='{.spec.ports[0].nodePort}{"\n"}')
export KAFKA_PORT
