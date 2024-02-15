#!/bin/bash

docker run \
    -e NEO4J_AUTH=neo4j/password \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
   --publish=7474:7474 --publish=7687:7687 \
   --volume=`pwd`/plugins:/plugins \
   neo4j:4.4.0

#    -e NEO4JLABS_PLUGINS=\[\"apoc\"] \
