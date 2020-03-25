# KodeSmil Microservices

## Installation (for local)

1. Create `deployments/namespace_local/secret.yaml` file ()
    
    ```
    apiVersion: v1
    kind: Secret
    metadata:
    name: kodesmil-secret
    type: Opaque
    data:
        mongodb.password: <PROVIDE>
        mongodb.username: <PROVIDE>
        mongodb.hostname: <PROVIDE>
        auth0.domain: <PROVIDE>
        auth0.api_identifier: <PROVIDE>
    ```

2. Install [Docker](https://www.docker.com/products/docker-desktop)
3. Install [Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
4. Install [Skaffold](https://skaffold.dev/docs/install/)
5. Start your cluster with `minikube start`
5. Add entries to your `/etc/hosts`

```
192.168.64.4    local-points.api.kodesmil.com
192.168.64.4    local-products.api.kodesmil.com
192.168.64.4    local-survey.api.kodesmil.com
192.168.64.4    local-activities.api.kodesmil.com
192.168.64.4    local-locations.api.kodesmil.com
```

where 192.168.64.4 is output of `minikube ip`

## Run

1. Start minikube cluster locally
2. Start development with 
`skaffold run -f skaffold.local.yaml -n local`
or if you want to prune images
`skaffold run -f skaffold.local.yaml -n local --no-prune=false --cache-artifacts=false`