#!/bin/bash

docker build \
 --build-arg LOGSTASH_PLUGINS=logstash-output-opensearch,logstash-input-opensearch \
 -t bitnami/logstash:latest \
 'https://github.com/bitnami/containers.git#main:bitnami/logstash/8/debian-11'
# 'https://github.com/bitnami/bitnami-docker-logstash.git#master:8/debian-11'
#$ docker build -t bitnami/logstash:latest 'https://github.com/bitnami/bitnami-docker-logstash.git#master:8/debian-11'
