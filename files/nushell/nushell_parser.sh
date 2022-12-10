#!/usr/bin/env bash

NODENAME_NUM_IN_TABLE=${1:-11}

docker exec -i nushell nu --stdin -c 'detect columns | table -w 1000' | awk -F"│" -vNODENAME_NUM_IN_TABLE=10 '
function createNode(nodeName) {
  printf("%s = node.createChild(\"%s\")\n", nodeName, nodeName)
} 
function nodeAttr(nodeName, attr, value) {
  printf("%s[\"%s\"] = \"%s\"\n", nodeName, attr, value)
} 
function nodeName(name) {
  return gensub(/\\-/, "_", "g", name)
}

(NR == 2) {
  for (i = 1; i < NF; i++) {
     HEADER[i] = gensub(/(^ +| +$)/, "", "g", $i)
  }
}

(NR >= 4) {
  for (i = 1; i < NF; i++) {
     DATA[i] = gensub(/(^ +| +$)/, "", "g", $i)
  }
  name = nodeName(DATA[NODENAME_NUM_IN_TABLE])
  createNode(name)
  for (i = 2; i < NF; i++) {
    nodeAttr(name, HEADER[i], DATA[i])
  } 
} 
'

