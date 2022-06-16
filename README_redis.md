install log:

```
bash-5.1$ helm repo add bitnami https://charts.bitnami.com/bitnami
```
```
"bitnami" has been added to your repositories
```
```
bash-5.1$ helm install redis1 bitnami/redis --set auth.password="icub"
```
```
NAME: redis1
LAST DEPLOYED: Wed Feb 16 15:44:50 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: redis
CHART VERSION: 16.4.0
APP VERSION: 6.2.6

** Please be patient while the chart is being deployed **

Redis&trade; can be accessed on the following DNS names from within your cluster:

    redis1-master.default.svc.cluster.local for read/write operations (port 6379)
    redis1-replicas.default.svc.cluster.local for read-only operations (port 6379)



To get your password run:

    export REDIS_PASSWORD=$(kubectl get secret --namespace default redis1 -o jsonpath="{.data.redis-password}" | base64 --decode)

To connect to your Redis&trade; server:

1. Run a Redis&trade; pod that you can use as a client:

   kubectl run --namespace default redis-client --restart='Never'  --env REDIS_PASSWORD=$REDIS_PASSWORD  --image docker.io/bitnami/redis:6.2.6-debian-10-r120 --command -- sleep infinity

   Use the following command to attach to the pod:

   kubectl exec --tty -i redis-client \
   --namespace default -- bash

2. Connect using the Redis&trade; CLI:
   REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis1-master
   REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h redis1-replicas

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/redis1-master : &
    REDISCLI_AUTH="$REDIS_PASSWORD" redis-cli -h 127.0.0.1 -p
```

Got the password:
```
bash-5.1$ export REDIS_PASSWORD=$(kubectl get secret --namespace default redis1 -o jsonpath="{.data.redis-password}" | base64 --decode)
bash-5.1$ echo $REDIS_PASSWORD
icub
```


# connect from outside

```
kubectl port-forward --namespace default svc/redis1-master 6379:6379
```

```
pip install redis
```

```
import redis

r = redis.Redis(
    host='127.0.0.1',
    port=6379, 
    password='icub')
r.set("hello","there")
r.get("hello")
```

