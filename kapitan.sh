#!/usr/bin/env bash

KAPITAN_IMAGE="kapicorp/kapitan:v0.32.0"
###KAPITAN_IMAGE="metacoma/kapitan:latest"

kapitan() {
	docker run -t -w `pwd` --rm -u $(id -u):$(id -g) -v/tmp:/tmp -v $(pwd):`pwd`:delegated ${KAPITAN_IMAGE} $*
}

kapitan $*
