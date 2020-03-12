#!/bin/sh

# Eval args

skip_build='false'

for i in "$@"
do
case $i in
    -s=*|--skip-build=*)
    skip_build="${i#*=}"
    shift
    ;;
    *)
    ;;
esac
done

# Start

products='activities survey locations'

kubectl apply -f deployment/secret.yaml

for product in $products
do
  echo "Build image: $product"
  image="kodesmil/kodesmil_$product"
  product_path="kodesmil_$product"
  deployment_path="$product_path/deployment"

  # Get timestamp for the tag
  timestamp=$(date +%Y%m%d%H%M%S)
  tag=$image:$timestamp
  latest=$image:latest

  if ! "$skip_build"
  then
    # Build image
    docker build -t "$latest" -t "$tag" "$product_path"

    # Push to dockerhub
    docker login
    docker push "$latest"

    # Remove dangling images
    docker system prune -f
  fi

  # Deploy
  kubectl delete deployment.apps/kodesmil-"${product/_/-}"
  kubectl apply -f "$deployment_path"/service.yaml
  kubectl apply -f "$deployment_path"/deployment.yaml

done

kubectl apply -f deployment/ingress.yaml