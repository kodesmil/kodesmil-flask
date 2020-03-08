#!/bin/sh

products='activities health_survey'

kubectl apply -f deployment/secret.yaml

for product in $products
do
  image="kodesmil/kodesmil_$product"
  product_path="kodesmil_$product"
  deployment_path="$product_path/deployment"

  # Get timestamp for the tag
  timestamp=$(date +%Y%m%d%H%M%S)
  tag=$image:$timestamp
  latest=$image:latest

  # Build image
  docker build -t $latest -t $tag $product_path

  # Push to dockerhub
  docker login
  docker push $latest

  # Remove dangling images
  docker system prune -f

  # Deploy
  kubectl delete deployment.apps/kodesmil-${product/_/-}
  kubectl apply -f $deployment_path/service.yaml
  kubectl apply -f $deployment_path/load-balancer.yaml
  kubectl apply -f $deployment_path/deployment.yaml
done