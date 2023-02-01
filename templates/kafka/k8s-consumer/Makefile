{% set p = inventory.parameters %}
{% set image_name = p.consumer_image.repo_prefix + consumer_name %}

IMAGE_NAME = {{ image_name }}
TAG = {{ p.consumer_image.tag }}

build:
	docker build -t $(IMAGE_NAME) .

push: build
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(TAG)
	docker push $(IMAGE_NAME):$(TAG)

deploy: push
	kubectl apply -f deployment.yaml
