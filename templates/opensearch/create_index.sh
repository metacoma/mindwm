#!/usr/bin/env
{% set p = inventory.parameters %}
{% set index_patterns = p.opensearch_index_patterns %}

. {{ p.compiled_dir }}/functions.bash

opensearch_wait_200
echo

endpoint=`opensearch_api_endpoint`
for index_pattern in {{ index_patterns.values() | map(attribute='name') | join(' ')}}; do 
   curl -X POST ${endpoint}/.kibana/_doc/index-pattern:${index_pattern} -u '{{ p.opensearch_api_user }}:{{ p.opensearch_api_password }}' -k -H 'Content-Type: application/json' -d '{"type" : "index-pattern","index-pattern" : {"title": "'${index_pattern}'-*","timeFieldName": "timestamp"}}'
done

