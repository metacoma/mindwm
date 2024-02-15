IMAGE_REPO := {{ processing_name }}
IMAGE_TAG := latest
IMAGE_NAME := $(IMAGE_REPO):$(IMAGE_TAG)

build:
	docker build -t $(IMAGE_NAME) .
run: build
	$(eval NEO4J_PORT := $(shell kubectl get svc neo4j-admin -n neo4j -o jsonpath='{.spec.ports[?(@.name=="tcp-bolt")].nodePort}'))
	$(eval NEO4J_HOST := $(shell minikube ip))
	$(eval NEO4J_URL := bolt://$(NEO4J_HOST):$(NEO4J_PORT))
	docker run --rm -it --network=host 	\
		-e NEO4J_URL="$(NEO4J_URL)"	\
 		$(IMAGE_NAME)
