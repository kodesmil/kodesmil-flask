# KodeSmil Universe

## KodeSmil Microservices

### Installation (for local)

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
    ```

2. Install [Docker](https://www.docker.com/products/docker-desktop)
3. Install [Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
4. Install [Skaffold](https://skaffold.dev/docs/install/)
5. Start your cluster with `minikube start`
5. Add entries to your `/etc/hosts`

```
192.168.64.4    points.local.api.kodesmil.com
192.168.64.4    products.local.api.kodesmil.com
192.168.64.4    survey.local.api.kodesmil.com
192.168.64.4    activities.local.api.kodesmil.com
192.168.64.4    locations.local.api.kodesmil.com
```

where 192.168.64.4 is output of `minikube ip`

### Run

1. Start minikube cluster locally
2. Start local dev with 
`skaffold run -f deployment/skaffold.local.yaml -n local`

### Dev & Production Servers

1. Install cert-manager Helm
2. Create certificate Issuer
`kubectl apply -f deploment/issuer.yaml`