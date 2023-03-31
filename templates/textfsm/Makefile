{% set p = inventory.parameters %}
{% set image = p.textfsm.image %}

IMAGE_NAME = {{ image.repo }}
TAG = {{ image.tag }}

minikube-env:
	eval $(minikube docker-env)

build: minikube-env
   	ifndef DOCKER_HOST
        	$(error DOCKER_HOST is not set)
    	endif
	docker build -t $(IMAGE_NAME) .

#push: build
#	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(TAG)
#	docker push $(IMAGE_NAME):$(TAG)

delete:
	kubectl delete -f ./deployment.yaml

logs:
	kubectl -n '{{ p.textfsm.k8s_namespace }}' logs -l name='{{ p.textfsm.k8s_deployment }}' -f --tail=5

exec:
	kubectl -n '{{ p.textfsm.k8s_namespace }}' exec -ti {{ p.textfsm.k8s_deployment }} -- /bin/sh


deploy: build
	kubectl apply -f deployment.yaml
