#!/usr/bin/env bash

COMPILED_DIR=~/mindwm/compiled/freeplane_plugin_grpc/

GRPC_SERVER=127.0.0.1:50051
GRPC_ARGS="-plaintext -proto ${COMPILED_DIR}/grpc/freeplane.proto -format json"
GRPC_CALL="grpcurl -plaintext -proto ./freeplane.proto -d @ ${GRPC_SERVER}"

. ${COMPILED_DIR}/functions.bash

createChild() {
  local name=$1
  local parent_node_id=$2
cat<<EOF  | jq | ${GRPC_CALL} freeplane.Freeplane/CreateChild
{
  "name": "${name}",
  "parent_node_id": "${parent_node_id}"
} 
EOF
} 

nodeDetailsSet() {
  local node_id=$1
  local details="$2"
cat<<EOF  | jq | ${GRPC_CALL} freeplane.Freeplane/NodeDetailsSet
{
  "node_id": "${node_id}",
  "details": "${details}"
} 
EOF
} 

cd ${COMPILED_DIR}/grpc

#grpcurl -plaintext -proto ./freeplane.proto ${GRPC_SERVER} describe
CPU_TEMP_NODE_ID=`createChild "cpu" "" | jq -r '.nodeId'`
while :; do
  t=`sensors -j | jq -r '."coretemp-isa-0000"."Package id 0".temp1_input'`
  nodeDetailsSet ${CPU_TEMP_NODE_ID} "${t}"
  sleep 0.1
done

exit


#json_data() {
#  sensors -j | jq -r '{"name": ."coretemp-isa-0000"."Package id 0".temp1_input|tostring, "parent_node_id": ""}'
#} 
#
#json_data2() {
#cat<<EOF | jq
#{
#  "name": "49",
#  "parent_node_id": ""
#}
#EOF
##  echo '{"name": "test", "parent_node_id": ""}' | jq
#} 
#
#json_data | docker run \
#  -i \
#  -v /home/bebebeko/mindwm/compiled/freeplane_plugin_grpc/grpc/freeplane.proto:/host/freeplane.proto \
#  -w /host  \
#  --network=host \
#  fullstorydev/grpcurl \
#  -proto ./freeplane.proto \
#  -v \
#  -format "json" \
#  -d @ \
#  -plaintext localhost:50051 freeplane.Freeplane/CreateChild 
