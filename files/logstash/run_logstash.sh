#!/usr/bin/env bash

# --env LOGSTASH_PLUGINS=logstash-output-opensearch \
#  --env LOGSTASH_PIPELINE_CONF_FILENAME=fluentbit.conf \

docker rm -f logstash

docker run -d --name logstash --restart unless-stopped \
  --user ${UID}:${GID} \
  --network host \
  --env LOGSTASH_ENABLE_MULTIPLE_PIPELINES=true \
  -v "/tmp:/tmp" \
  -v `pwd`/config/:/bitnami/logstash/config  \
  -v `pwd`/pipeline/:/bitnami/logstash/pipeline  \
  bitnami/logstash:latest

docker logs -n10 -f logstash
