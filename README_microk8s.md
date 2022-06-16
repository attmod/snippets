# Installation
    snap search microk8s
    snap install microk8s --classic

    microk8s status
    microk8s enable dashboard dns helm3 gpu portainer registry

Docker image registry will be available at localhost:32000

Portainer requires:
    dns
    ha-cluster
    ingress
    metrics-server
    rbac
    storage
So:

    microk8s enable dns ha-cluster ingress metrics-server rbac storage

Portainer is at localhost:30777

Create a user admin with some password

My addons after that are:
```
alice@rabbithole:~$ microk8s status
microk8s is running
high-availability: no
  datastore master nodes: 127.0.0.1:19001
  datastore standby nodes: none
addons:
  enabled:
    dashboard            # The Kubernetes dashboard
    dns                  # CoreDNS
    gpu                  # Automatic enablement of Nvidia CUDA
    ha-cluster           # Configure high availability on the current node
    helm3                # Helm 3 - Kubernetes package manager
    ingress              # Ingress controller for external access
    metrics-server       # K8s Metrics Server for API access to service metrics
    portainer            # Portainer UI for your Kubernetes cluster
    rbac                 # Role-Based Access Control for authorisation
    registry             # Private image registry exposed on localhost:32000
    storage              # Storage class; allocates storage from host directory
  disabled:
    ambassador           # Ambassador API Gateway and Ingress
    cilium               # SDN, fast with full network policy
    dashboard-ingress    # Ingress definition for Kubernetes dashboard
    fluentd              # Elasticsearch-Fluentd-Kibana logging and monitoring
    helm                 # Helm 2 - the package manager for Kubernetes
    host-access          # Allow Pods connecting to Host services smoothly
    inaccel              # Simplifying FPGA management in Kubernetes
    istio                # Core Istio service mesh services
    jaeger               # Kubernetes Jaeger operator with its simple config
    kata                 # Kata Containers is a secure runtime with lightweight VMS
    keda                 # Kubernetes-based Event Driven Autoscaling
    knative              # The Knative framework on Kubernetes.
    kubeflow             # Kubeflow for easy ML deployments
    linkerd              # Linkerd is a service mesh for Kubernetes and other frameworks
    metallb              # Loadbalancer for your Kubernetes cluster
    multus               # Multus CNI enables attaching multiple network interfaces to pods
    openebs              # OpenEBS is the open-source storage solution for Kubernetes
    openfaas             # OpenFaaS serverless framework
    prometheus           # Prometheus operator for monitoring and logging
    traefik              # traefik Ingress controller for external access
```

Kubectl get pods -A:
```
alice@rabbithole:~$ microk8s.kubectl get pods -A
NAMESPACE                NAME                                                          READY   STATUS      RESTARTS      AGE
default                  gpu-operator-node-feature-discovery-worker-5br68              1/1     Running     0             7m37s
default                  gpu-operator-node-feature-discovery-master-5f6fb954cf-vb2sb   1/1     Running     0             7m37s
kube-system              kubernetes-dashboard-585bdb5648-4d6zw                         1/1     Running     0             7m37s
kube-system              hostpath-provisioner-7764447d7c-ctzc2                         1/1     Running     0             7m37s
kube-system              dashboard-metrics-scraper-69d9497b54-tf6jl                    1/1     Running     0             7m37s
container-registry       registry-5f697bb7df-tmwdz                                     1/1     Running     0             7m37s
gpu-operator-resources   nvidia-container-toolkit-daemonset-7brkj                      1/1     Running     0             6m51s
gpu-operator-resources   nvidia-cuda-validator-gcrhr                                   0/1     Completed   0             6m11s
gpu-operator-resources   nvidia-dcgm-j57z2                                             1/1     Running     0             6m51s
gpu-operator-resources   nvidia-device-plugin-daemonset-dsj8d                          1/1     Running     0             6m51s
gpu-operator-resources   nvidia-device-plugin-validator-xzphx                          0/1     Completed   0             5m15s
gpu-operator-resources   nvidia-operator-validator-4snlk                               1/1     Running     0             6m51s
gpu-operator-resources   nvidia-dcgm-exporter-2zqhm                                    1/1     Running     0             6m51s
gpu-operator-resources   gpu-feature-discovery-brckm                                   1/1     Running     0             6m50s
kube-system              metrics-server-679c5f986d-z8kbc                               1/1     Running     0             10m
default                  gpu-operator-7d9854fc59-26vf9                                 1/1     Running     0             7m37s
kube-system              calico-node-kf85f                                             1/1     Running     1 (14m ago)   35m
kube-system              coredns-64c6478b6c-9g6gz                                      1/1     Running     0             7m37s
portainer                portainer-685c4f4bfc-h7n9k                                    1/1     Running     0             7m37s
kube-system              calico-kube-controllers-87ccff444-dhn62                       1/1     Running     1 (14m ago)   35m
ingress                  nginx-ingress-microk8s-controller-t2s9h                       1/1     Running     0             3m11s
```

# Images
## Option 1: build local, pack into tar, push ctr
Check what you have in ctr repo:
    microk8s ctr images ls

https://microk8s.io/docs/registry-images

## Option 2: private docker registry on localhost:32000
Be sure to do:
    microk8s enable registry

Check your local registry: docker images
Check private registry:    docker images localhost:32000

Should start empty

https://microk8s.io/docs/registry-private