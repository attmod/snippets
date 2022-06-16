#!/bin/bash
kubectl port-forward --namespace default svc/redis1-master 6379:6379