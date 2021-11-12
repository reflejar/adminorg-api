
docker-compose build && docker login && docker push anopa/adminsmart_django:latest


cd ~/Documentos/pala/kind && \
kind create cluster --config=00-cluster-with-2workers-in-localhost.yaml && \
helm install totoro ~/Documentos/pala/adsm/totoro/k8s/totoro \
kubectl create ns databases \
helm install postgres bitnami/postgresql --set postgresUser=anopa,postgresDatabase=adminsmart --namespace databases \
kind load docker-image anopa/adminsmart_django:latest && \
helm install coreapi ~/Documentos/pala/adsm/django/chart/coreapi