#!/bin/sh

product="activities"
image="kodesmil/kodesmil_$product"
deployment_path="deployment/kodesmil-$product"

# Get timestamp for the tag
timestamp=$(date +%Y%m%d%H%M%S)
tag=$image:$timestamp
latest=$image:latest

# Build image
docker build -t $latest -t $tag .

# Push to dockerhub
docker login
docker push $latest

# Remove dangling images
docker system prune -f

# Deploy
kubectl delete deployment.apps/kodesmil-$product
kubectl apply -f $deployment_path-service.yaml
kubectl apply -f $deployment_path-load-balancer.yaml
kubectl apply -f $deployment_path-deployment.yaml