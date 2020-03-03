#!/bin/sh

image="kodesmil/kodesmil_activities"
deployment_path="deployment/kodesmil-activities"



# Deploy
kubectl apply -f $deployment_path-service.yaml
kubectl apply -f $deployment_path-load-balancer.yaml
kubectl apply -f $deployment_path-deployment.yaml