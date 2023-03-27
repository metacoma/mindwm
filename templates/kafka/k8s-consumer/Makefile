{% set p = inventory.parameters %}
{% set image_name = p.consumer_image.repo_prefix + consumer_name %}

IMAGE_NAME = {{ image_name }}
TAG = {{ p.consumer_image.tag }}

minikube-env:
	eval $(minikube docker-env)

build: minikube-env
	docker build -t $(IMAGE_NAME) .

#push: build
#	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(TAG)
#	docker push $(IMAGE_NAME):$(TAG)

deploy: build
	kubectl apply -f deployment.yaml
