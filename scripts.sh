
docker-compose build && docker login && docker push anopa/adminsmart_django:latest


cd ~/Documentos/pala/kind && \
kind create cluster --config=00-cluster-with-2workers-in-localhost.yaml && \
helm install totoro ~/Documentos/pala/adsm/totoro/k8s/totoro

kind load docker-image anopa/adminsmart_django:latest && \
helm install coreapi ~/Documentos/pala/adsm/django/chart/coreapi


Tengo que colocar el HOST_IP para que django lo tome en env del deployment
    https://stackoverflow.com/questions/62224705/disallowedhost-django-deployment-in-kubernetes-cluster-invalid-http-host-header

