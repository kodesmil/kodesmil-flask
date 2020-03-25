# KodeSmil Microservices

## Installation

1. Create `deployments/secret.yaml` file ()
    
    ```
    apiVersion: v1
    kind: Secret
    metadata:
    name: kodesmil-secret
    type: Opaque
    data:
    MONGODB_PASSWORD: <PROVIDE>
    MONGODB_USERNAME: <PROVIDE>
    MONGODB_HOSTNAME: <PROVIDE>
    AUTH0_DOMAIN: <PROVIDE>
    API_IDENTIFIER: <PROVIDE>
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
2. Start development with `skaffold dev -n local`