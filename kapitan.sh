#!/usr/bin/env bash

KAPITAN_IMAGE="kapicorp/kapitan:v0.30.0"
#KAPITAN_IMAGE="metacoma/kapitan:latest"

kapitan() {
  docker run -t --rm -u $(id -u) -v $(pwd):/src:delegated ${KAPITAN_IMAGE} $*
}

kapitan $*
